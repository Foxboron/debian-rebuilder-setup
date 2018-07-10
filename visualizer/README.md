Visualizer
======

This module consists of 2 web servers:
* Accumulator: This webserver receives information about builds as and when they happen and stores them. This is supposed to be exposed only inside the network for the other modules to communicate with it.
* Visualizer: This is the only external interface to the whole rebuilder setup with a webserver which exposes the builds and their metadata + buildinfo.

## Accumulator

API Endpoint: `/new_build`

Form parameters: metadata (File) and buildinfo (File)

## Visualizer

API Endpoint: `/sources`

Get the names of the source packages ever rebuilt on this infrastructure

---

API Endpoint: `/sources/<source>`

See all versions of a particular source built on this infrastructure

---

API Endpoint: `/sources/<source>/<version>/metadata`

Get metadata for a particular source version.

---

API Endpoint: `/sources/<source>/<version>/buildinfo`

Get buildinfo for a particular source version.
