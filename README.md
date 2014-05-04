deployed-systems
================

A collection of current (and past) server configuration files for opentree components. These are provided here as a way of sharing admin duties safely, and also as a set of working examples for others who want to use the [opentree deployment tools](https://github.com/OpenTreeOfLife/opentree/tree/master/deploy).

### Overview

deployment.conf lists the hosts for the services in production and
development mode (currently just the "api" services are listed).

Each named directory represents a complete working system, e.g., 'development' or 'production'. Typically this involves multiple servers working in concert, each providing websites or other services in the OpenTreeOfLife project. 

See the README file in each directory for a description of each system's purpose and notable history. For more on our deployment tools and how to use them, see the [deplyment README](https://github.com/OpenTreeOfLife/opentree/tree/master/deploy) in the main 'opentree' repository.

### Available servers

The file [opentree-servers.txt](https://github.com/OpenTreeOfLife/deployed-systems/blob/master/opentree-servers.txt) contains a list of all servers currently available to the project. Note that we commonly refer to these in a serialized shorthand, e.g., an AWS server called _ec2-54-203-212-107.us-west-2.compute.amazonaws.com_ will simply be designated **ot6**. When in doubt as to the naming of a server, this list is the authoritative source.

### Sensitive information

Deployment requires a variety of private keys and API secrets. Naturally, these should kept far from this repository. To facilitate sharing of config files, please keep them all in ```~/.ssh/opentree```. It's already a pretty varied collection:

```bash
$ ls -alF ~/.ssh/opentree
total 104
drwx------  15 jima  staff   510 Apr 16 05:35 ./
drwx------@ 20 jima  staff   680 Apr 10 13:08 ../
-rw-------   1 jima  staff    41 Apr  7 02:21 OPENTREEAPI_OAUTH_TOKEN
-rw-------   1 jima  staff    41 Feb 25 13:16 curation-GITHUB_CLIENT_SECRET-dev.opentreeoflife.org
-rw-------   1 jima  staff    41 Apr 15 00:34 treeview-GITHUB_CLIENT_SECRET-dev.opentreeoflife.org
-rw-------   1 jima  staff  1696 Oct 29 10:56 ec2-54-202-160-175.us-west-2.compute.amazonaws.com.pem
-rw-------   1 jima  staff  1696 Oct 29 10:53 ec2-54-212-192-235.us-west-2.compute.amazonaws.com.pem
-rw-------@  1 jima  staff  1679 Dec 20 01:39 opentree-gh.pem
-rw-------   1 jima  staff  1679 Mar 25 02:47 opentree-hbf-test.pem
lrwxr-xr-x   1 jima  staff    54 Feb 25 12:47 opentree.pem@ -> ec2-54-202-160-175.us-west-2.compute.amazonaws.com.pem
-rw-------   1 jima  staff  1675 Dec 31 19:21 opentreeapi-gh.pem
-rw-------   1 jima  staff  1675 Apr  1 16:21 opentreeapi-test-0.pem
-rw-------   1 jima  staff  1679 Mar 23 20:07 opentreeapi-test-gh.pem
```


### Running the push scripts

For best results, run the scripts from within the ```opentree/deploy``` directory. If you've installed the ```opentree``` and ```deployed-systems``` repos side by side, let's start from the parent directory of both repos):

```bash
$ cd opentree/deploy
$ ./push.sh -c ../../deployed-systems/development/ot3.config opentree
```

It's a little awkward, but this will ensure a clear separation of tools, configuration files, and sensitive files.

_**TODO**: Do we need a solution when a server is **shared** between two systems? For example, if someone sets up a new 'test' system that uses a running treemachine in 'development'. Should we repeat its configuration file in both bundles, or note this is a dependency (perhaps in a one-line DEPENDENCIES file) to avoid accidental changes to configuration?_

