#!/usr/bin/python
import sys
import subprocess
import os
from os import walk
import glob
import time

# func for help
def printhelp():
    print("""
Data generation and copy utility for Databricks DBFS
source_path: path and filename with wildcards to copy to DBFS
destination_path: path to destination DBFS path
overwrite: overwrite existing files. False by default
sleep_between_copy_msec: sleep between copy of each file specified in milliseconds

Samples:
Copy all files under data that match 2013-9-*.json to destination. Overwrite if files exist.
    python copy_to_databricks.py --source_path="./data/2013-9-*.json" --destination_path="dbfs:/home/cihan/tmp" --overwrite --sleep_between_copy_msec=330
""")


    return

#func for parsing the commandline args
def parse_commandline(_my_args):
    #process commandline arguments
    if (len(sys.argv) == 0):
        #no command line option specified - display help
        printhelp()
        raise("No arguments specified.")

    elif (len(sys.argv) > 0):
        for arg in sys.argv:
            #splitter based on platform
            argsplit = arg.split("=")

            #read commandline args
            if (argsplit[0] == "--source_path"):
                #connection string
                _my_args.source_path = str(argsplit[1])
                continue
            elif (argsplit[0] == "--destination_path"):
                #port number
                _my_args.destination_path = str(argsplit[1])
                continue
            elif (argsplit[0] == "--sleep_between_copy_msec"):
                #port number
                _my_args.sleep_between_copy_msec = int(argsplit[1])
                continue
            elif (argsplit[0] == "--overwrite"):
                #port number
                _my_args.overwrite = True
                continue
            elif ((argsplit[0] == "-h") or (argsplit[0] == "--help") or (argsplit[0] == "--h") or (argsplit[0] == "-help")):
                printhelp()
                sys.exit(0)



class cmd_args:
    # assign defaults
    source_path=""
    destination_path=""
    overwrite=False
    sleep_between_copy_msec=0

# START HERE #
_my_args=cmd_args()

#parse the commandline arguments and validate them
parse_commandline(_my_args)

#internal settings
total_retries = 100
retry_counter = 0

#see if there is a wildcard involved
for _file in glob.glob(_my_args.source_path):
    print ("Copying :", _file, "to", _my_args.destination_path)
    try:
        if (_my_args.overwrite):
            subprocess.run(["databricks",
                "fs",
                "cp",
                _file, 
                _my_args.destination_path,
                "--overwrite"]
                )
        else:
            subprocess.run(["databricks",
                "fs",
                "cp",
                _file, 
                _my_args.destination_path]
                )
        if (_my_args.sleep_between_copy_msec != 0):
            print ("Sleeping ", _my_args.sleep_between_copy_msec/1000, "seconds")
            time.sleep(_my_args.sleep_between_copy_msec/1000)
    except:
        retry_counter = retry_counter+1

