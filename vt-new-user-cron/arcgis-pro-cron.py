# This is the operation we will run in a cron job for new users
# This code is heavily adapted from Peter Knoop, University of Michigan

from arcgis import *
import requests
import time
import csv
import json
import pandas
from time import strftime

# Make the connection to VT ArcGIS Online
with open('orgConfig.json') as configFile:
    myConfig = json.load(configFile)

# now connect
gis = GIS(myConfig['agolOrg']['url'],username=myConfig['agolOrg']['username'],password=myConfig['agolOrg']['password'])    

# verify that it works
try:
    org = gis.properties.name
    print ("Connected to " + org)
except exception as ex:
        print ("Error retrieving AGOL org properties.")
        

new_user_role = myConfig['newUserRole']

# For now, we'll use the licenses and entitlements we expect
entitlements = {'ArcGIS Pro': ['geostatAnalystN', 'spatialAnalystN', 'networkAnalystN', 'dataReviewerN',
                               'dataInteropN', 'workflowMgrN', '3DAnalystN', 'desktopAdvN'],
                'GeoPlanner for ArcGIS': ['GeoPlanner', ],
                'AppStudio for ArcGIS Standard': ['appstudiostd', ],
                'ArcGIS Community Analyst': ['CommunityAnlyst', ],
                'ArcGIS Business Analyst': ['BusinessAnlyst', ]}
# Retrieve the actual licenses for later use
try:
    licenses = {lic: gis.admin.license.get(lic) for lic in entitlements}
    print('License information retrieved.')
except Exception as ex:
    print('Unable to retrieve license information')
    print(ex)


try:
    # Find new users
    new_users = gis.users.search(new_user_role, max_users=9999)
    if len(new_users) == 0:
        print('No new users found.')
    else:
        print(str(len(new_users))+" new users found.")
except Exception as ex:
    print('Unable to perform user search.')
    print(ex)
    print('Exiting.')

for u in new_users:
    print('Granting ArcGIS Pro license to user: {0}'.format(u.username))
    try:
        # Grant entitlements to new users
        for license_type in entitlements:
            lic = licenses[license_type]
            lic.assign(username=u.username, entitlements=entitlements[license_type])
            #print('{0} entitlements granted to user.'.format(license_type) + u.username)
    except Exception as ex:
        print('Error encountered while assigning license {0} to user.'.format(license_type) )
        print(ex)
        print('Exiting.')

    try:
        # Enable ESRI access for new user by changing userType from 'arcgisonly' to 'both'
        u.esri_access = True  # Note: This only works with arcgis package v. 1.3 or later
        print('ESRI access enabled for user '+ u.username)
    except Exception as ex:
        print('Error enabling ESRI access for user.')
        print(ex)
        print('Exiting.')

    try:
        # Change new users' role from "Publisher (New User)" to the standard "Publisher".
        u.update_role('org_publisher')
        print('Role updated for user '+  u.username)
    except Exception as ex:
        print('Error changing user role')
        print(ex)
        print('Exiting.')
