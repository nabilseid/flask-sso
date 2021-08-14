import setuptools
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="flask-sso",
    version="0.0.1",
    author="Adludio INC.",
    author_email="datascience@adludio.com",
    description="Adludio sso authentication for flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FutureAdLabs/flask-sso",
    project_urls={
        "Bug Tracker": "https://github.com/FutureAdLabs/flask-sso/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['requests', 'flask']
)
