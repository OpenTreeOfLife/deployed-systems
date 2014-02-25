deployed-servers
================

A collection of current (and past) server configuration files for opentree components. These are provided here as a way of sharing admin duties safely, and also as a set of working examples for others who want to use the [opentree deployment tools](https://github.com/OpenTreeOfLife/opentree/tree/master/deploy).

Each named directory represents a complete working system, e.g., 'development' or 'production'. Typically this involves multiple servers working in concert, each providing websites or other services in the OpenTreeOfLife project. 

See the README file in each directory for a description of each system's purpose and notable history. For more on our deployment tools and how to use them, see the [deplyment README](https://github.com/OpenTreeOfLife/opentree/tree/master/deploy) in the main 'opentree' repository.

_**TODO**: Do we need a solution when a server is **shared** between two systems? For example, if someone sets up a new 'test' system that uses a running treemachine in 'development'. Should we repeat its configuration file in both bundles, or note this is a dependency (perhaps in a one-line DEPENDENCIES file) to avoid accidental changes to configuration?_

