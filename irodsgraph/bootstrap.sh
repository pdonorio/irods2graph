
USER=`whoami`
export HOME="/home/$USER"

IRODS_DIR="$HOME/.irods"
IRODS_ENV="$IRODS_DIR/.irodsEnv"
mkdir -p $IRODS_DIR

if [ "$1" == "remote" ]; then
    echo "Remote connection"
    # dmp1.local
    remoteconf="
    irodsHost 130.186.13.14
    irodsPort 1247
    irodsHome '/cinecaDMPZone/home/pdonorio'
    irodsUserName pdonorio
    irodsZone cinecaDMPZone
    irodsCwd '/cinecaDMPZone/home/pdonorio'
    "

    echo "$remoteconf" > $IRODS_ENV
    bash -c "iinit" || exit $?
else

    echo "Working locally"
    # my laptop/docker
    localconf="
    irodsHost rodserver
    irodsPort 1247
    irodsUserName rods
    irodsZone tempZone
    "
    # Note: for local configuration, password is 'mytest'
    # (specified inside docker compose)

    if [ ! -f $IRODS_ENV ]; then
        echo "$localconf" > $IRODS_ENV
        bash -c "iinit" || exit $?

        # # Create a second resource for replicas?
        iadmin mkresc replicaResc unixfilesystem rodserver:/tmp/REPLICA
        # #https://docs.irods.org/master/manual/installation/#add-additional-resources
    fi

    cmd="./app.py --mock -v"
    $cmd popolae --size=20
    if [ "$?" == "0" ]; then
        $cmd convert
    fi

fi
