Our current setup (early 2020) still uses `devtree` for the main 
webapp (synth-tree viewer) and study curation tool. But we split
the various "API services" into separate deployments.

For most of these, the name accurately reflects what repo/system 
will be deployed. But note that otcetera is deployed as part of 
`devapi`. This name reflects is central role in receiving and 
dispatching all requests to (dev)api.opentreeoflife.org.

NOTE: otindex is now handled separately via Ansible!

Also NOTE the 'files.opentreeoflife.org' vhost, for which see
[here](http://files.opentreeoflife.org/README.md).
