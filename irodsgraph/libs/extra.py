#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TO BE FIXED - THIS FILE SHOULD BE REMOVED
"""

################################
## POPOLAE

# Some chaos to order
def string_generator(size=32, \
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """ Create a random string of fixed size """
    return ''.join(random.choice(chars) for _ in range(size))

def random_files_into_irods(elements, prefix='abc_', \
    tmp_dir='itmp', irods_dir='mine'):

    # Clean host
    rm("-rf", tmp_dir)
    mkdir("-p", tmp_dir)
    # Clean existing on iRODS
    (status, stdin, stdout) = ICOM["list"][irods_dir].run(retcode = (0,4))
    if status == 0:
        print("Cleaning everything on server")
        ICOM["remove"]["-r", irods_dir]()
    ICOM["create_dir"](irods_dir)
    print("Created directory")

    # Create random files
    for i in range(1,elements):
        rand1 = string_generator()
        rand2 = string_generator()
        filename = prefix + rand1 + ".txt"
        hostfile = tmp_dir + "/" + filename
        with open(hostfile,'w') as f:
            f.write(rand2)

        # Put into irods
        ICOM["save"][hostfile, irods_dir + "/" + filename]()

    print("Generated", elements, "elements")

    # Check data
    print(ICOM["search"](prefix + '%'))

# ################################
# ## READ LOOP

def fill_graph_from_irods(elements):
    print("test")

# # Get list
# objlist = !ils [0-9a-z]*.txt
# metas = {}

# for obj in objlist:
#     ifile = os.path.basename(obj.strip())
#     meta = !imeta ls -d {ifile}
#     metas[ifile] = meta[1]
#     #print("Element " + ifile + " with meta " + meta[1])

# print(metas)
