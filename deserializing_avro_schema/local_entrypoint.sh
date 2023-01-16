#!/usr/bin/env bash

python /code/deserializing_avro_schema/save_schema_to_karapace.py
faust -A deserializing_avro_schema.main:app worker -l info
