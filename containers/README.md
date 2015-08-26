
# Containers

The chosen technology is [Docker](http://docs.docker.com/mac/started/).

### Images

The irods client container with libraries for neo4j graph database.
Build it with:

```
$ cd PROJECT/containers/docker_images
$ docker build -t pdonorio/neoicommands -f neoicommands .
```

I made it available
[inside the public docker hub](https://hub.docker.com/r/pdonorio/neoicommands/)

## Run project

All required components may be executed with docker
[compose](https://docs.docker.com/compose/) tool.

```
$ cd PROJECT/containers
$ docker-compose up -d
```

If everything is up and running, open a terminal inside the client container

```
$ docker exec -it containers_icom_1 bash
/data# ls
app.py  libs
/data# ipython
In [1]:
```