# Project Data Pipelines with Airflow

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

# Extract Transform Load (ETL) and Extract Load Transform (ELT):
* ETL is normally a continuous, ongoing process with a well-defined workflow. ETL first extracts data from homogeneous or heterogeneous data sources. Then, data is cleansed, enriched, transformed, and stored either back in the lake or in a data warehouse.

* ELT (Extract, Load, Transform) is a variant of ETL wherein the extracted data is first loaded into the target system. Transformations are performed after the data is loaded into the data warehouse. ELT typically works well when the target system is powerful enough to handle transformations. Analytical databases like Amazon Redshift and Google BigQ.

# What is S3?
* Amazon S3 has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. It gives any developer access to the same highly scalable, reliable, fast, inexpensive data storage infrastructure that Amazon uses to run its own global network of web sites." Source: Amazon Web Services Documentation.

# What is RedShift?
Amazon Redshift is a fully managed, petabyte-scale data warehouse service in the cloud. You can start with just a few hundred gigabytes of data and scale to a petabyte or more... The first step to create a data warehouse is to launch a set of nodes, called an Amazon Redshift cluster. After you provision your cluster, you can upload your data set and then perform data analysis queries. Regardless of the size of the data set, Amazon Redshift offers fast query performance using the same SQL-based tools and business intelligence applications that you use today.

# Apache Airflow
Airflow is a platform to programmatically author, schedule and monitor workflows. Use airflow to author workflows as directed acyclic graphs (DAGs) of tasks. The airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed. When workflows are defined as code, they become more maintainable, versionable, testable, and collaborative.

# Data Quality
* Measure of how well a dataset satisfies its intended use: how our downstream consumers are going to utilize this data.
* Adherence to a set of requirements is a good starting point for measuring data quality.

## Examples of Data Quality Requirements
* Data must be a certain size
* Data must be accurate to some margin of error
* Data must arrive within a given timeframe from the start of (SLA)
* Pipelines must run on a particular schedule
* Data must not contain any sensitive information


# Prerequisites

* Tables must be created in Redshift before executing the DAG workflow. The create tables statements can be found in:

**`create_tables.sql`**

* Create connection with AWS
* 1. Open Admin->Connections
* 2. Click "Create"
* 3. Set "Conn Id" to "aws_credentials", "Conn Type" to "Amazon Web Services"
* 4. Set "Login" to your aws_access_key_id and "Password" to your aws_secret_key
* 5. Press (Save and Create another)
* 6.Conn Id: Enter redshift.
* 7.Conn Type: Enter Postgres.
* 8.Host: Enter the endpoint of your Redshift cluster, excluding the port at the end. You can find this by selecting your cluster in the Clusters page of the Amazon Redshift console. See where this is located in the screenshot below. IMPORTANT: Make sure to NOT include the port at the end of the Redshift endpoint string.
* 9.Schema: Enter dev. This is the Redshift database you want to connect to.
* 10.Login: Enter awsuser.
* 11.Password: Enter the password you created when launching your Redshift cluster.
* 12.Port: Enter 5439.


# Project Workflow

* 1- Create Redshift Cluster
* 2- Create tables with query editor in Redshift 
*  <img src=https://github.com/AhmadAbdElhameed/Data-Engineering-Nanodegree-Udacity/blob/master/Data%20Engineering%20Nanodegree/Data%20Pipelines%20with%20Airflow/Project%20Data%20Pipelines%20with%20Airflow/airflow05.PNG>
*  <img src=https://github.com/AhmadAbdElhameed/Data-Engineering-Nanodegree-Udacity/blob/master/Data%20Engineering%20Nanodegree/Data%20Pipelines%20with%20Airflow/Project%20Data%20Pipelines%20with%20Airflow/airflow04.PNG>
* <img src=https://github.com/AhmadAbdElhameed/Data-Engineering-Nanodegree-Udacity/blob/master/Data%20Engineering%20Nanodegree/Data%20Pipelines%20with%20Airflow/Project%20Data%20Pipelines%20with%20Airflow/airflow02.PNG>
* <img src=https://github.com/AhmadAbdElhameed/Data-Engineering-Nanodegree-Udacity/blob/master/Data%20Engineering%20Nanodegree/Data%20Pipelines%20with%20Airflow/Project%20Data%20Pipelines%20with%20Airflow/airflow03.PNG>

* 3- Run the Dag

# Data Sources

Data resides in two directories that contain files in JSON format:

1. Log data: s3://udacity-dend/log_data
2. Song data: s3://udacity-dend/song_data

# Data Quality Checks

In order to ensure the tables were properly loaded, a data quality checking is performed to count the total records each table has. If a table has no rows then the workflow will fail and throw an error message.

## Project Files 

* `udac_example_dag.py` - The DAG configuration file to run in Airflow
* `create_tables.sql` - Contains the DDL for all tables used in this projecs
* `stage_redshift.py` - Operator to read files from S3 and load into Redshift staging tables
* `load_fact.py` - Operator to load the fact table in Redshift
* `load_dimension.py` - Operator to read from staging tables and load the dimension tables in Redshift
* `data_quality.py` - Operator for data quality checking

# Built With

* [Python 3.6.2](https://www.python.org/downloads/release/python-363/) - Used to code DAG's and its dependecies
* [Apache Airflow 1.10.2](https://airflow.apache.org/) - Workflows platform

# Final Dag View

<img src=https://github.com/AhmadAbdElhameed/Data-Engineering-Nanodegree-Udacity/blob/master/Data%20Engineering%20Nanodegree/Data%20Pipelines%20with%20Airflow/Project%20Data%20Pipelines%20with%20Airflow/finished.PNG>
