#!/usr/bin/env bash

curl -X DELETE "http://localhost:9200/oldpapers"

while read line; do curl -X POST "http://localhost:9200/oldpapers/paper" -d "$line" &> /dev/null ; done < "data.json"

curl -X POST "http://localhost:9200/oldpapers/_refresh"
