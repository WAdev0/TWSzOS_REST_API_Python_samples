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
parser = argparse.ArgumentParser(description='List job streams defined in TWSz model')
parser.add_argument('-e','--engineName', help='name of the engine as defined in the TWSz Connector', required=True, metavar="<engine_name>")
parser.add_argument('-j','--jsName', help='job stream filter', required=True, metavar="<job_stream_name_filter>")
parser.add_argument('-n','--howMany', help='max numer of returned job streams', required=False, metavar="<how_many>")

args = parser.parse_args()

howMany = '100'
if args.howMany:
	howMany=args.howMany

now = datetime.datetime.utcnow().isoformat()

# -----------------------------------------------------
# Intialize the client utility module
# -----------------------------------------------------
conn = waconn.WAConn('waconn.ini','/twsz/v1/'+args.engineName)

# -----------------------------------------------------
# Query the model and get the js id
# -----------------------------------------------------
resp = conn.post('/model/jobstream/header/query', 
	json={"filters": {"jobstreamFilter": {"jobStreamName": args.jsName,"validIn": now}}},
	headers={'How-Many': howMany})

r = resp.json()
if len(r) == 0:
    print('job stream not found')
    exit(2)

# -----------------------------------------------------
# Print result
# -----------------------------------------------------

for js in r:
	print (js["key"]["name"])
