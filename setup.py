import setuptools

setuptools.setup(
    name="vdb-lite-aws-launcher",
    version="0.0.1",

    description="vdb-lite-aws-launcher",

    author="author",

    package_dir={"": "vdb-lite-aws-launcher"},
    packages=setuptools.find_packages(where="vdb-lite-aws-launcher"),

    install_requires=[
        "aws-cdk.core",
    ],

    python_requires=">=3.6",
)
