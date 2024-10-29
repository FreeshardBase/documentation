# Single User Isolation

## How typical SaaS applications work

Basically all traditional SaaS applications are multi-user applications.
This means that the same application is used by multiple users, and the data of these users is stored in the same database.
This is a very efficient way to build and run applications from the perspective of the application provider, 
but it has some privacy and security implications that are not always desirable.

Most importantly, the application provider has access to all the data of all the users
and there is no good way to prevent this.
Access control is only realized on the application level, 
and the application provider, who has direct access to the database, can always bypass it.

This sets up a natural power imbalance between the application provider and the user,
where the user is always at a disadvantage.
No technical barrier can prevent the misuse of user data and there are many examples of this happening.

But even if the application provider is trustworthy and acts in the best interest of the user,
security breaches can happen and if they do, all user data is usually compromised.

## How Portal works

Portal's architecture works very differently.
It is designed from the ground up to maximize the sovereignty of the Portals' owners.
(For this reason, we don't call people who use Portal _users_, we call them more accurately _owners_.)
Instead of infrastructure being shared between multiple people, each one has their own dedicated infrastructure
in the form of a virtual machine and disk.
This infrastructure of a single Portal is isolated from all others on a basic level 
and only the Portal's owner is able to access them.

The result is a fundamentally different set of conditions, making some things easier and some things harder.
It is easier to guarantee the privacy of owners' data,
since ownership is not just defined by code, which could be faulty or have vulnerabilities, but by the infrastructure itself.
It is also easier to safeguard against security breaches,
since in such an event, there is no huge database with all user data to be compromised.

On the other hand, sharing of data between Portal owners is more difficult - a natural consequence of isolation.
To compensate, Portal apps will need to adapt and offer decentralized sharing mechanisms, 
where data is shared directly between Portals in a peer-to-peer fashion 
while the person that does the sharing retains explicit ownership.

Portal supports this model with its features and APIs,
making it easy for developers to leverage end-to-end encrypted communication between Portals.

From a owner's perspective, this model is expected to feel more natural.
Every piece of data has one explicit place and owner, who decides what may happen to it
instead of living in a fuzzy cloud, governed by often complex access control rules.

## How this differs from typical selfhosting

Since most Portal apps are originally designed as self-hosted applications,
they employ a multi-user architecture by default.
This is because self-hosting is usually done by a single person or organization
who then gives access to others: family, friends, or colleagues.

Often, at a first glance, people think that Portal is just a platform to make self-hosting easier.
But that is not quite right, and the single user isolation is one of the key differences.
It explicitly prevents the sharing of infrastructure between multiple people.

The only exception is where an owner publishes or shares some data or functionality with others,
but this is a much more restricted process than in traditional self-hosting.
Shared data is always still owned and controlled by the one who shares it and physically stays on their Portal.
In particular, an owner could not let others run their own apps or create their own accounts on their Portal.
Instead, sharing usually happens on a per-item basis, like sharing a single file
and the mechanisms are usually special sharing-links, sometimes often unguessable and time-limited.
