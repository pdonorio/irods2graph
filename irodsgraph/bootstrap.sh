
IRODS_DIR="$HOME/.irods"
IRODS_ENV="$IRODS_DIR/.irodsEnv"
mkdir -p $IRODS_DIR
touch $IRODS_ENV

echo "
irodsHost rodserver
irodsPort 1247
irodsUserName rods
irodsZone tempZone
" > $IRODS_ENV

bash -c "iinit"
