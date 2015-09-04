# irods2graph

EUDAT (http://eudat.eu/) Work Package 9.2: experimenting with graph database on entities across the various services

Tracking ideas & progress [here](http://j.mp/cinecagraphdoc).

### Models
*for [B2Safe](http://eudat.eu/b2safe) Eudat service*

```
DataObject{Location:'irods://host:port/ZONE/path'} - [:IS_LOCATED_IN] -> Zone
DataObject - [:STORED_IN] -> Resource - [:IS_AVAILABLE_IN] -> Zone

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
