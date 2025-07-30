BQTABLE = "isv-coe-denisj-00.medical_providers.providers"
PROJECT_ID = "isv-coe-denisj-00"
DATASET_ID = "isv-coe-denisj-00.medical_providers"
TABLE_ID = "providers"

from llmutils import get_intended_specialties, validate_specialtycheck, llm_determine_language, llm_determine_location, llm_bison_getquery2
from google.cloud import bigquery
from tabulate import tabulate
import pandas as pd

def provider23():
    # Initialize the BigQuery client
    client = bigquery.Client()
    # Define your SQL query
    sql_query = f"""
        SELECT DISTINCT specialty
        FROM `{BQTABLE}`,
        UNNEST(specialty) AS specialty;
    """
    # Execute the query
    query_job = client.query(sql_query)
    # Fetch the results as a list
    specialtylist = [row.specialty.strip() for row in query_job]
    # Print the list of distinct specialties
    #print(specialtylist)
    #Create a string of the same to keep handy to use with prompts etc
    formatted_strings = ['"' + s + '"' for s in specialtylist]
    # Combine the formatted strings with square brackets
    specialtylist_str = "[" + ", ".join(formatted_strings) + "]"
    #print(specialtylist_str)




    print("----")
    #####print(bisonquery)

    #execute_sql
    sql_query2 = f"""
        SELECT
  name,
  specialty,
  gender,
  type,
  address
FROM
  `isv-coe-denisj-00.medical_providers.providers`
WHERE
  (
    SELECT COUNT(1)
    FROM UNNEST(specialty) AS x
    WHERE LOWER(x) IN (LOWER("endocrinology & diabetes & metabolism physician"))
  ) >= 1
  AND (
    SEARCH(address, '`"city": "Louisville"`')
  )
    """
    # Execute the query
    query_job2 = client.query(sql_query2)
    # Fetch the results as a list
    #specialtylist2 = [row.specialty.strip() for row in query_job2]
    # Print the list of distinct specialties
    #print(specialtylist2)
    # Get the results of the query job
    results = query_job2.result()

    df = pd.DataFrame(results)

    print(df)
# Convert the results to a list of dictionaries
    #results_list = [dict(row) for row in results]

    print("----")
    #print(tabulate(results_list, headers='keys', tablefmt='fancy_grid'))
    print("----")
    print("----")
    print("----")
   

    # Render the home page template with the results
    return df #results_list


    print("----")
# Print the results in a tabular format
    print(tabulate(results, headers='keys', tablefmt='fancy_grid'))

    #return results

provider23()


