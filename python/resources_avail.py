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
parser = argparse.ArgumentParser(description='Change the availability of a resource in  TWSz plan')
parser.add_argument('-e','--engineName', help='name of the engine as defined in the TWSz Connector', required=True, metavar="<engine_name>")
parser.add_argument('-r','--resName', help='resource name filter', required=True, metavar="<resource_name_filter>")
parser.add_argument('-a','--avail', help='availability yes/no', required=True, metavar="yes|no")
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
# Query the plan and get the resource ids
# -----------------------------------------------------
resp = conn.post('/plan/current/resource/query', 
	json={"filters": {"resourceInPlanFilter": {"resourceName": args.resName}}},
	headers={'How-Many': howMany})

r = resp.json()
if len(r) == 0:
    print('resource not found')
    exit(2)

# -----------------------------------------------------
# Change availability of all resources
# -----------------------------------------------------

for res in r:
	print ("Changing availability for "+res["resourceInPlanKey"]["name"])
	response = conn.get('/plan/current/resource/'+res["id"])
	res = response.json()
	print (res)
	print ("current overridden availability: "+res["defaultConstraints"]["zosSpecificAttributes"]["overriddenAvailability"])
	# Set overriddenAvailability and save
	res["defaultConstraints"]["zosSpecificAttributes"]["overriddenAvailability"] = "YES" if (args.avail == 'yes') else "NO"
	print ("new overridden availability: "+res["defaultConstraints"]["zosSpecificAttributes"]["overriddenAvailability"])
	res = conn.put('/plan/current/resource/'+res["id"],json=res)
	print (res)

	
