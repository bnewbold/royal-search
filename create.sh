#!/usr/bin/env bash

BUCKETNAME=test_bucket

curl -X PUT "http://api.thriftdb.com/$BUCKETNAME"
curl -d @schema.json -X PUT "http://api.thriftdb.com/$BUCKETNAME/old_royal_papers"
curl -d @data.json -X POST "http://api.thriftdb.com/$BUCKETNAME/old_royal_papers/_bulk/put_multi"

