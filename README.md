
# Data objects mapped to Graph DB

Project for EUDAT (http://eudat.eu/) - Work Package 9.2.
Experimenting with graph databases on connecting entities
across the different services.

### Models
*Instance related to [B2Safe](http://eudat.eu/b2safe) service*

```
DataObject{Location:'irods://host:port/ZONE/path'} - [:IS_LOCATED_IN] -> Zone
DataObject - [:STORED_IN] -> Resource - [:IS_AVAILABLE_IN] -> Zone
DataObject - [:IS_OWNED_BY] -> Person

DataObject - [:BELONGS_TO] -> Collection [:INSIDE] -> Collection [:IS_PLACED_IN] -> Zone
    Note: Path is computable from Collections walking

DataObject - [:DESCRIBED_BY] -> MetaData
Collection - [:DESCRIBED_BY] -> MetaData
Resource - [:DESCRIBED_BY] -> MetaData

DataObject - [:UNIQUELY_IDENTIFIED_BY] -> PID{EudatChecksum:'xyz'}
    Note: PID is also a Metadata attribute (PID: x/y-z-w)
    but since Checksum is its property it is better handled as a node

DataObject - [:IS_REPLICA_OF{PPID, ROR}] -> DataObject
    Note: PPID = PID of replicated object, computable by query
    Note: ROR is the ancestor, the first element. Should be computable.
    Note: Replica relation is preferable a node instead of property { Replica: 0/1 }

# To be added as model/properties:
# - checksum timestamp (integrity)
# - ACL

```

These models [are mapped as objects](https://github.com/pdonorio/irods2graph/blob/master/irodsgraph/libs/ogmmodels.py#L13) inside the python project using
the [**neomodel**](http://neomodel.readthedocs.org/en/latest/) OGM library

### Get started

**Initial setup to launch docker containers**

```
cd containers
./restart
# A working client shell will open
./app.py -h
# Show usage of the main app
```

Now you can choose between a local connection or remote.

**Local environment**
<small>(irods + graphdb + client on the same test machine, e.g. laptop)</small>

```
bash bootstrap.sh
# You will be prompted for irods password. It's 'mytest'
```

There will be a first random data creation and insert.
It will be followed by conversion to graph.
At this point you may open http://localhost/ to use *ipython notebooks*.

**Remote environment**
<small>(irods server is with real data in production)</small>

Edit 'irodsgraph/bootstrap.sh' to verify if irods data are correct.
Then:

```
bash bootstrap.sh
# You will be prompted for your real irods password.
./app convert --size=10
# Port 10 elements from your irods server to the local graph db.
```

At this point you may:
* check your local graph on web url http://localhost:7777
* open http://localhost/ to use *ipython notebooks*.

*N.B. **localhost** may be your server IP (e.g. if you use docker with virtualbox)*