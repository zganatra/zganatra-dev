import setuptools

required_packages = [
    "wandb",
    "apache-beam[gcp]",
    "sklearn"
]

setuptools.setup(
    name="test_wandb_dataflow",
    author="ML PLatform",
    author_email="zganatra@etsy.com",
    version="0.0.1.dev",
    packages=setuptools.find_packages(),
    install_requires=required_packages,
    python_requires=">=3.7",
    include_package_data=True,
) 
