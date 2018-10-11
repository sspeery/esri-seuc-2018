## Cron job for indiscriminately granting ArcGIS Pro licenses to any user flagged as a "New User"

Modelled after the excellent work of Peter Knoop at the University of Michigan, this is how Virginia Tech currently ensures that all named users have an ArcGIS Pro license.  We have our ArcGIS Online org set to assign all newly auto-provisioned users the "New_User" custom role, which serves as a flag that gets them picked up by the next run of this script.  Said script then assigns a Pro license, grants ESRI access and switches the user role to org_publisher.   

### Dependencies 
This is currently a python program set to run as a cron job.  In order to work, you need a server that can run scheduled tasks or cron jobs, and a python environment with the arcgis module installed.

### Future work
My intention is to migrate this to an AWS Lambda function.  I will contribute that to the community once complete.

### Last major change
2018-10-11