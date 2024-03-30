Data Pipelines DAG Project
Evidence
1	Workspace
1.1	Project
My work is included in the highlighted files. You will notice that I have added additional files (e.g. create_table.py and final_project_create_tables_sql_statements.py that were used in combination to create the staging and star tables in Redshift).

 ![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/94d8c920-1008-4021-9ab7-89cce6fa045e)

1.2	Code
1.2.1	Dimension Table Append Option
I have added an option for dimension tables to either append or delete-before-insert. As for the fact table it is always insert (as a principle owing to the usually big size of the a fact table).
Below is an example of setting the append option on/off across different dimension tables:

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/79633747-373b-4baf-9b61-9a7db411ee21)
 
This is where the code takes care of reflecting the decision of the user:

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/8d92a572-c509-4465-927b-1f11a2a0f540)

1.2.2	Data Quality Check
I have built on top the “has_rows” operator from the course, and added the check of NULL for a specific column that the user can choose.

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/324becc4-c866-4198-ba6c-10a7b6d9f4b1)

On failure the Scheduler will retry a number of times specified in the operator “retries” parameter:

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/5bf47a57-c705-46d3-9424-c8b650974332)

 
1.2.3	Loading Data from S3 to Staging (Redshift)
I initially used the s3://udacity-dend//log-data and song-data, however I have found them erroneous (overflow of datatype size that couldn’t be resolved), so I switched to s3://udacity-dend/log_data and song_data (which I used previously in the Cloud Data Warehouses module with no problem), and tada! Everything worked fine.
For staging I used log_json_path.json medata file to read the log_data files:

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/8c3d2760-4dbd-4e80-b06e-c719b889de5c)
 
While for the song_data I chose json format as auto:

 ![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/cfd701c5-1a87-4657-a4ca-5c4ca86cda8a)


2	Airflow
The data pipeline name is “final_dag_project”

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/52898269-d46e-4388-96a4-217a800015ce)

2.1	DAG Graph
Below is the representation of all tasks and relationships, all DAG stages have been completed successfully.
You will notice that I have chosen to have the dimension tables created prior to the fact one (unlike what the example from the project instructions) due to the dependency of the fact on the dimension through foreign keys.

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/56d84f8e-2d69-4e7a-9547-7bbd51b4f1db)

2.2	Variables

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/72eca80f-3819-47a9-8b16-36803926d337)

2.3	Connections

2.3.1	AWS Credentials

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/7ac5ee8d-185b-4c0c-88ad-a24460e85137)

2.3.2	Redshift

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/7e46a7b6-bc7a-4b14-ab56-a6f364f554d2)

2.4	Important Note
Please note that errors shown by Airflow are not related to the project, rather they are related to other pipelines from the course which complained after I made changes in some of the files they are dependent on.

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/750186fa-9257-4cb1-85ae-f04ee4689462)

3	AWS
3.1	IAM User

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/0621222c-0a52-40e0-9308-84bc792ea9d1)

3.2	S3 Bucket

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/178fd43b-5f56-4525-8931-baa1757e7a16)
 
3.3	Redshift
3.3.1	Namespace and Workspace

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/84a969cf-3ee7-43b8-9441-dfeebe7ae420)
  
3.3.2	Tables
All Tables

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/fe8afc10-3652-4f46-a46c-cddc0dabbfa4)

staging_songs

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/4fc287d5-bb8e-429a-b3c5-ceed6edeaed6)

staging_events

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/513fca74-7c05-449b-8c55-5f503ad82e26)

users

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/16883f7b-4d3b-45e3-b680-f24f19d4381b)

artists

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/c0aa03e5-64f4-4649-b401-d1991c4ccd75)

songs

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/8872b29f-835d-46a6-9e5d-4b0122ce9a76)

time

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/affcb052-37ee-4766-b638-6d2b961defb3)

songsplay

![image](https://github.com/ksharawi/data_pipelines_with-_airflow/assets/94605032/67501b34-d828-46ec-991c-d88101443a37)
