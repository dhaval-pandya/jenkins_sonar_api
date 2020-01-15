#!/bin/bash
#sudo apt-get install xmlstarlet
jenkinsUrlBase='http://admin:test123@localhost:8080'
oldExtentionName="SonarQube_Scanner"
newExtentionName="Sonarqube_scanner_2.8"

callJenkins() { # funcPath
    curl --silent --show-error -g "${jenkinsUrlBase}${1}"
}

callJenkins '/api/xml?tree=jobs[name]' | xmlstarlet sel -t -v '//hudson/job/name' | while read projectName ; do

    echo "Processing ${projectName}..."
    
    echo "\nUpdating ${projectName} file ${configFile}-----------------------\n"
    configFile="/var/lib/jenkins/jobs/${projectName}/config.xml"
    #echo $configFile
    echo "\nUpdating configuration of ${projectName} having file ${configFile}...\n"
    sed -i "s/$oldExtentionName/$newExtentionName/g" "$configFile"
    echo "\n updated ${oldExtentionName} Extention with ${newExtentionName} \n"

done

echo "\nRestarting jenkins...\n"
service jenkins restart