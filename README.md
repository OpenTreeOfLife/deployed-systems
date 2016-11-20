deployed-systems
================

A collection of current (and past) server configuration files for opentree components. These are provided here as a way of sharing admin duties safely, and also as a set of working examples for others who want to use the [opentree deployment tools](https://github.com/OpenTreeOfLife/opentree/tree/master/deploy).

### Overview

Each named directory represents a complete working system, e.g., 'development' or 'production'. Typically this involves multiple servers working in concert, each providing websites or other services in the OpenTreeOfLife project.

See the README file in each directory for a description of each system's purpose and notable history. For more on our deployment tools and how to use them, see the [deployment README](https://github.com/OpenTreeOfLife/opentree/tree/master/deploy) in the main 'opentree' repository. Details on the use of each value in a server-config file can be found in the commented [sample.config](https://github.com/OpenTreeOfLife/opentree/tree/master/deploy/sample.config) file.

### Migrating to a new production system

The production system can be updated in either of two ways.  The
easier way is to update it in place using the deployment system.  This
is straightforward.  Some care has to be taken to make sure there's
enough disk space at each step.

The more thorough and principled approach to update is as follows.  We
don't plan to use it in the future, at least not very often.

As each new system is provisioned, it is typically assigned to temporary names (**otXX**.opentreeoflife.org, **otYY**.opentreeoflife.org, etc). Once it's been thoroughly tested, its machines are re-assigned to production domains (**tree**.opentreeoflife.org, **api**.opentreeoflife.org, etc).

Here I will use "incoming" and "outgoing" to describe systems in transition from (for example) dev to production.

Of course, the crux of a migration is updating the DNS records for our production and dev domains. For a fast and smooth changeover, the TTL (time to live) settings for these domains should be very short. But before we "throw the switch", we also need to make some changes to individual server-config files in the **incoming production** system:

- Suspend / redirect live production domains. **IMPORTANT**: See our notes on [**Notifying users of scheduled downtime**](https://github.com/OpenTreeOfLife/opentree/tree/master/deploy#notifying-users-of-scheduled-downtime) for details.

- Re-assign incoming production servers to use the production docstore (OPENTREE_DOCSTORE) and databases.

- Update `*_GITHUB_CLIENT_ID` and `*_GITHUB_REDIRECT_URI` variables, which are domain-specific. These GitHub app registrations are already created, so it's just a matter of moving the production values to the incoming production servers, etc.

- Update all hostnames and base URLs for services to use our standard production domains:
    - OPENTREE_API_HOST
    - OPENTREE_API_BASE_URL (i.e., phylesystem-api)
    - TREEMACHINE_BASE_URL
    - TAXOMACHINE_BASE_URL
    - OTI_BASE_URL
    - OTINDEX_BASE_URL

- If all services are on one machine, just set OPENTREE_API_HOST and prepend this to the base URLs. Easy!

- Set OPENTREE_PUBLIC_DOMAIN=**tree**.opentreeoflife.org

Systems that are not currently mapped to development or production domains are assumed to be test systems. These should use explicit server names like 'ot11.opentreeoflife.org' in their server-config files. And of course they should **not** be using the production docstore or data! Authentication (login) for these systems can be enabled in **local** testing as follows:

- Change `*_GITHUB_CLIENT_ID` and `*_GITHUB_REDIRECT_URI`, which are domain-specific, to use the GitHub apps on development domains.

- If you like you can modify your local HOSTS file (usually `/etc/hosts`) to remap dev domains (**devtree**.opentreeoflife.org, **devapi**.opentreeoflife.org, etc) to point to the corresponding server IPs for ot11, etc.  This might make help to direct certain test scripts to the test system.

- Set OPENTREE_PUBLIC_DOMAIN=**devtree**.opentreeoflife.org

For now, we're using this manual checklist for migrations. Once we've refined the process, we should be able to create easier migration scripts.


### Available servers

The file [opentree-servers.txt](https://github.com/OpenTreeOfLife/deployed-systems/blob/master/opentree-servers.txt) contains a list of all servers currently available to the project. Note that we commonly refer to these in a serialized shorthand, e.g., an AWS server called _ec2-54-203-212-107.us-west-2.compute.amazonaws.com_ will simply be designated **ot6**. When in doubt as to the naming of a server, this list is the authoritative source.

**TODO**: Combine ```opentree-servers.txt``` and ```opentree-ssh-config.txt``` into a single working config file with comments.

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
-rw-------   1 jima  staff  1675 May 20 19:45 repo-phylesystem-0.pem
```


### Running the push scripts

For best results, run the scripts from within the ```opentree/deploy``` directory. If you've installed the ```opentree``` and ```deployed-systems``` repos side by side, let's start from the parent directory of both repos):

```bash
$ cd opentree/deploy
$ ./push.sh -c ../../deployed-systems/development/ot3.config opentree
```

It's a little awkward, but this will ensure a clear separation of tools, configuration files, and sensitive files.

_**TODO**: Do we need a solution when a server is **shared** between two systems? For example, if someone sets up a new 'test' system that uses a running treemachine in 'development'. Should we repeat its configuration file in both bundles, or note this is a dependency (perhaps in a one-line DEPENDENCIES file) to avoid accidental changes to configuration?_  

-- Having a test instance employ services such as taxomachine running on a different system works just fine, as we've seen with the MLS instance.


# Experimental

We are considering a terse configuration file can be used to generate the richer specific
config files.
Some tweaking of the real config files may still be necessary (e.g. the correction of what
branch of each codebase is deployed).
But the ```terse.conf``` would summarize where the main services are deployed.

To try this system out:

    $ mkdir test-dev
    $ cd test-dev
    $ python ../generate-config.py ../terse.conf development

to generate candidate config files that could then be moved to development subdirectory (and then
deployed in the normal way).

**Advantages**

1. We could write a development tool that easily reads the ```terse.conf``` to figure out
the endpoints of the services for the development and production systems. This would make it easier to
write a crontab (or Travis CI hook) that checks for regressions of the APIs in the development and
production environment.

1. ```terse.conf``` is going to a be a lot easier for people to understand, and the developer in charge
of each tweakable tool will just need to make sure that the logic in ```generate-config.py``` is up to date.

**Disadvantages**

1. If we tweak the "raw" configs too much and forget to update ```terse.conf```, then we'll be misled.
