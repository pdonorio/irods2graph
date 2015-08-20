##############################
## FUNCTIONS

# Random generator
function randword {
    dim=32
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $dim | head -n 1
}

# Create a pseudo random key
function generatekey {
    # generate two random string of fixed val
    rand1=`randword`
    rand2=`randword`
    # create random file name with random file content
    file="/tmp/$rand2"
    echo "$rand1" > $file
    # generate hash from that file ^_^
    key=`sha1sum $file | awk '{print $1}'`
    # remove the file for security reason
    rm $file
    # return value for bash functions
    echo $key
}

##############################
## POPULATION

# How many?
laststep=10

# Create files
for i in `seq 1 $laststep`;
do
    key1=$(generatekey)
    key2=$(generatekey)
    echo "$key2" > $key1.txt
done

# Put them in irods
for i in `ls -1`;
do
    iput $i
done
ils

##############################

