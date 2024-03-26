#!/bin/bash

analyzer_ip=$(docker inspect presidio-analyzer | awk -F'"' '/"IPAddress"/{print $4}' | uniq)
anonymizer_ip=$(docker inspect presidio-anonymizer | awk -F'"' '/"IPAddress"/{print $4}' | uniq)

if [ -z "$analyzer_ip" ]; then
    analyzer_ip="presidio-analyzer"
fi

if [ -z "$anonymizer_ip" ]; then
    anonymizer_ip="presidio-anonymizer"
fi



export ANALYZE_URL="http://$analyzer_ip:3000/analyze"
export ANONYMIZE_URL="http://$anonymizer_ip:3000/anonymize" 


echo "ANALYZE_URL set to: http://$analyzer_ip:3000/analyze"
echo "ANONYMIZE_URL set to: http://$anonymizer_ip:3000/anonymize"




