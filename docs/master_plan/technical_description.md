# Technical Description of Portal

To understand the project that is Portal, we need to understand the product that is Portal. What follows is a description of the product itself with some - but not too much - technical detail. It might not immediately become clear how this meets the aforementioned requirements or solves the aforementioned problems. That is normal. Some implications are indirect which is why they will be explained further down.

## Portal, the thing itself

Each single Portal is a computer. It behaves like you are used to from computers like a notebook or a smartphone: there is an operating system with a graphical user interface which you can use to manage all things about it. You can use it to install and run applications that were created by others. Each app has its own GUI and its own logic and runs only for you. You can store data in the shape of files on your Portal, as can the apps. So in many ways a Portal is something that has been around for a few decades now.

But: a Portal has no hardware you can touch. That sets it apart from any computer that consumers are used to. Each Portal runs on cloud infrastructure, its hardware is virtual. The implications of this are huge and they are all discussed later. To make it short: Portal instantly beams itself to any physical device you want it to and it has superpowers that come with the cloud like being managed, always-on, or upgradeable with a single click.

It is important not to confuse Portal with a SaaS app. Most SaaS apps also use virtual hardware, but they utilize it as a tool on top of which the developers build the app. That means you share the hardware with all the other users. Only with Portal you exclusively own the virtual hardware. This is like staying at a hotel vs. your own apartment or taking taxis vs. your own car.

## Portals have names

Each Portal has a unique identity from the moment it is created. This identity is a random alphanumeric string, the kind of identity computers are good at working with, humans not so much. For humans, we shorten it to the first six digits. It is still random, but easier to remember and to type, similar to a telephone number or an android from StarWars, and it remains sufficiently unique. (Technical detail: a Portal’s ID is the hash of its public key.)

An example for a Portal ID is: c0p3x5.

You might wonder why we introduce such a complicated thing to Portal and the decision is surely not done lightly. It is the simplest approach that satisfies several conflicting requirements from the areas of security, cryptography and ease of use. Further discussion of this decision is a topic for a future publication.

## Accessing a Portal

As mentioned above, a Portal beams itself to any physical device its owner (and that of the device) wants it to. Since it is a virtual computer living in the cloud, the owner cannot directly access it and needs to use other devices as middle-men. But those devices are just empty shells. Compare them to a keyboard and monitor that you plug into your desktop PC. Even though you mainly interact with them, they are not the PC.

During the prototype phase, browsers are the empty shells that Portal beams itself into. In other words, every Portal has a web interface you can access. You can find the web interface of the Portal above at https://c0p3x5.p.getportal.org. (Note the ID in the web address.) A browser is well suited for that task because it is specifically made to provide a sandboxed environment where the user interface of a remote service can be displayed. Still, there will be client applications later and they will greatly enhance Portals’ capabilities.

## Pairing physical devices

What is the act of plugging in periphery for a PC is pairing a device for Portal. The process is very quick and painless and done in seconds. You need to have one device at hand that is already paired. Then you use it to scan a QR code on the new device or vice versa. That’s it, the complete Portal is now accessible from the new device.

You can do similar things today with some SaaS applications like messengers that allow you to pair more client devices. But with Portal, this happens on another level: you pair to the platform, not the app. Once paired, all apps on Portal become available, no need to pair each one separately.

## Apps

What makes smartphones so versatile is the ability to install apps and that anyone may develop them, so even for niche use-cases there are apps in the store. The smartphone offers a platform for apps to run on and makes all the bells and whistles available to it. This clear separation of concerns - common functions in the platform, specific logic in the app - has been a huge success.

Portal replicates that. However, Portal’s architecture adds new advantages to the concept. For example, instead of installing apps on a device (or multiple devices), you install them on Portal which means they instantly appear on all paired devices. Install once, use everywhere. Also, since people only need a single Portal and because of its cloud-superpowers, there are more common functions that can be part of the platform - and don’t have to be part of the app. Examples are contacts/friends, end-to-end encrypted communication, and access control. And then there is hardware: a smartphone app can access the smartphone’s hardware (read position, use camera, vibrate, etc.) but a Portal can use all the paired hardware at once. There are lots of new use-cases to be explored based on those capabilities.

## There are already hundreds of Apps

Every Portal app is a collection of docker containers, something you would start up using docker-compose. One of the containers must publish a normal web interface. That is all that is needed for a basic Portal app and the important implication is: there are hundreds of such apps out there. The selfhosting community creates and maintains lots of open-source applications that work exactly like that. They are meant for people with technical expertise to host on their own servers but many of them work just as well when used as Portal apps. That means that there is a large offering of suitable apps available right now and the prototype app store is therefore already well-populated.

