from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['wandb==0.9.7', 'lightgbm']

setup(
    name='bank_model',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='My training application package.'
)
