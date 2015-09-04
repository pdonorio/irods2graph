
USER=`whoami`
export HOME="/home/$USER"

IRODS_DIR="$HOME/.irods"
IRODS_ENV="$IRODS_DIR/.irodsEnv"

mkdir -p $IRODS_DIR
touch $IRODS_ENV

# dmp1.local
remoteconf="
irodsHost 130.186.13.14
irodsPort 1247
irodsHome '/cinecaDMPZone/home/pdonorio'
irodsUserName pdonorio
irodsZone cinecaDMPZone
irodsCwd '/cinecaDMPZone/home/pdonorio'
"

# my laptop/docker
localconf="
irodsHost rodserver
irodsPort 1247
irodsUserName rods
irodsZone tempZone
"
# Note: for local configuration, password is 'mytest'

echo "$remoteconf" > $IRODS_ENV
#echo "$localconf" > $IRODS_ENV
bash -c "iinit" || exit $?

# # Create a second resource for replicas?
# iadmin mkresc replicaResc unixfilesystem rodserver:/tmp/REPLICA
# #https://docs.irods.org/master/manual/installation/#add-additional-resources

./app.py popolae --size=2

#./app.py popolae --size=20
# ./app.py convert

