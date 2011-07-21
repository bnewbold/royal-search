#!/usr/bin/env bash

curl -X DELETE "http://localhost:9200/oldpapers"

#while read line; do echo $line | json _id; done < "data.json"
#while read line; do curl -X POST "http://localhost:9200/oldpapers/paper/`echo $line | json _id`" -d '`echo $line`'; done < "data.json"
while read line; do curl -X POST "http://localhost:9200/oldpapers/paper" -d "$line"; done < "data.json"

curl -X POST "http://localhost:9200/oldpapers/_refresh"
