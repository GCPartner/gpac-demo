from vertexai.preview.language_models import TextEmbeddingModel, TextGenerationModel
# Function returns a list of specialties
def llm_standardize_address(project: str, address: str, region="us-central1"):
    import vertexai
    from vertexai.preview.language_models import TextGenerationModel
    
    vertexai.init(project=project, location=region)
    parameters = {
        "max_output_tokens": 1024,
        "temperature": 0,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    prompt = f"""Task: standardize address information

About You:
For the follow address extract the fields 'street', 'city', 'state' and 'zip' and return the results in JSON structure.  The entire json structure should be a string with no extra spaces or newline characters.

address:
{address}

Your Response:
"""
    #print("Prompt \n{}\n".format(prompt))
    response = model.predict(
        prompt,
        **parameters
    )
    #print(f"Response from Model: {response.text}")
    return response.text

    
def get_intended_specialties(project: str, query: str, specialtylist: str, region="us-central1"):
    import vertexai
    from vertexai.preview.language_models import TextGenerationModel
    
    vertexai.init(project=project, location=region)
    parameters = {
        "max_output_tokens": 8192,
        "temperature": 0,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison-32k")
    prompt = f"""Task: Only Extract Relevant Provider Specialties

About You:
You are a medical expert. You have access to a list of medical specialties provided as part of the prompt in the "List of Specialties" Your sole objective is to identify and return the specialties directly related to the given query. You MUST only use the specialties listed in the provided "List of Specialties" and disregard all other information. 
You have a very strict job and cannot create any specialty not specified in the "List of Specialties"



Instructions:

Do not lie or make up an answer
Response should include only specialties from provider "List of Specialties".
Do not include specialties that are not in the list.
Consider age-related criteria: If the query specifies a need for a child, focus on pediatric specialties. For older patients, concentrate on geriatrics or adult specialties.
Do not consider any other information, such as location or state.
If no matching specialty is found, respond with "No specialty found."
The response format should be a string with specialties (if more than 1) separated by commas.

Example: Psychiatry, Geriatric Medicine


"List of Specialties":
{specialtylist}
Query:
{query}

Response:
"""
    #print("Prompt \n{}\n".format(prompt))
    response = model.predict(
        prompt,
        **parameters
    )
    print(f"Response from Model: {response.text}")
    responsetext = response.text
    responsetext = responsetext.replace('"', "")
    result_array = [item.strip() for item in responsetext.split(',')]
    #print(f"cleaned up result array from llmutils: {result_array}")

    return result_array

def get_intended_specialties1(project: str, query: str, specialtylist: str, region="us-central1"):
    import vertexai
    from vertexai.preview.language_models import TextGenerationModel
    
    vertexai.init(project=project, location=region)
    parameters = {
        "max_output_tokens": 8192,
        "temperature": 0.1,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison-32k")
    prompt = f"""Task: Extract Relevant Specialties

About You:
You have access to a list of medical specialties provided in the "List of Specialties" Your sole objective is to identify the intended specialty in the query and find the closest matches in the presented "List of Specialties"/ You MUST only use the List provided. You have a very strict job and cannot create any specialty not specified in the "List of Specialties"
If you don't find a match do not return anything, say "None found"

Instructions:
You have access to a list of medical specialties provided in the "List of Specialties" Your sole objective is to identify the intended specialty in the query and find the closest matches in the presented "List of Specialties"/ You MUST only use the List provided. You have a very strict job and cannot create any specialty not specified in the "List of Specialties"
If you don't find a match do not return anything, say "None found"
Your response should include only specialties from the "List of Specialties"
Do not include specialties that are not in the list named "List of Specialties" in any circumstance
Consider age-related criteria: If the query specifies a need for a child, focus on pediatric related specialties in the list as a priority. For older patients, concentrate on geriatrics or adult specialties as a priority.
Do not consider any other information, such as location or state.
If no matching specialty is found, respond with "No specialty found."

Example:
Query: "I am looking for a sleep doctor in Texas."
List of Specialties:
[Alzheimer's and Dementia, Circadian Rhythm Disorders, Dementia,Headaches,Narcolepsy,Neuropathy,Sleep Apnea,Circadian Rhythm Disorders,Sleep and Epilepsy Issues]

Expected Response: ["Sleep Apnea", "Circadian Rhythm Disorders", "Sleep and Epilepsy Issues"]

List of Specialties:
{specialtylist}

Query:
{query}

Your Response:
"""
    #print("Prompt \n{}\n".format(prompt))
    response = model.predict(
        prompt,
        **parameters
    )
    #print(f"Response from Model: {response.text}")
    responsetext = response.text
    responsetext = responsetext.replace('"', "")
    result_array = [item.strip() for item in responsetext.split(',')]


    return result_array

def palm_determine_primary(project: str, query: str, specialtylist: str, region="us-central1"):
    import vertexai
    import json
    from vertexai.language_models import TextGenerationModel
    
    vertexai.init(project=project, location=region)
    parameters = {
        #"candidate_count": 1,
        "max_output_tokens": 256,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    template = f"""Medical Specialty Assistant:

Role: You are a medical assistant tasked with identifying the most relevant primary and secondary medical specialties based on the provided inputs.

Input:
- Specialty List: This is a list of medical specialties.
- Query: This is a search query indicating the type of doctor a patient is looking for.

Task:
Your objective is to generate two sets of information:
1. Primary List: This list should contain at most three primary medical specialties that best match the query.
2. Secondary List: This list should include secondary medical specialties that may also be relevant to the query.

Output Format:
You should return an array of only the identified primary medical specialties.

Specialty List:
{specialtylist}

Query:
{query}
"""
    
    response = model.predict(
        template,
        **parameters
    )
    
    print(f"Response from Model: {response.text}")
    responsetext = response.text
#    responsetext = responsetext.replace('"', "")
#    result_array = [item.strip() for item in responsetext.split(',')]
    result_array = [item.strip() for item in responsetext.strip('[]').split(',')]
    return result_array

def validate_specialtycheck(primarylist: list, specialtylist: list):
    elist = []
    nelist = []
    for i in primarylist:
        if i.lower() not in [x.lower() for x in specialtylist]:
            nelist.append(i)
        else:
            elist.append(i)
    return elist, nelist

def llm_determine_location(project: str, query: str, region="us-central1"):
    import vertexai
    import json
    from vertexai.language_models import TextGenerationModel
    
    vertexai.init(project=project, location=region)
    parameters = {
      #  "candidate_count": 1,
        "max_output_tokens": 256,
        "temperature": 0.1,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    template = f"""Task: Extract Location Details (if available)
About You:
You have the ability to identify location information mentioned in the query.

Instructions:

Extract address information from the query and format it like requested.
If there are no address or location indicators, return "None."
If the query mentions a state, return the state abbreviation in uppercase.
When a country or state or city is not mentioned, only if you have good confidence regarding those pieces of information, then only add those in from your knowledge. If you know a city is "Round Rock" and you know if its in texas then add the state information also. 
Structure the output as a string with key value pairs separated by commas. No commas should be used within the keys and the values.
Correct spelling mistakes
'street' : <street>,'city':<city>,'state':<state>,'zip':<zipcode>

Don't have keys for empty values 

Examples:
Query: "I am looking for a sleep doctor near Dewberry Ct, Plano"
Output: 'street':'Dewberry Ct','city':'Plano'

Query: "I am looking for a sleep doctor near Dewberry Ct, Plano, Texas"
Output: 'street':'Dewberry Ct','city':'Plano','state':'TX'

Query: "I am looking for a sleep doctor near Dewberry Ct, Plano, Texas 75025"
Output: 'street':'Dewberry Ct','city':'Plano','state':'TX','zip':'75025'

Query: "I am looking for a sleep doctor in Austin"
Output: 'city':'Austin'
Query: "I am looking for a sleep doctor in Austin 78732"
Output: 'city':'Austin', 'zip': '78732'
Query:
{query}
Output:
"""
    response = model.predict(
       template,
       **parameters
    )
    lexists = True    

    print(f"Response from Model:{response.text}")
    larray = response.text.split(',')
    address = response.text.strip()
    if address == "None":
        lexists = False
    else:
        address = address.replace("', '","','")
        address = address.replace("': '","':'")
    return address, lexists

def llm_determine_language(project: str, query: str, region="us-central1"):
    import vertexai
    import json
    from vertexai.language_models import TextGenerationModel
    
    vertexai.init(project=project, location=region)
    parameters = {
      #  "candidate_count": 1,
        "max_output_tokens": 256,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    template = f"""Task: Extract Language Details (if available)

About You:
You possess the ability to identify language information mentioned in the query.

Instructions:

Your response should contain only the extracted language information from the query.

Return a comma-separated string where each value represents an identified language.
You are tolerant of spelling errors. Even if the query has a language misspelled, you can identify the correct one.

If there is no mention of a language, return a default of "English".

Examples:
Query: "I am looking for a sleep doctor near Dewberry Ct, Plano who speaks Hindi or Spanish"
Output: "Hindi, Spanish"

Query: "I am looking for a sleep doctor near Dewberry Ct, Plano, Texas"
Output: ""

Query: "I am looking for a sleep doctor near Dewberry Ct, Plano, Texas 75025 who speaks Portugeese"
Output: "Portuguese"

Query:
{query}
Output:
"""
    response = model.predict(
       template,
       **parameters
    )
    
    print(f"Response from Model: {response.text}")
    responsetext = response.text
    result_array = []
    if responsetext != "":
        result_array = [item.strip() for item in responsetext.strip('[]').split(',')]
    return result_array 

def llm_bison_getquery(project: str, datasetname: str, tablename: str, schemastring: str, providerlist: list, location: str, language: list, region="us-central1"):
    # Schema is mandatory, atleast one other is mandatory
    import vertexai
    import json
    from vertexai.language_models import TextGenerationModel
    
    vertexai.init(project=project, location=region)
    parameters = {
      #  "candidate_count": 1,
        "max_output_tokens": 256,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    template = f"""Task: Create a BigQuery SQL Query

About You:
You are an expert at BigQuery SQL Query, given the schema and the various arguments provided
Here are some instructions below

Instructions:
* Arguments are provided which might be a single variable or a list. In each section it is specified whether all conditions need to be met in the array (AND) or one of the arguments in the list are enough to be met (OR)
An example of using the where clause for the case when the specialty being search is Sleep Apnea OR Sleep obstruction is

 WHERE (
  SELECT COUNT(1) 
  FROM UNNEST(specialty) AS x 
  WHERE LOWER(x) IN (LOWER("Sleep Apnea"), LOWER("Sleep obstruction"))
  ) >= 1

An example of a where clause for the case when both Sleep Apnea AND Sleep obstruction is being searched 

 WHERE (
  SELECT COUNT(1) 
  FROM UNNEST(specialty) AS x 
  WHERE LOWER(x) IN (LOWER("Sleep Apnea"))
  ) >= 1
AND 
(
  SELECT COUNT(1) 
  FROM UNNEST(specialty) AS x 
  WHERE LOWER(x) IN (LOWER("Sleep obstruction"))
  ) >= 1

* Dataset name and Table names are provided as arguments
* Using "BigSearch" implies to use the function SEARCH with the column mentioned
eg If it is suggested to use bigsearch to search for a string "bar" in a columns named "message" you can do this
SELECT * FROM my_dataset.Logs WHERE SEARCH(message, 'bar')
*  
An example of the entire query is here
SELECT
  name,
  specialty,
  acceptingstatus,
  gender,
  language,
  services,
  affiliations,
  address_saddress
FROM
  `datasetname.tablename`
WHERE
  (
    SELECT COUNT(1)
    FROM UNNEST(specialty) AS x
    WHERE LOWER(x) IN (LOWER("Sleep Apnea"), LOWER("Cardiology"))
  ) >= 1
  AND (
    SEARCH(address_saddress, '`"city":"Elgin","state":"IL"`')
  )
  AND (
    SEARCH(language, 'English')
  )
Inputs:
Datasetname: this is a string
{datasetname}

Tablename: this is a string
{tablename}

Specialty: For this argument the query should looking for any of the strings specified in the list provided and use the field "specialty" in the schema. "ARRAY_CONTAINS" does not exist in 
the BigQuery vocabulary. Use the UNNEST function for the array type schema elements.
{providerlist}

Location: this argument is an array of strings. However the schema element For this argument the query should use bigsearch with the "address_saddress" field in the schema. This field is a string type. If it has double quotes, surround the whole single quotes and back ticks like this '`"Key":"Value"`'. 
{location}

Language: The "language" field in the schema is a string type and not an array. Do not use UNNEST but use the SEARCH function. If the input has more than one language then use the SEARCH function with 
one input string at a time. 
{language}

Schema:
{schemastring}

Do not use markdown for output format

Output:

"""
    response = model.predict(
       template,
       **parameters
    )
    
    print(f"Response from Model: {response.text}")
    responsetext = response.text
    '''
    result_array = []
    if responsetext != "":
        result_array = [item.strip() for item in responsetext.strip('[]').split(',')]
    return result_array 
    '''
    return responsetext

def llm_bison_getquery2(project: str, datasetname: str, tablename: str, schemastring: str, providerlist: list, location: str, language: list, region="us-central1"):
    # Schema is mandatory, atleast one other is mandatory
    import vertexai
    import json
    from vertexai.language_models import TextGenerationModel
    
    vertexai.init(project=project, location=region)
    parameters = {
      #  "candidate_count": 1,
        "max_output_tokens": 256,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    template = f"""Task: Create a BigQuery SQL Query

About You:
You are an expert at BigQuery SQL Query, given the schema and the various arguments provided
Here are some instructions below

Instructions:
* Arguments are provided which might be a single variable or a list. In each section it is specified whether all conditions need to be met in the array (AND) or one of the arguments in the list are enough to be met (OR)
An example of using the where clause for the case when the specialty being search is Sleep Apnea OR Sleep obstruction is

 WHERE (
  SELECT COUNT(1) 
  FROM UNNEST(specialty) AS x 
  WHERE LOWER(x) IN (LOWER("Sleep Apnea"), LOWER("Sleep obstruction"))
  ) >= 1

An example of a where clause for the case when both Sleep Apnea AND Sleep obstruction is being searched 

 WHERE (
  SELECT COUNT(1) 
  FROM UNNEST(specialty) AS x 
  WHERE LOWER(x) IN (LOWER("Sleep Apnea"))
  ) >= 1
AND 
(
  SELECT COUNT(1) 
  FROM UNNEST(specialty) AS x 
  WHERE LOWER(x) IN (LOWER("Sleep obstruction"))
  ) >= 1

* Dataset name and Table names are provided as arguments
* Using "BigSearch" implies to use the function SEARCH with the column mentioned
eg If it is suggested to use bigsearch to search for a string "bar" in a columns named "message" you can do this
SELECT * FROM my_dataset.Logs WHERE SEARCH(message, 'bar')
*  
An example of the entire query is here
SELECT
  name,
  specialty,
  gender,
  type,
  address
FROM
  `datasetname.tablename`
WHERE
  (
    SELECT COUNT(1)
    FROM UNNEST(specialty) AS x
    WHERE LOWER(x) IN (LOWER("Sleep Apnea"), LOWER("Cardiology"))
  ) >= 1
  AND (
    SEARCH(address, '`"city": "Elgin", "state": "IL"`')
  )
Inputs:
Datasetname: this is a string
{datasetname}

Tablename: this is a string
{tablename}

Specialty: For this argument the query should looking for any of the strings specified in the list provided and use the field "specialty" in the schema. "ARRAY_CONTAINS" does not exist in 
the BigQuery vocabulary. Use the UNNEST function for the array type schema elements.
{providerlist}

Location: this argument is an array of strings. However the schema element For this argument the query should use bigsearch with the "address" field in the schema. This field is a string type. If it has double quotes, surround the whole single quotes and back ticks like this '`"Key": "Value"`'. 
{location}

Schema:
{schemastring}

Do not use markdown for output format

Output:

"""
    response = model.predict(
       template,
       **parameters
    )
    
    print(f"Response from Model: {response.text}")
    responsetext = response.text
    responsetext = responsetext.replace("```","")
    responsetext = responsetext.replace("sql","")
    '''
    result_array = []
    if responsetext != "":
        result_array = [item.strip() for item in responsetext.strip('[]').split(',')]
    return result_array 
    '''
    return responsetext
    

    

