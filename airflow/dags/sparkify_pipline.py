from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                               LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries


default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
}

dag = DAG('sparkify_pipline',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@hourly',
          catchup=False
          )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


stage_events_to_redshift = StageToRedshiftOperator(
    task_id='staging_events',
    dag=dag,
    table='staging_events',
    redshift='redshift',
    aws_credentials='aws_credentials',
    s3_bucket="udacity-dend",
    s3_key="log_data",
    json_path="s3://udacity-dend/log_json_path.json",
    file_type="json"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='staging_songs',
    dag=dag,
    table='staging_songs',
    redshift='redshift',
    aws_credentials='aws_credentials',
    s3_bucket="udacity-dend",
    s3_key="song_data/A/A",
    json_path="auto",
    file_type="json"
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplay_fact_table',
    dag=dag,
    table='songplay_fact',
    sql_statement=SqlQueries.songplays_table_insert,
    redshift='redshift',
    append_only=False
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_users_dim_table',
    dag=dag,
    redshift='redshift',
    table='user_dim',
    sql_statement=SqlQueries.users_table_insert,
    append_only='False'
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift='redshift',
    table='song_dim',
    sql_statement=SqlQueries.songs_table_insert,
    append_only='False'
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift='redshift',
    table='artist_dim',
    sql_statement=SqlQueries.artists_table_insert,
    append_only='False'
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift='redshift',
    table='time_dim',
    sql_statement=SqlQueries.time_table_insert,
    append_only='False'
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift='redshift',
    tables=['songplay_fact', 'user_dim', 'song_dim', ' artist_dim', 'time_dim']
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


# Dependencies


start_operator >> stage_events_to_redshift
start_operator >> stage_songs_to_redshift

stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_user_dimension_table
load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_time_dimension_table

load_song_dimension_table >> run_quality_checks
load_user_dimension_table >> run_quality_checks
load_artist_dimension_table >> run_quality_checks
load_time_dimension_table >> run_quality_checks

run_quality_checks >> end_operator
