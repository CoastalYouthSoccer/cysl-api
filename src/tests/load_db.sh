#!/bin/bash

source ./common_code.sh

for FILE in test_data/*
do
  mysql -u $DB_USER -p$DB_PASSWORD  -h 127.0.0.1 $DB_NAME < $FILE
done
