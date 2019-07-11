#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################


import waconn
import argparse
import datetime

# -----------------------------------------------------
# Define and parse command line arguments
# -----------------------------------------------------
parser = argparse.ArgumentParser(description='Run a WAPL command')
parser.add_argument('-e','--engineName', help='name of the engine as defined in the TWSz Connector', required=True, metavar="<engine_name>")
parser.add_argument('-c','--cmds', help='WAPL command to run', required=True, metavar="<cmds>")

args = parser.parse_args()

now = datetime.datetime.utcnow().isoformat()

# -----------------------------------------------------
# Intialize the client utility module
# -----------------------------------------------------
conn = waconn.WAConn('waconn.ini','/twsz/v1/'+args.engineName)

# -----------------------------------------------------
# Query the model and get the js id
# -----------------------------------------------------
resp = conn.textPost('/wapl', text=args.cmds)

r = resp.response
if len(r) == 0:
    print('no response')
    exit(2)

# -----------------------------------------------------
# Print result
# -----------------------------------------------------

print (r)
