import time

from kfp import components
from kfp.v2 import compiler, dsl
from kfp.v2.google.client import AIPlatformClient

# Required Parameters
PROJECT_ID = 'etsy-mlinfra-dev'
USER = 'zganatra@etsy.com'
BUCKET_NAME = 'test-zganatra'
OUTPUT = f'gs://{BUCKET_NAME}/vertex/pipelines/test_wandb'
REGION = 'us-central1'
OUTPUT_GCS_PATH = OUTPUT + str(int(time.time())) + '/'
PIPELINE_ROOT = 'gs://{}/pipeline_root/{}'.format(BUCKET_NAME, USER)


@dsl.pipeline(
    name='wandb-pipeline',
    description='Vertex pipeline test for wandb',
    pipeline_root=PIPELINE_ROOT
)
def taxo_recs_pipeline():
    now=time.time()
    inference_job_gen = components.load_component_from_file("beam_inference.yaml")
    inference_job_gen(
        storage-path='gs://test-zganatra/test-job',
        n-estimators=500,
        n-jobs=8
    )


if __name__ == '__main__':
    pipeline_func = taxo_recs_pipeline
    compiler.Compiler().compile(
        pipeline_func=pipeline_func, package_path='pipeline_spec.json'
    )

    api_client = AIPlatformClient(project_id=PROJECT_ID, region=REGION)
    response = api_client.create_run_from_job_spec(
        'pipeline_spec.json', pipeline_root=PIPELINE_ROOT, enable_cache=False
    )
