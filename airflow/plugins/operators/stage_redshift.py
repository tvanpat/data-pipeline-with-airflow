from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook


    
class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    
    
    json_copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        TIMEFORMAT as 'epochmillisecs'
        JSON '{}'
        COMPUPDATE OFF
    """


    @apply_defaults
    def __init__(self,
                 table="",
                 redshift="",
                 aws_credentials="",
                 s3_bucket="",
                 s3_key="",
                 json_path="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift = redshift
        self.aws_credentials = aws_credentials
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_path = json_path


    def execute(self, context):
        aws = AwsHook(self.aws_credentials)
        credentials = aws.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift)
        self.log.info(f'Starting transfer of staging data from {self.s3_bucket} / {self.s3_key} to {self.table}')
        self.log.info(f'Deleting data from {self.table}')
        redshift.run("DELETE FROM {}".format(self.table))
        self.log.info(f'Copying data from {self.s3_bucket} / {self.s3_key} to {self.table}')
        
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        

        formatted_sql = StageToRedshiftOperator.json_copy_sql.format(
                self.table,
                s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.json_path
            )
        redshift.run(formatted_sql)
