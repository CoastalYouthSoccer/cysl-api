#!/bin/bash
# Code assumes the Python environment is already established.
# 
source ./common_code.sh
export ENV_FILE="ci.env"
ORIG_PWD=$(pwd)
mysql -e "DROP DATABASE IF EXISTS $DB_NAME;" -u $DB_USER -p$DB_PASSWORD -h 127.0.0.1
mysql -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;" -u $DB_USER -p$DB_PASSWORD -h 127.0.0.1

export DATABASE_URL="mysql+asyncmy://$DB_USER:$DB_PASSWORD@localhost:3306/$DB_NAME"
cd ..
alembic upgrade head
cd $ORIG_PWD
./load_db.sh -u $DB_USER -p $DB_PASSWORD -d $DB_NAME

#coverage run -m pytest
