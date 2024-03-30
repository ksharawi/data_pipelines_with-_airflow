from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from udacity.common import final_project_drop_tables_sql_statements, final_project_create_tables_sql_statements

class CreateRedshiftTables(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 *args, **kwargs):

        super(CreateRedshiftTables, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info('Dropping before tables before create...')
        for query in final_project_drop_tables_sql_statements.drop_table_queries:
            redshift.run(query)

        self.log.info('Creating tables...')
        for query in final_project_create_tables_sql_statements.create_table_queries:
            redshift.run(query)

        self.log.info('Tables have been created successfully!')
