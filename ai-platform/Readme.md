Command run:
```
gcloud ai-platform jobs submit training test_job_21 --project etsy-mlinfra-dev     --module-name=src.train_lgbm     --package-path=./src     --staging-bucket=gs://test-zganatra     --region=us-central1     --scale-tier=CUSTOM     --master-machine-type=n1-standard-8     --python-version=3.7     --runtime-version=2.2     --     --storage-path=gs://test-zganatra/$JOB_NAME     --n-estimators=500     --n-jobs=8
```
