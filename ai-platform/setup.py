from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['comet_ml','google-cloud-secret-manager','google-api-core-grpc >= 1.18.0', 'lightgbm']

setup(
    name='bank_model',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='My training application package.'
)
