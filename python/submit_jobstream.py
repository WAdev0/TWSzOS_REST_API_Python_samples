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
# Submit the jobstream to the plan
# -----------------------------------------------------
submit = {"name": args.jsName, "startTime": now}

# now we can submit the js
print "submit parameters: " +str(submit)
resp = conn.post('/plan/current/jobstream/action/submit_jobstream', json=submit)

r = resp.json()

for js in r:
	print ('Submitted: '+js)
