from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag, task
from airflow.operators.dummy_operator import DummyOperator
from final_project_operators.stage_redshift import S3ToRedshiftStagingEvents, S3ToRedshiftStagingSongs
from final_project_operators.load_fact import LoadFactOperator
from final_project_operators.load_dimension import LoadDimensionOperator
from final_project_operators.data_quality import DataQualityOperator
from final_project_operators.create_table import CreateRedshiftTables
from udacity.common import final_project_load_star_tables_sql_statements


default_args = {
    'owner': 'udacity',
    'start_date': pendulum.now(),
    'end_date': None,
    'depends_on_past': True, #I want to make sure that especially the table loading will only happen if the previous task completed successfully.
    'retries':1,
    'retry_delay':timedelta(seconds=120),
    'catchup': True
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='@hourly'
)
def final_dag_project():

    start_operator_task = DummyOperator(task_id='Begin_execution')

    create_tables_task = CreateRedshiftTables(
        task_id='Create_tables',
        redshift_conn_id="redshift"
    )

    s3_to_redshift_stage_events_task = S3ToRedshiftStagingEvents(
        task_id = "Stage_events",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_events",
        s3_bucket="airflow-s3-storage",
        s3_key="log_data"
    )

    s3_to_redshift_stage_songs_task = S3ToRedshiftStagingSongs(
        task_id = "Stage_songs",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_songs",
        s3_bucket="airflow-s3-storage",
        s3_key="song_data",
    )

    load_users_dim_table_task = LoadDimensionOperator(
        task_id          ="Load_user_dim_table",
        redshift_conn_id ="redshift",
        table            = "users",
        append           = "true"
    )

    load_songs_dim_table_task = LoadDimensionOperator(
        task_id          = 'Load_song_dim_table',
        redshift_conn_id ="redshift",
        table            = "songs",
        append           = "true"
    )

    load_artists_dim_table_task = LoadDimensionOperator(
        task_id          = 'Load_artist_dim_table',
        redshift_conn_id = "redshift",
        table            = "artists",
        append           = "false"
    )

    load_time_dim_table_task = LoadDimensionOperator(
        task_id          = 'Load_time_dim_table',
        redshift_conn_id = "redshift",
        table            = "time",
        append           = "true"
    )

    load_songsplay_fact_table_task = LoadFactOperator(
        task_id          ='Load_songplays_fact_table',
        redshift_conn_id ="redshift",
        table            = "songsplay"
    )

    run_quality_checks_task = DataQualityOperator(
        task_id          = 'Run_data_quality_checks',
        redshift_conn_id = "redshift",
        table            = "users",
        column           = "u_firstname",
        retries          = 3
    )

# Note that I have chosen the dimension tables to get created before the fact table because of the dependency of the latter on the former (foreign keys).
    start_operator_task >> create_tables_task
    create_tables_task >> s3_to_redshift_stage_songs_task
    create_tables_task >> s3_to_redshift_stage_events_task
    s3_to_redshift_stage_songs_task >> load_users_dim_table_task
    s3_to_redshift_stage_events_task  >> load_users_dim_table_task
    s3_to_redshift_stage_songs_task >> load_songs_dim_table_task
    s3_to_redshift_stage_events_task  >> load_songs_dim_table_task
    s3_to_redshift_stage_songs_task >> load_artists_dim_table_task
    s3_to_redshift_stage_events_task  >> load_artists_dim_table_task
    s3_to_redshift_stage_songs_task >> load_time_dim_table_task
    s3_to_redshift_stage_events_task  >> load_time_dim_table_task
    load_users_dim_table_task >> load_songsplay_fact_table_task 
    load_songs_dim_table_task >> load_songsplay_fact_table_task 
    load_artists_dim_table_task >> load_songsplay_fact_table_task 
    load_time_dim_table_task >> load_songsplay_fact_table_task 
    load_songsplay_fact_table_task  >> run_quality_checks_task


final_dag_project = final_dag_project()
