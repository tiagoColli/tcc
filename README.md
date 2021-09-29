## Introduction

Hi! I am a Feature Store, I was born in Will and I am growing up pretty fast ! I hope you will help me grow and find some bugs as I will centainly help you organize your data and your models. If are are seeing this repository, I guess you already have the necessary permission to clone and edit the files. 

.. note:: If you are not a developer, please go to the section 
    **Installation from Repository** bellow and note that yoy may need your
    bitbucket credentials as this is a private tool.

## Features and Modules
 
 The feature store code are divided in two modules and a cli: 
* Willfsemr - a module responsible to handle the features writing and formatting into an s3 bucket
and the database metadata.
* Willfs - a module responsible to handle the reading of the features and the metadata to an s3 bucket. packages with the Feature Store Cli - a complementary module with the auxiliary functions.


## Building de packages
To meet the requirement of having the reader (willfs) module available along with the writer (willfsemr) - when installing the willfsemr being able to import the Reader, and also have the 'common' folder sharing code between both packages, we've structured the directory tree inside the
feature-store folder in a way that when building the package the setup.py could import any code
inside the directory.

The only thing is that the way setuptools was made one cant have multiple setup's.py inside the same folder, so to get around that we made available a Makefile that switches the setup file depending on
your needs, if you want to build the willfs package just run

``make setup-willfs``

same for willfsemr, just switch to setup-willfsemr
and to build it and deploy to dev

``make deploy-dev``

same thing for prod, just switch to deploy-prod
if you just want to build it to test locally

``pip install -e .``

will be enought

## Installation from Repository

To download via HTTPS **inside the VPN**, simply install the package via: 

``pip install --index-url https://pypi-8uh6f4-prod.souwill.com.br/ willfs``

If everything worked correctly, you can import the modules: 

``import willfs``

## Test

To run pytest, simply run 
``pytest .`` in the root folder of the project. 
This command will look from every function called ``test_*.py`` or ``*_test.py`` and execute each.  If you are wrinting a new one, don't forget to always ``assert`` True or False.
