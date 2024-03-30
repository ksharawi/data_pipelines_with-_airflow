import logging

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table            = "",
                 column           = "",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.table            = table
        self.column           = column
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)

        #Check if a table has rows
        logging.info(f"The following data quality check assess if the table {self.table} contains records.")
        records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {self.table}")
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f"Data quality check failed. {self.table} returned no results")
        num_records = records[0][0]
        if num_records < 1:
            raise ValueError(f"Data quality check failed. {self.table} contained 0 rows")
        logging.info(f"Data quality on table {self.table} check passed with {records[0][0]} records")
        
        #Check if a specific column of interest has null values
        logging.info(f"The following data quality check assess if the {self.table}.{self.column} contains any empty values.")
        null_record = redshift_hook.get_records(f"SELECT COUNT(*) FROM {self.table} WHERE {self.column} IS NULL")
        if null_record[0][0] > 0:
            raise ValueError(f"Data quality check failed. Table {self.table}.{self.column} contains NULL values.")
        else:
            logging.info(f"Data quality check passed. Table {self.table}.{self.column} does not contain any empty values.")
