#! /usr/bin/bash

export COMET_LOGGING_FILE=/tmp/comet.log
export COMET_LOGGING_FILE_LEVEL=debug

python3 /zganatra-dev/ai-platform/src/train.py

gsutil cp /tmp/comet.log gs://test-zganatra/comet-debug/test_job_77/comet.log
