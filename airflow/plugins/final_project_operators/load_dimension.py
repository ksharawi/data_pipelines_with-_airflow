from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from udacity.common import final_project_load_star_tables_sql_statements
import re

class LoadDimensionOperator(BaseOperator):

    ui_color = '#F98866'
    #query = final_project_load_star_tables_sql_statements.{{}}_table_insert

    @apply_defaults
    def __init__(self,
                 table            = "",
                 redshift_conn_id = "",
                 append           = "false", #default is delete before insert.
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table            = table
        self.append           = append

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        #Check if table is to be deleted before insert or appended.
        if (self.append == "false"):
            self.log.info("You have asked to delete the table before insert.")
            self.log.info("Clearing data from table {}".format(self.table))
            redshift.run("DELETE FROM {}".format(self.table))

        self.log.info("Loading data into table {}".format(self.table))
        for query in final_project_load_star_tables_sql_statements.insert_table_queries:
            if re.search(f'INSERT INTO {self.table}', query):
                print(query)
                redshift.run(query)


#Backup for failed trials:
        #query='final_project_load_star_tables_sql_statements.{}_table_insert'.format(self.table)

        # formatted_query = LoadDimensionOperator.query.format(
        #     self.table
        # )
        #query=f'final_project_load_star_tables_sql_statements.{self.table}_table_insert'
        #print(query)
        #redshift.run(f'final_project_load_star_tables_sql_statements.{self.table}_table_insert')
        #redshift.run(self.query)
