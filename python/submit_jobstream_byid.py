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
parser = argparse.ArgumentParser(description='Submit a job stream to the TWSz plan')
parser.add_argument('-e','--engineName', help='name of the engine as defined in the TWSz Connector', required=True, metavar="<engine_name>")
parser.add_argument('-j','--jsName', help='job stream', required=True, metavar="<job_stream_name>")

args = parser.parse_args()

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
	headers={'How-Many': '1'})

r = resp.json()
if len(r) == 0:
    print('job stream not found')
    exit(2)

jsId=r[0]["id"]

print("the js id is: " + jsId)

# -----------------------------------------------------
# Now submit the jobstream to the plan
# -----------------------------------------------------
submit = {"inputArrivalTime": now}

# now we can submit the js
print "submit parameters: " +str(submit)
resp = conn.post('/plan/current/jobstream/' + jsId + '/action/submit_jobstream', json=submit)

r = resp.json()

for js in r:
	print ('Submitted: '+js)
