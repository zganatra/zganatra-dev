from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['comet_ml','google-cloud-secret-manager','grpcio==1.39.0' ,'grpcio-gcp==0.2.2' ,'lightgbm', 'pandas']

setup(
    name='bank_model',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='My training application package.'
)
