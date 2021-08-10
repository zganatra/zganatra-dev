import numpy as np
import pandas as pd
import lightgbm
import wandb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from wandb.lightgbm import wandb_callback
from shared.code_test import actual_execution
import os
os.environ['WANDB_API_KEY'] = "c4ba628fba75a4ef20686c737a51504bc9fa0465"

parameters = {
    'application': 'binary',
    'objective': 'binary',
    'metric': 'auc',
    'is_unbalance': 'true',
    'boosting': 'gbdt',
    'num_leaves': 31,
    'feature_fraction': 0.5,
    'bagging_fraction': 0.5,
    'bagging_freq': 20,
    'learning_rate': 0.05,
    'verbose': 0
}

run = wandb.init(project="aiplatform-lgbm-project", config=parameters)

actual_execution()
