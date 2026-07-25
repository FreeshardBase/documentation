---
draft: false
date: 2026-07-25
authors:
  - max
---

# Putting apps to sleep, and waking them in under two seconds

![Cover image](cover.png)

A shard is a small server. Often a very small one, a VPS with 1 or 2 GB of RAM, and the whole point is that you can install a pile of apps on it and treat them as your own: photos, documents, notes, a recipe box. The trouble is that self-hosted apps are not shy about memory. Immich alone, with its machine-learning workers, will happily take a large bite out of a 2 GB box before you have uploaded a single photo. Install three or four apps like it and the box is full.

<!-- more -->

## The problem with a personal cloud

The obvious fix is to stop the apps you are not using and start them again on demand. We already did that. But cold-starting a container stack is slow, often 30 seconds or more, and that half-minute is exactly where the experience falls apart. One of our owners put it plainly: the single biggest daily annoyance was waiting for an app to wake up. It gets worse with Immich specifically, because its Android app polls the server so rarely that it can take up to ten minutes to even notice the instance is back. That is not something we can fix directly, we don't own the app. The only lever we have is on the server: wake faster.

So the goal became a familiar one with an unfamiliar setting. **Scale-to-zero, the thing you normally only get from big-cloud serverless, but running on a cheap shard with strict per-app isolation.** Idle apps should give their memory back, and waking one should feel instant, not like restarting your computer.

## The answers that didn't work

The first instinct is checkpoint/restore: freeze a running process to disk with all its memory, then restore it later exactly where it was. On Linux that means [CRIU](https://criu.org/), or `docker checkpoint` which wraps it. It is a beautiful idea and it has been "experimental" for years. There is no real docker-compose support, and our apps are compose stacks, not single containers. Ruled out.

The next thought is to switch the whole runtime to Podman, which has friendlier primitives for some of this. But our entire app catalog is built and tested against docker-compose, and migrating the runtime is an ecosystem cost that buys us one feature. Not worth it.

Then there is [Sablier](https://sablierapp.dev/), a nice middleware that starts and stops containers on demand behind a proxy. We looked hard at it. The problem is that it only starts and stops, and stopping is the slow cold path we are trying to avoid. It also wants to own the wake decision, which would fight the control loop we already run to decide what to demote under memory pressure. Two schedulers arguing over the same containers is a bug waiting to happen.

What actually worked turned out to be boring in a good way.

## Freeze, then page out

Two Linux primitives do the whole job.

The first is the **[cgroup freezer](https://docs.kernel.org/admin-guide/cgroup-v2.html)**, which you reach through `docker compose pause`. Pausing a container does not stop it. It freezes every process in it in place, instantly, using no CPU. The catch is that a frozen app still holds all its memory, so on its own, pause saves only CPU, not RAM.

The second primitive fixes that. [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-interface-files) exposes `memory.reclaim`, which tells the kernel to push a cgroup's anonymous pages out to swap. So the sequence is: freeze the app, then proactively reclaim its memory to swap. The RAM comes back for everything else, and the frozen app sits there costing nothing but some disk.

Anonymous pages are the memory an app allocates for its own working state, your data in flight, as opposed to file-backed pages that are just cached copies of things already sitting on disk. They're the pages that would otherwise be lost if you stopped the app, and on the apps we care about they're the bulk of the footprint. The target we set is to hand back roughly three-quarters of a running app's RAM this way.

Waking it is the payoff. There is no cold start, no re-pulling images, no waiting for a database to come up. It is a single `docker compose unpause`, and the app is back exactly as it was, in **under two seconds**. That number is not aspirational; it is asserted by an integration test that pauses and pages a real container stack and then measures the unpause. Compare that to the 30-plus seconds of a full cold start.

Underneath, apps move through three states rather than two:

- **Running** — normal, using RAM.
- **Paused + Paged** — frozen, memory mostly pushed to swap, wakes in ms to ~2s.
- **Stopped** — cold, memory fully freed, the slow 30s+ wake.

An idle app drops from Running to Paused first, the warm state, and only falls to Stopped if it stays idle long enough or the box comes under real pressure. The demotion is driven by [PSI](https://docs.kernel.org/accounting/psi.html), the kernel's pressure-stall information, read from `/proc/pressure/memory`. When memory gets tight, the least-recently-used apps get demoted, and pausing is always preferred over stopping, because pausing is cheap to undo and stopping is not.

Cold starts don't disappear entirely. An app that stays idle long enough, or one caught when the box is genuinely out of memory, still falls all the way to Stopped and pays the full 30s+ wake the next time you reach for it. And the very first start after you install or update an app is always cold, there's nothing frozen to come back to yet. Sleep just makes the slow path the exception instead of every single wake.

## Making a cheap VPS survive swap

Leaning on swap has an obvious risk: swap is slow, and a box that thrashes on wake is worse than one that was just slow to begin with. Two things keep that from happening.

First, **zswap**. Before a page goes to the swapfile on disk, it goes through a compressed cache held in RAM (zstd compression, decompressing in microseconds). On a small VPS most of the paged-out memory never touches the disk at all; it lives compressed in a slice of RAM and comes back almost for free. Every shard now gets a RAM-sized swapfile plus zswap, because the paging half is useless without somewhere to page into.

Second, it shipped behind a kill-switch, with telemetry: transition counters, pause and unpause latency percentiles, PSI snapshots, swap usage, all reported so we can watch the real behavior rather than trust the design doc. We've only just started watching, though, so I can't hand you real-world numbers yet, that's the next thing to report.

## Where this leaves you

If you own a shard, your idle apps now get out of the way. They give their memory back to whatever you are actually using, and when you come back to one, it is usually there in about the time it takes to notice you clicked. A 2 GB box can hold more of your stuff and still feel responsive, which is the entire promise of a personal cloud that behaves like one product rather than a pile of servers.

The interesting part, at least to me, is that the answer was not the exotic one. Checkpoint/restore is the flashy idea everyone reaches for; the thing that actually shipped is a freezer, a swapfile, and a compressed cache, primitives that have been in the kernel for years. Sometimes the boring tools win.

Is there any app you host where wake time drives you up the wall? [Tell me which one](mailto:contact@freeshard.net) and how you use it. And as always, if something isn't behaving the way it should, tell me that too. The idle heuristics are still being tuned, and real usage is what tunes them, just as real bug reports are what fix bugs.
