#!/usr/bin/env bash

curl -X PUT "http://api.thriftdb.com/test_bucket"
curl -d @schema.json -X PUT "http://api.thriftdb.com/test_bucket/materials"
curl -d @data.json -X POST "http://api.thriftdb.com/test_bucket/materials/_bulk/put_multi"

