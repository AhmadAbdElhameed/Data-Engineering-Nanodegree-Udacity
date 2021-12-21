# Project Data Pipelines with Airflow

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

### Prerequisites

Tables must be created in Redshift before executing the DAG workflow. The create tables statements can be found in:

**`create_tables.sql`**

#### Create connection with AWS
##### 1. Open Admin->Connections
##### 2. Click "Create"
##### 3. Set "Conn Id" to "aws_credentials", "Conn Type" to "Amazon Web Services"
##### 4. Set "Login" to your aws_access_key_id and "Password" to your aws_secret_key
##### 5. Press (Save and Create another)
##### 6.Conn Id: Enter redshift.
##### 7.Conn Type: Enter Postgres.
##### 8.Host: Enter the endpoint of your Redshift cluster, excluding the port at the end. You can find this by selecting your cluster in the Clusters page of the Amazon Redshift console. See where this is located in the screenshot below. IMPORTANT: Make sure to NOT include the port at the end of the Redshift endpoint string.
##### 9.Schema: Enter dev. This is the Redshift database you want to connect to.
##### 10.Login: Enter awsuser.
##### 11.Password: Enter the password you created when launching your Redshift cluster.
##### 12.Port: Enter 5439.

## Data Sources

Data resides in two directories that contain files in JSON format:

1. Log data: s3://udacity-dend/log_data
2. Song data: s3://udacity-dend/song_data

## Data Quality Checks

In order to ensure the tables were properly loaded, a data quality checking is performed to count the total records each table has. If a table has no rows then the workflow will fail and throw an error message.

## Project Files 

* `udac_example_dag.py` - The DAG configuration file to run in Airflow
* `create_tables.sql` - Contains the DDL for all tables used in this projecs
* `stage_redshift.py` - Operator to read files from S3 and load into Redshift staging tables
* `load_fact.py` - Operator to load the fact table in Redshift
* `load_dimension.py` - Operator to read from staging tables and load the dimension tables in Redshift
* `data_quality.py` - Operator for data quality checking

## Built With

* [Python 3.6.2](https://www.python.org/downloads/release/python-363/) - Used to code DAG's and its dependecies
* [Apache Airflow 1.10.2](https://airflow.apache.org/) - Workflows platform


