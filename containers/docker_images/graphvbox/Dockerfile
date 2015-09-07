# A quick fix of some neo4j problems
# Note: on virtualbox docker (mac/windows) with volume sharing
# you need to move 'rrd' inside the configuration to outside data directory

FROM neo4j/neo4j
MAINTAINER "Paolo D'Onorio De Meo <p.donoriodemeo@gmail.com>"

RUN apt-get update
RUN apt-get install -y lsof
