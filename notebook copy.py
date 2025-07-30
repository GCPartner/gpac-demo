BQTABLE = "isv-coe-denisj-00.medical_providers.goodclinic"
PROJECT_ID = "isv-coe-denisj-00"
DATASET_ID = "isv-coe-denisj-00.medical_providers"
TABLE_ID = "goodclinic"

#
#from llmutils import get_intended_specialties, validate_specialtycheck, llm_determine_language, llm_determine_location, llm_bison_getquery
from google.cloud import bigquery
from tabulate import tabulate
def final(query: str):
    # Initialize the BigQuery client
    print(PROJECT_ID)
    client = bigquery.Client(project=PROJECT_ID)
    print('hello4')
    # Define your SQL query
    sql_query = f"""
        SELECT DISTINCT specialty
        FROM `{BQTABLE}`,
        UNNEST(specialty) AS specialty;
    """
    # Execute the query
    print('hello45555')
    client.query(sql_query, project='isv-coe-denisj-00')



final('denis')


