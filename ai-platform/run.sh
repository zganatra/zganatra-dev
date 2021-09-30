#! /usr/bin/bash

export COMET_LOGGING_FILE=/tmp/comet.log
export COMET_LOGGING_FILE_LEVEL=info

python3 /zganatra-dev/ai-platform/src/train.py \
--n-estimators=500 \
--n-jobs=8 \
--storage-path=gs://test-zganatra/test_job_78

gsutil cp /tmp/comet.log gs://test-zganatra/comet-debug/test_job_77/comet.log
