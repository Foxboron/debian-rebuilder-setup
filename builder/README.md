Builder
===

Builds a package given just the buildinfo file.


# Steps


## Parsing Buildinfo

Parses buildinfo as a Dpkg Control File as the buildinfo
format matches the format. Extracts essential information
from the buildinfo.


## Calculate sources

For each dependency specified in `Build-Depends` of the buildinfo
file, calculate the [snapshot.debian.org](https://snapshot.debian.org/)
timestamp when it first appeared in the archives. Use this to calculate
a complete list of timestamps for each dependency. These timestamps are
now individual sources for the chroot `sources.list`.


## Setup chroot

Find out when the particular version of the package being built
appeared in [snapshot.debian.org](https://snapshot.debian.org/).
If it never appeared, assume its in latest sid. Using this information,
set up a chroot using the calculated base repository (either a snapshot or sid).

Also add the calculate sources in the previous step to the `sources.list` of the
chroot.


## Prebuild hooks


### Chroot Setup

In the chroot set up phase, perform the apt installation of all build depends.


### Starting Build

Just before starting build, verify using `dpkg` that all the required dependencies
are at the exact version.


## Build

Build uses `sbuild` to build the package after which, the checksums are verified.


# Work Remaining

## Do something with results

We need to forward the generated checksums / buildinfo to a central location.
One suggestion was to post signed buildinfo to buildinfo.debian.net.

We intend to expose some metadata about the builds (probably in-toto link metadata
with a sub-layout) for verification purposes by the client (i.e., apt).


# Previous Work and inspiration

There has already been a lot of work regarding this. The two major scripts / code
snippets I modified for this were:

-   <https://bugs.debian.org/774415> - <https://salsa.debian.org/reproducible-builds/packages/sbuil>
-   <https://github.com/StevenC99/reprobuild>

