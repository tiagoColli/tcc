Introduction
==============================================

Hi! I am a Feature Store, I was born in Will and I am growing up pretty fast! I hope you will help me and find some bugs, 
I will centainly help you organize your data and your models.
 
.. note:: Note that yoy may need your
    aws credentials as this is a private tool.


Environments
==============================================

Almost all Feature Store functions require a connection with aws, to make that possible we heavly
rely on your AWS_SECRET_ACCESS_KEY environment variable.

As we have the willfs has several envirnoments, **make sure you've setted the AWS_ACCESS_KEY_ID that
matches the envirnoment you're trying to connect to.**


Features and Modules
==============================================
 
The feature store code are divided in three modules by its functions: 
* Feature Store EMR Writer (willfserm) - A module responsible to handle the writing the features and its metadata into an persistent file system (s3). **This package is still only avaible for EMR usage** (Decision Engines Team).
* Feature Store Reader (willfs) - A module responsible to handle the reading of the features and its metadata.
* CLI (built in willfs) - A CLI with some auxiliary functions to interface the user and the feature store.

You can find the descriptive of those modules in :ref:`modindex`.


Feature Store Reader (willfs) Installation
==============================================

To download via HTTPS **inside the VPN**, simply install the package via: 

.. code-block:: bash

    pip install --index-url https://pypi-8uh6f4-prod.souwill.com.br/ willfs

If everything worked correctly, you can import the modules: 

.. code-block:: python

    import willfs

Tests
==============================================

To run pytest, simply run 
``pytest .`` in the root folder of the project. 
This command will look from every function called ``test_*.py`` or ``*_test.py`` and execute each.  If you are wrinting a new one, don't forget to always ``assert`` True or False.

Also, while testing, set the logging level to ``DEBUG`` to show everything, while ``INFO`` will only show the important information.
