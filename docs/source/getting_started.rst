==============================================
Getting Started
==============================================

In this section we will have a hands-on using the feature store. So that this
tutorial can be followed without any major problems, please make sure that 
you have all the dependencies installed:

.. code-block:: 

    Spark 3.0.2
    Hadoop 2.7
    PySpark 3.0.1
    PyArrow 2.0.0

When you install the packages, the python dependencies that can be installed 
via pip will be downloaded and installed.

Creation of the .env file
==============================================

Another important factor for the correct functioning of the feature store and 
to facilitate your work is the `.env` file.

Write the following parameters and settings in a file called `.env` and place 
your AWS credentials on them. Also make sure that the credentials provided 
have access to that bucket in which the features are stored.

The parameters shown below are the default parameters for operation.

.. code-block:: python 

    AWS_ACCESS_KEY_ID="myawskey"
    AWS_SECRET_ACCESS_KEY="myawssecret"


Packages and Import
==============================================

To import the Reader module, simply: 

.. code-block:: python 
    
    from willfs import Reader 

The Writer module is only available to use in Amazon EMR. This package is not present in this distributed library.
Please contact the Data Team in Slack to require the access to the WILLFS-EMR package.


Using the CLI to interact with the feature store
==================================================

When installing the willfs package, a built in cli will be avaible, there are several functions you can use to interact
with the feature store. First, we can list all features from the feature store using the cli:

.. code-block:: bash

    willfs list-features

The response from the command line will be like: 

.. code-block:: python

        Feature                   GroupingKey          Size          Last Modified
    0    | feature_1               | index             581          2021-02-23 16:55:47
    1    | feature_2               | index             1443         2021-02-12 12:36:22
    2    | feature_3               | index             1448         2021-02-12 12:32:18
    3    | application_yearmonth   | id_card_account   1885         2021-02-17 11:06:03
    4    | area_id                 | dr_number         312          2021-02-23 16:38:51
    5    | area_name               | dr_number         316          2021-02-23 16:38:10
    6    | cnt_bvs_queries_ever    | id_card_account   1222         2021-02-12 13:45:50
    7    | cnt_serasa_queries_ever | id_card_account   1231         2021-02-12 13:50:10
    8    | date_diff               | id_card_accoun    1192         2021-02-12 14:14:44
    9    | days_since_application  | id_card_account   1231         2021-02-12 14:10:36
    10   | decil_score_shortterm   | id_card_account   1226         2021-02-12 13:37:26


You can also use the command bellow to check the versions of a given feature:

.. code-block:: bash

    willfs list-feature-version `featurename`


Reading Features
==============================================
To read the features directly from the feature store.

The first step is to create an instance of the Reader. 

If you want the returned dataset to be a **Pandas** dataset, simply: 

.. code-block:: python

    will_reader = Reader()

Otherwise, if you want the returned dataset to be a **Spark** dataset, simply: 

.. code-block:: python

    will_reader = Reader(spark=True)

.. note:: Remember to always use the instance will_reader.spark instance of Spark. \
If you start another instance in you execution code, some conflicts may arise.

If you want to use our pag bucket, you can simply set the environment as follows: 

.. code-block:: python

    will_reader = Reader(environment='pag')

**make sure you've setted the AWS_ACCESS_KEY_ID that matches the envirnoment you're trying to connect to.**

To read a given feature, simply

.. code-block:: python

    read_df = will_reader.read_feature('feature_1')

If you want to read multiple features, simply: 

.. code-block:: python

    read_df = will_reader.read_multiple_features(['feature_1','feature_2','feature_3'])

.. note:: Always verify the grouping key columns when reading multiple features, 
they must be the same.

If you want more informations for a single feature, you can read the metadata:

.. code-block:: python

    metadata = will_reader.read_metadata('feature_1')


Conclusion
==============================================

In this tutorial, you learned how to write and read features in the features store, 
for both Spark and Pandas dataframe.

Also, you can read metadata and list the features. You may find in the next 
pages a detailed description of each available function. 

`If you have any doubts, 
please don't hesitate to contact us in our slack data channel.`
