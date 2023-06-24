#!/bin/bash

echo "127.0.0.1:5432:postgres:postgres:postgres" > ~/.pgpass
echo "127.0.0.1:5432:test:postgres:postgres" >> ~/.pgpass
chmod 600 ~/.pgpass
psql --host=127.0.0.1 --port=5432 --username=postgres -w -c "create database test"
psql --host=127.0.0.1 --port=5432 --username=postgres -w -d "test" -c "CREATE TABLE usertable (YCSB_KEY VARCHAR(255) PRIMARY KEY not NULL, YCSB_VALUE JSONB not NULL);"
psql --host=127.0.0.1 --port=5432 --username=postgres -w -c "GRANT ALL PRIVILEGES ON DATABASE test to postgres;"


exit 0