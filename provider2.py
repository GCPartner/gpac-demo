BQTABLE = "isv-coe-denisj-00.pier_57_insurance.doctors"
PROJECT_ID = "isv-coe-denisj-00"
DATASET_ID = "isv-coe-denisj-00.pier_57_insurance"
TABLE_ID = "doctors"

from llmutils import get_intended_specialties, validate_specialtycheck, llm_determine_language, llm_determine_location, llm_bison_getquery2
from google.cloud import bigquery
from tabulate import tabulate

def provider2(query: str):
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
    '''
    with open("specialtylist.txt", 'w') as file:
        # Iterate through the list and write each element to the file
        for item in specialtylist:
            file.write(f"{item}\n")  
    '''
    query = query
    #print(query)
    #query = "Find me a demensia doctor for my mom" #add hallucinted location
    #query = "Find a knee pain doctor for my 5 year old" #adds halucinated location
    #query = "I need a sugars doctor in Lousvill" #not avail in dataset
    #query = "I need a doctor for sugar problem in Birmingam"
    #query = "Find me a lung doctor in 60007 who speaks espaniol"
    #query = "Need arthitis doctor in Chikago"
    #query = "I need lab work in Denver" #not avail in dataset, doesn't know to map IDL


    #intended specialty
    #specialtylist_str = specialties()
    query_sp_list_str = []
    query_sp_array = get_intended_specialties(PROJECT_ID, query, specialtylist_str)
    ##########query_sp_list = get_intended_specialties(PROJECT_ID, query, specialtylist_str)
    #####print(query_sp_list[0])
    ###########type(query_sp_list)
    ###########query_sp_array = query_sp_list[0].split("\n")
    #print(f"query_sp_array {query_sp_array}")

    #validate
    providerlist, nonexistlist = validate_specialtycheck(query_sp_array, specialtylist)
    #print(f"providelist {providerlist}")
    print("What exists in our set of provider specialties ? {}".format(providerlist))
    print("What does NOT exist in our set of provider specialties ? {}".format(nonexistlist))
    print("----")
    print("----")
    print("----")
    print("----")
    #location
    location, lexists = llm_determine_location(PROJECT_ID, query)
    #print(location, lexists)

    #language
    language = llm_determine_language(PROJECT_ID,query)
    #####print(language)

    #SQL query
    file_path = 'schema_providers.txt'
    with open(file_path, 'r') as file:
        # Read the entire file into a variable
        schemastring = file.read()
    bisonquery = llm_bison_getquery2(PROJECT_ID, DATASET_ID, TABLE_ID, schemastring, providerlist, location, language)


    print("----")
    #print(bisonquery)

    #execute_sql
    sql_query2 = f"""
        {bisonquery}
    """
    # Execute the query
    query_job2 = client.query(sql_query2)
    # Fetch the results as a list
    #specialtylist2 = [row.specialty.strip() for row in query_job2]
    # Print the list of distinct specialties
    #print(specialtylist2)
    # Get the results of the query job
    results = query_job2.result()
# Convert the results to a list of dictionaries
    results_list = [dict(row) for row in results]

    # Render the home page template with the results
    return results_list, providerlist, location, bisonquery

    print("----")
    print("----")
# Print the results in a tabular format
    print(tabulate(results, headers='keys', tablefmt='fancy_grid'))

    #return results

#final()


