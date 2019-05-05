#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################


import waconn
import argparse
import datetime
import time

# -----------------------------------------------------
# Define and parse command line arguments
# -----------------------------------------------------
parser = argparse.ArgumentParser(description='Change the time dependency of a job in  TWSz plan')
parser.add_argument('-e','--engineName', help='name of the engine as defined in the TWSz Connector', required=True, metavar="<engine_name>")
parser.add_argument('-j','--jsName', help='jobstream name filter', required=True, metavar="<jobstream_name_filter>")
parser.add_argument('-n','--howMany', help='max numer of returned job streams', required=False, metavar="<how_many>")

args = parser.parse_args()

howMany = '100'
if args.howMany:
	howMany=args.howMany

# -----------------------------------------------------
# Intialize the client utility module
# -----------------------------------------------------
conn = waconn.WAConn('waconn.ini','/twsz/v1/'+args.engineName)

# -----------------------------------------------------
# Query the plan and get the job ids
# -----------------------------------------------------
resp = conn.post('/plan/current/job/query', 
	json={"filters": {"jobInPlanFilter": {"jobStreamName": args.jsName}}},
	headers={'How-Many': howMany})

r = resp.json()
if len(r) == 0:
    print('job not found')
    exit(2)
print ("Length of the list of job that matches this filter is",len(r))

# -----------------------------------------------------
# GET JOBS AND SAVE JOBLOGS
# -----------------------------------------------------

for job in r:
	print ("GETTING JOBLOG FOR JOB "+job["name"]+" in JOBSTREAM "+job["jobStreamInPlan"]["name"]+" IA = "+job["jobStreamInPlan"]["startTime"])
	response = conn.get('/plan/current/job/'+job["id"]+'/joblog')
	joblog = response.json()
	# NOTE: THIS PATH MUST EXIST
	joblog_path = "D:/joblog/"
	if not (response.status_code == 200):
		for j in joblog["messages"]:
			if ("EQQM637I" in j or "EQQM391I" in j):
				time.sleep(10)
				response = conn.get('/plan/current/job/'+job["id"]+'/joblog')
				joblog = response.json()
	file=open(joblog_path + job["jobStreamInPlan"]["name"]+"_"+job["jobStreamInPlan"]["startTime"]+"_"+job["name"]+".txt","w+")
	log = joblog["log"]
	file.write(log)
	file.close()
	print ("YOU CAN FIND YOUR JOBLOG HERE: " + joblog_path)