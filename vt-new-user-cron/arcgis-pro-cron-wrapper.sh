#!/bin/bash



#replace <workingdir> with location of arcgis-pro-cron directory
#replace <pythonpath> with location of a python environment with the arcgis module

# To run this and log output to a file, you need a crontab entry of the form
# */2 * * * * <workingdir>/vt-agol-new-user-cron-wrapper.sh  >> <workingdir>/new_user_cron.log 2>&1


echo "-----------------------------------------------"
date
<pythonpath>/bin/python <workingdir>/arcgis-pro-cron.py
