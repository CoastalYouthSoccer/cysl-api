#!/bin/bash

while getopts ":u:p:d:" opt; do
  case $opt in
    u) DB_USER="$OPTARG"
    ;;
    p) DB_PASSWORD="$OPTARG"
    ;;
    d) DB_NAME="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
  esac

  case $OPTARG in
    -*) echo "Option $opt needs a valid argument"
    exit 1
    ;;
  esac
done

DB_USER="${DB_USER:-root}"
DB_PASSWORD="${DB_PASSWORD:-testrootpass}"
DB_NAME="${DB_NAME:-testdb}"
