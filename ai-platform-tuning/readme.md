gcloud ai-platform jobs submit training "test-hypertune" \
  --job-dir "gs://test-zganatra/hyperparameter-tuning/hp_job_dir" \
  --package-path ./trainer \
  --module-name "trainer.train" \
  --region "us-central1" \
  --runtime-version="1.9" \
  --python-version="3.5" \
  --scale-tier STANDARD_1 \
  --config $HPTUNING_CONFIG 

# Optional command to stream the logs in the console
gcloud ai-platform jobs stream-logs $JOB_NAME
