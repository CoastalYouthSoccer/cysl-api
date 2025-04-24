#!/bin/bash
# Code assumes the Python environment is already established.
# 
source ./common_code.sh
ORIG_PWD=$(pwd)
cd ..
echo "DROP DATABASE IF EXISTS $DB_NAME;" | mysql -u $DB_USER -p$DB_PASSWORD
echo "CREATE DATABASE IF NOT EXISTS $DB_NAME;" | mysql -u $DB_USER -p$DB_PASSWORD

export DATABASE_URL="mysql+asyncmy://$DB_USER:$DB_PASSWORD@localhost:3306/$DB_NAME"
alembic upgrade head
cd $ORIG_PWD
./load_db.sh -u $DB_USER -p $DB_PASSWORD -d $DB_NAME

#coverage run -m pytest