## Peers

One of the weirder consequences of the current way we do things is the coupling of messengers with encryption methods. WhatsApp, Signal, Telegram all come with their own encryption schemes baked in and even promote them. As if those two things - messaging and encryption - have anything to do with each other. They don’t, or rather they shouldn’t.

In a better world, encryption (and contact/identity management, which is tightly coupled with encryption) should be part of the platform and messaging would be an app that only uses this platform feature. Many other apps would also use the same feature for communicating securely with others. No app developer would have to take on a daunting task like encryption for a relatively trivial use-case like messaging.

Portal does it that way. A Portal owner establishes connections between their Portal and those of others. This is aided by the Portal IDs mentioned above: they are good at preventing spoofing and are ensuring that the end-to-end encrypted channel that can now be established is cryptographically sound. This channel can now be used by any app with a simple API call. What was once only available to app developers with significant resources is now built-in for everyone.

## Good old filesystem

In our opinion, a filesystem is an underrated feature of computers. It once was the single place where you can organize your data but newer paradigms pushed it in the background or got rid of it altogether. Mobile apps hide their file structure away and SaaS offerings don’t let you touch it at all. And yet, a filesystem is such a natural way of arranging data e.g. by project or by topic. It also lets you collect files of different types together in one place. With current SaaS apps, this has become completely impossible.

It is also a simple way for apps to interoperate, just by giving multiple apps access to the same files. An image gallery, a social networking app and a photo manipulation app can all share the same image files without the user having to send them back and forth.

For these reasons, Portal embraces the file system and makes it a first-class citizen again. It is one of the cases where making the inherent complexity transparent is actually simpler than trying to hide it behind leaky abstractions. And it is in line with the idea of giving power to the user: the power to organize their data on their terms.

## Public and private Views

Since a Portal is always on and always online, it can take the role of the public online presence that is currently played by social networks: an online profile, visible to anyone, with information about a person and a kind of timeline. Equivalents of Facebook, Twitter, Instagram, or LinkedIn could exist as Portal apps. They would publish your information: some of it completely public, some only to a select group of peers. Others would access the content with their browser or through the same app on their Portal. The app could also compile a timeline of all the people you follow, one that is curated only by you.

With the decentralized nature of Portal, this is all happening peer-to-peer and end-to-end-encrypted and without a middleman.

But we can go further than replacing existing ideas. A Portal can provide a public view that is the single place for interacting with the owner. Like a business card on steroids. Someone just needs to know your Portal and can access this page. It would allow them to see your information but also chat with you, call you, book an appointment with you, and so on, all from a single interface. If they access it through their own Portal, they might get privileged access based on their identity, like booking appointments at odd hours.

## Noone wants to manage their own server

In the early days of the internet, people actually thought that everyone would manage their own server. However, doing this has remained complicated for too long and internet adoption has spread too fast to non-technical demographics, so a market gap was created: a demand of active participation met a lack of supply of easy ways of doing so. Centralized services came to the rescue and started providing the means of participation using their platforms.

Unfortunately, we quickly became used to it and what could have been a temporary fix until having your own server became easy enough for everyone remains the only way to participate. So in a way, Portal picks up this unfinished task of making it a no-brainer to have your own server, basically by managing all the technical details for you.

Among the things a Portal owner does not need to think about are: choosing hardware, replacing hardware, upgrading hardware, making backups, managing DNS, managing certificates, securing anything, synchronizing data. Portal does all these things on its own, so you get all the benefits of your own server in a package that is as easy as a smartphone.

## Wrap Up of Digital Lifes

To sum up what Portal is: it is a computer that works similar to what people are used to, but lives in the cloud which gives it superpowers. No technical skills are needed to use it, so it achieves all three properties of which other systems only achieve two: It is usable on any device, it is a private and user-owned space, and it is simple to use for everyone.

A Portal is simultaneously its owner's identity on the internet, their digital archive, their public profile, their digital assistant, and much more with the right apps. Those apps are supplied by third-party developers and Portal makes it really easy for them by handling a lot of common concerns itself (hosting, storage, encrypted communication, etc.).

Through all of that, Portal remains grounded. It renounces bells and whistles that provide no real benefit (like recommendation algorithms) or oversimplifications that make everything more complicated in the end (like letting every app manage their data in a silo).

Ultimately, Portal has the potential to replace all other paradigms of computing for consumers because almost all use-cases can be realized on Portal. And it will feel much saner, more controlled and more sovereign.
