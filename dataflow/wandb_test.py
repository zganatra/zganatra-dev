import os
import logging
import sys
import time
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import os
os.environ['WANDB_API_KEY'] = "c4ba628fba75a4ef20686c737a51504bc9fa0465"
import wandb
logging.basicConfig(
    stream=sys.stderr,
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)
_DEFAULT_PROJECT = "etsy-search-ml-dev"
_DEFAULT_REGION = "us-central1"
_DEFAULT_NUM_WORKERS = 2
_DEFAULT_MAX_NUM_WORKERS = 2
_DEFAULT_BUCKET = "gs://test-zganatra/wandb"
_DEFAULT_SERVICE_ACCOUNT = "sa-aiplatform-dev@etsy-search-ml-dev.iam.gserviceaccount.com"
_PROJECT_VPC="project-vpc"

def beam_deploy_func(run):
    """Create beam job to invoke ccp
    """

    import numpy as np
    from sklearn.datasets import load_breast_cancer
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix

    random_state = 42
    cancer = load_breast_cancer()
    print("cancer.keys(): {}".format(cancer.keys()))
    print("Shape of cancer data: {}\n".format(cancer.data.shape))
    print("Sample counts per class:\n{}".format(
        {n: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}))
    print("\nFeature names:\n{}".format(cancer.feature_names))

    X_train, X_test, y_train, y_test = train_test_split(
        cancer.data,
        cancer.target,
        stratify=cancer.target,
        random_state=random_state)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    logreg = LogisticRegression()

    param_grid = {'C': [0.001, 0.01, 0.1, 1, 5, 10, 20, 50, 100]}

    params = {"random_state": random_state,
              "model_type": "logreg",
              "scaler": "standard scaler",
              "param_grid": str(param_grid),
              "stratify": True
              }
    
    run.config.update(params)
    
    clf = GridSearchCV(logreg,
                       param_grid=param_grid,
                       cv=10,
                       n_jobs=-1)
    run.sklearn.plot_learning_curve(clf, X_train, y_train)
    
    clf.fit(X_train_scaled, y_train)

    y_pred = clf.predict(X_test_scaled)

    #print("\nResults\nConfusion matrix \n {}".format(confusion_matrix(y_test, y_pred)))
    run.sklearn.plot_confusion_matrix(y_test, y_pred, ['target'])
   
    
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    metrics = {"f1": f1,
               "recall": recall,
               "precision": precision
               }
    run.log(metrics)
    

def dataflow_wandb_fn():
    """
    server trained image
    :return:
    """
    job_name = f"wandb-{int(time.time() * 1000)}"
    temp_location = os.path.join(_DEFAULT_BUCKET, "tmp", job_name)
    pipeline_args = {
        "runner": "DataflowRunner",
        "job_name": job_name,
        "num_workers": _DEFAULT_NUM_WORKERS,
        "max_num_workers": _DEFAULT_MAX_NUM_WORKERS,
        "project": _DEFAULT_PROJECT,
        "region": _DEFAULT_REGION,
        "temp_location": temp_location,
        "staging_location": temp_location,
        "use_public_ips": False,
        "service_account_email": _DEFAULT_SERVICE_ACCOUNT,
        "subnetwork": f"regions/{_DEFAULT_REGION}/subnetworks/{_PROJECT_VPC}",
        "save_main_session": True,
        "setup_file": "./setup.py"
    }
    with beam.Pipeline(options=PipelineOptions(**pipeline_args)) as pipeline:
        pipeline \
        | 'Create Run' >> beam.Create(wandb.init(reinit=True,project='dataflow-test-sklearn',save_code=True)) \
        | 'Train Model' >> beam.Map(lambda x: beam_deploy_func(run))
        pipeline.run().wait_until_finish()

if __name__ == "__main__":
    dataflow_wandb_fn()
