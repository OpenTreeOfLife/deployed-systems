#!/usr/bin/env python
from ConfigParser import SafeConfigParser
import codecs
import sys
import os

_CONFIG = None

def config(config_file_path, section, param):
    '''
    Returns the config object if `section` and `param` are None, or the 
        value for the requested parameter.
    
    If the parameter (or the section) is missing, the exception is logged and
        None is returned.
    '''
    global _CONFIG, _CONFIG_FN
    if _CONFIG is None:
        _CONFIG = SafeConfigParser()
        _CONFIG.read(config_file_path)
    try:
        return _CONFIG.get(section, param)
    except:
        sys.stderr.write('Config file "%s" does not contain option "%s in section "%s"\n' % (_CONFIG_FN, param, section))
        return None

def tag2host(host_tag):
    if host_tag == 'ot10':
        host = 'ashby.opentreeoflife.org'
    else:
        host = host_tag + '.opentreeoflife.org'
    return host

if __name__ == '__main__':
    import sys
    config_file_path = sys.argv[1]
    target = sys.argv[2]
    sys.stderr.write('Reading "{}" to build config files for the "{}" deployment.\n'.format(config_file_path, target))
    services_keys = ['api', 'oti', 'treemachine', 'taxomachine', 'browser', 'curator']
    service2node = {}
    node2service = {}
    other_keys = ['studyrepo']
    service2component = {}
    for k in services_keys:
        service2component[k] = k
        service2node[k] = config(config_file_path, target, k)
        node2service.setdefault(service2node[k], []).append(k)
    service2component['browser'] = 'opentree'
    studyrepo = config(config_file_path, target, 'studyrepo')

    repo2sshkey = {
        'phylesystem-0': 'opentreeapi-test-gh.pem',
        'phylesystem-1': 'phylesystem-1.pem',
        'hbf_phylesystem_test': 'opentree-hbf-test.pem',
    }
    node_set = set(service2node.values())
    neo4jhost_tag = service2node['treemachine']
    neo4jhost = tag2host(neo4jhost_tag)
    otihost_tag = service2node['oti']
    otihost = tag2host(otihost_tag)
    apihost_tag = service2node['api']
    apihost = tag2host(apihost_tag)
    for host_tag in node_set:
        sys.stderr.write('Creating config file for {} ...\n'.format(host_tag))
        host = tag2host(host_tag)
        component_list = []
        for service in node2service[host_tag]:
            component_list.append(service2component[service])
        component_str = ' '.join(component_list)
        full_config = '''OPENTREE_TAG={host_tag}
OPENTREE_HOST={host}
OPENTREE_COMPONENTS='{component_str}'
OPENTREE_PUBLIC_DOMAIN=dev.opentreeoflife.org
OPENTREE_IDENTITY=~/.ssh/opentree/opentree.pem
OPENTREE_GH_IDENTITY=~/.ssh/opentree/{github_keyname}
OPENTREE_NEO4J_HOST={neo4jhost} # {neo4jhost_tag}
OPENTREE_DOCSTORE={studyrepo}
TREEMACHINE_BASE_URL=http://${onhstr}/treemachine
TAXOMACHINE_BASE_URL=http://${onhstr}/taxomachine
OTI_BASE_URL=http://{otihost}/oti  # {otihost_tag}
OPENTREE_API_BASE_URL=http://{apihost}/api/v1  # {apihost_tag}

CURATION_GITHUB_CLIENT_ID=9a81785e2af910035667
CURATION_GITHUB_REDIRECT_URI=http://${{OPENTREE_PUBLIC_DOMAIN}}/curator/user/login
# NOTE that GITHUB_CLIENT_SECRET is kept in a separate file, outside of the repo

TREEVIEW_GITHUB_CLIENT_ID=32cb7a650c449237398d
TREEVIEW_GITHUB_REDIRECT_URI=http://${{OPENTREE_PUBLIC_DOMAIN}}/opentree/user/login
# NOTE that GITHUB_CLIENT_SECRET is kept in a separate file, outside of the repo
 

OPEN_TREE_API_LOGGING_LEVEL=debug
OPEN_TREE_API_LOGGING_FILEPATH=/home/opentree/log/api.log
OPEN_TREE_API_LOGGING_FORMATTER=rich
export PEYOTL_LOGGING_LEVEL=debug
export PEYOTL_LOG_FILE_PATH=/home/opentree/log/peyotl.log

# -----
# The opentree_branch command specifies which branch to use for the
# given repo.  The default is always 'master'.

# opentree_branch opentree master
# opentree_branch oti master
# opentree_branch taxomachine master
# opentree_branch treemachine master
# opentree_branch peyotl master

'''.format(host_tag=host_tag,
           host=host,
           component_str=component_str,
           github_keyname=repo2sshkey[studyrepo],
           neo4jhost=neo4jhost,
           neo4jhost_tag=neo4jhost_tag,
           studyrepo=studyrepo,
           otihost=otihost,
           otihost_tag=otihost_tag,
           apihost=apihost,
           apihost_tag=apihost_tag,
           onhstr='{OPENTREE_NEO4J_HOST}'
           )
        ofn = host_tag + '.config' 
        with codecs.open(ofn, 'w', encoding='utf-8') as ofo:
            ofo.write(full_config)
