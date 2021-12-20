from airflow.hooks.postgres_hook import PostgresHook
from airflow import DAG
from airflow.hooks.S3_hook import S3Hook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    template_fields = ("s3_key",)
    
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION AS '{}'
        {}
        ;
    """

    @apply_defaults
    def __init__(self,
                 table="",
                 redshift_conn_id="",
                 aws_credentials_id="",
                 s3_bucket="",
                 s3_key="",
                 region="us-west-2",
                 extra_params="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region = region
        self.extra_params = extra_params

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info(f"Copying data from S3 to Redshift staging {self.table} table")
        rendered_key = self.s3_key.format(**context)
        self.log.info(f"Rendered Key: {rendered_key}")
        s3_path = f"s3://{self.s3_bucket}/{rendered_key}"

        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.extra_params
        )
        
        self.log.info(f"Executing query to copy data from '{s3_path}' to '{self.table}'")
        redshift.run(formatted_sql)



'''
class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    template_fields = ("s3_key",)
    copy_sql = """
    COPY {} 
    FROM '{}'
    ACCESS_KEY_ID '{}'
    SECRET_ACCESS_KEY '{}'
    """
    

    @apply_defaults
    def __init__(self,               
                 redshift_conn_id="",
                 aws_credential_id= "",
                 table = "",
                 s3_bucket ="",
                 s3_key="",
                 provide_context = True,
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)       
        self.redshift_conn_id = redshift_conn_id
        self.aws_credential_id = aws_credential_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key= s3_key
        

    def execute(self, context):
        #aws_hook = AwsHook(self.aws_credential_id)
        aws_hook = S3Hook(aws_conn_id=self.aws_credential_id, verify=False)
        #
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id )
        self.log.info('Clearing Data from destination staging table')
        redshift.run("DELETE FROM {}".format(self.table))
        self.log.info('Copying data to destination staging table from S3')
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key, 
        )
        redshift.run(sql)
'''