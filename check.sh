#!/bin/bash

#Written by wai.phyo6
#if [ "$#" -ne 1 ]; then
#    echo "Usage: $0 <input_file>"
#    exit 1
#fi

gr=/bin/grep
aw=/usr/bin/awk

input_file="/root/object_storage_report/cred.txt"

if [ ! -f "$input_file" ]; then
    echo "Input file not found!"
    exit 1
fi

echo "$(date)" > /root/object_storage_report/result.txt
while IFS=',' read -r bucket_name username auth_key || [[ -n "$bucket_name" ]]; do
    #echo "Checking size for $bucket_name bucket..."
    #echo "$bucket_name,$username,$auth_key"

    # Authenticate to the bucket using swift
    export ST_USER="$bucket_name:$username"
    export ST_KEY="$auth_key"
    export ST_AUTH="http://192.168.102.103:8000/auth/v1.0"
    source /root/.bashrc

    /root/.pyenv/shims/swift stat --lh | $gr -E "Account|Bytes in policy" | $aw '/Account/{printf $2} /Bytes in policy/{printf ": %s\n", $5}' >> /root/object_storage_report/result.txt
done < "$input_file"

