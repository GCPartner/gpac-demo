""" This is a simple chat bot that uses HTTP Cookies to retain chat history. In a production
    environment, you would most likely have authentication or store this data in something
    like Google Memory Store. But for this example, HTTP Cookies work just fine! (Asside
    from the 4KB size limit mentioned below.)
"""
import json
import os
import functions_framework
from flask import make_response, render_template
from vertexai.preview.language_models import TextEmbeddingModel, TextGenerationModel
import vertexai
#import chromadb
import markdown

from notebook import final
from provider2 import provider2
from validate import provider23
from tabulate import tabulate

def get_embedding(question: str, project_id: str, region: str, model: str = "textembedding-gecko@001"):
    vertexai.init(project=project_id, location=region)
    embedding_model = TextEmbeddingModel.from_pretrained(model)
    embedding = embedding_model.get_embeddings([question])

    return embedding[0].values


def get_context(embedding, collection, results):
    context = ""
    documents = collection.query(query_embeddings=[embedding], n_results=results)
    print(json.dumps(documents))
    for document in documents['documents'][0]:
        context += f" \n{document}"
    return context


def build_ui_body(env_vars, post_vars, answer=""):
    # collections = chromadb_client.list_collections()
    # questions_sets = ""

    # if len(collections) < 1:
    #    questions_sets = "There are no questions indexed!"

    # for collection in collections:
    #    questions_sets = questions_sets + f'<option value="{collection.name}">{collection.name.replace("_", " ")}</option>'

    if 'question' not in post_vars:
        items = '<div class="h-100 d-flex justify-content-center align-items-center">'
        items = items + "Please use the text box below to ask your question!"
        items = items + '</div>'
    else:
        items = "<div>"
        items = items + '<div class="float-right" style="width: 100%;">'
        items = items + '<div class="float-right">'
        items = items + f"<strong>{env_vars['ui_user_name']}:</strong>"
        items = items + '</div>'
        items = items + '</div>'
        items = items + '<div style="width: 100%;">'
        items = items + '<div class="float-right small p-2 me-3 ' \
                        'mb-1 text-white bg-primary rounded">'
        items = items + post_vars['question']
        items = items + '</div>'
        items = items + '</div>'
        items = items + '<div style="width: 100%;">'
        items = items + '<div class="float-left" style="width: 100%;">'
        items = items + f"<strong>{env_vars['ui_bot_name']}:</strong>"
        items = items + '</div>'
        items = items + '</div>'

        
        items = items + '<div style="width: 100%;">'
        items = items + '<div class="float-left small p-2 ms-3 mb-1 rounded" ' \
                        'style="background-color: #f5f6f7;">'
        #items = items + markdown.markdown(answer)
        print("----")
        print("----")
        print("----")
        print("----")
        # Create a table to display the results
        table = tabulate(answer, headers='keys', tablefmt='html')

        # Add the table to the items list
        items = items + table

        items = items + '</div>'
        items = items + '</div>'
    items = items + '</div>'

    body = render_template('ui.html', items=items, ui_title=env_vars['ui_title'])
    return body

def build_ui_body2(env_vars, post_vars, providerlist, location, bisonquery, answer=""):
    # collections = chromadb_client.list_collections()
    # questions_sets = ""

    # if len(collections) < 1:
    #    questions_sets = "There are no questions indexed!"

    # for collection in collections:
    #    questions_sets = questions_sets + f'<option value="{collection.name}">{collection.name.replace("_", " ")}</option>'
    test = 'Pulmonary Medicine, Critical Care Medicine, Sleep Medicine'
    #location = 'city: NYC'

    if 'question' not in post_vars:
        items = '<div class="h-100 d-flex justify-content-center align-items-center">'
        items = items + "Please use the text box below to ask your question!"
        items = items + '</div>'
    else:
        items = "<div>"
        items = items + '<div class="float-right" style="width: 100%;">'
        items = items + '<div class="float-right">'
        items = items + f"<strong>{env_vars['ui_user_name']}:</strong>"
        items = items + '</div>'
        items = items + '</div>'
        items = items + '<div style="width: 100%;">'
        items = items + '<div class="float-right small p-2 me-3 ' \
                        'mb-1 text-white bg-primary rounded">'
        items = items + post_vars['question']
        items = items + '</div>'
        items = items + '</div>'
        items = items + '<div style="width: 100%;">'
        items = items + '<div class="float-left" style="width: 100%;">'
        items = items + f"<strong>{env_vars['ui_bot_name']}:</strong>"
        items = items + '</div>'
        items = items + '</div>'






        #items = items + markdown.markdown(answer)
        print("----")
        print("----")
        print("----")
        print("----")
        if post_vars['question_num'] == 'Provider2':
            items = items + '<div style="width: 100%;">'
            items = items + '<div class="float-left small p-2 ms-3 mb-1 rounded" ' \
                        'style="background-color: #f5f6f7;">'
            items = items  + "<strong>STEP 1: </strong>" + "Identify and verify the correct speciality" + "<br><br>"
            items = items  + "<strong>This is specialties list identified by the LLM:</strong><br>" + "".join(providerlist) + "<br>"
            items = items  + "<strong>What exists in our set of provider specialties? </strong><br>" + "".join(providerlist) + "<br>"
            items = items  + "<strong>What does NOT exist in our set of provider specialties?</strong><br>" + "[]" + "<br><br>"

            items = items  + "<strong>STEP 2: </strong>" + "Identify location and check spelling" + "<br><br>"
            items = items  + "<strong>This is the location identified by the LLM:</strong><br>" + "".join(location) + "<br><br>"

            markdown_content = bisonquery

            html_content = markdown.markdown(markdown_content)
            
            items = items  + "<strong>STEP 3: </strong>" + "Use determined parameters to create SQL query" + "<br><br>"
            items = items  + "<strong>SQL query generated by the LLM:</strong><br>" + html_content + "<br><br><br>"
            #items = items  + "<strong>SQL query generated by the LLM:</strong><br>" + bisonquery.replace("SELECT", "SELECT<br>").replace("FROM", "<br>FROM").replace("WHERE", "<br>WHERE").replace("AND", "<br>AND").replace("(", "(<br>").replace(")", "<br>)") + "<br><br><br>"
            items = items + '</div>'
            items = items + '</div>'


        items = items + '<div style="width: 100%;">'
        items = items + '<div class="float-left small p-2 ms-3 mb-1 rounded" ' \
                        'style="background-color: #f5f6f7;">'

        # Create a table to display the results
        #print(table)
        # Add the table to the items list
        table = tabulate(answer, headers='keys', tablefmt='html')
        items = items + table

        items = items + '</div>'
        items = items + '</div>'
    items = items + '</div>'

    body = render_template('ui.html', items=items, ui_title=env_vars['ui_title'])
    return body


def get_env_vars():
    # TODO: Add error handling
    env_vars: dict = {}
    env_vars['project_id']: str = os.environ.get('project_id')
    env_vars['region']: str = os.environ.get('region')
    env_vars['chromadb_ip']: str = os.environ.get('chromadb_ip')
    env_vars['chromadb_port']: int = int(os.environ.get('chromadb_port'))
    env_vars['ui_title']: str = os.environ.get('ui_title')
    env_vars['ui_bot_name']: str = os.environ.get('ui_bot_name')
    env_vars['ui_user_name']: str = os.environ.get('ui_user_name')
    env_vars['llm_model']: str = os.environ.get('llm_model')
    env_vars['embedding_model']: str = os.environ.get('embedding_model')
    env_vars['max_output_tokens']: int = int(os.environ.get('max_output_tokens'))
    env_vars['temperature']: float = float(os.environ.get('temperature'))
    env_vars['top_k']: int = int(os.environ.get('top_k'))
    env_vars['top_p']: float = float(os.environ.get('top_p'))

    return env_vars


def get_post_vars(request):
    # TODO: Add error handling
    post_vars: dict = {}
    post_vars['question'] = request.form['question']
    post_vars['collection_name'] = request.form['questions_sets']
    post_vars['question_num'] = request.form['question_num']
    print(post_vars['question'])
    print(post_vars['question_num'])
    return post_vars


def promt_llm(prompt, env_vars):
    vertexai.init(project=env_vars['project_id'], location=env_vars['region'])
    parameters = {
        "temperature": env_vars['temperature'],
        "max_output_tokens": env_vars['max_output_tokens'],
        "top_p": env_vars['top_p'],
        "top_k": env_vars['top_k']
    }
    #print(f"parameters: {parameters}")
    #print(f"env_vars: {env_vars}")
    model = TextGenerationModel.from_pretrained(env_vars['llm_model'])
    print(prompt)
    response = model.predict(prompt=prompt, **parameters)
    print(response)
    print(f"Blocked by saftey filter:  {response.is_blocked}")
    #print(response._prediction_response)
    if response.is_blocked:
        print(response.safety_attributes)
        answer = "The response was blocked by the saftey filters. Please try another question."
    else:
        answer = response.text
    return answer


def answer_question(env_vars, post_vars):
    #collection = chromadb_client.get_collection(name=post_vars['collection_name'])
    #embedded_question = get_embedding(post_vars['question'], env_vars['project_id'], env_vars['region'])
    #context = get_context(embedded_question, collection, post_vars['question_num'])
#    prompt = f"""You are a cheerful and helpful technical support assistant. You will be provided one or more \\
##previously asked "Question" & "Answer" sets. Use only these previously asked questions and answers to answer the \\
#final question. If you can't find the answer in the previously asked "Question" & "Answer" sets say "I can't find \\
#the answer" Use a lot of words and explain your answers. Do not make up answers or guess!
    #Question: {post_vars['question']}
#Answer:"""
    #prompt = post_vars['question']
    if post_vars['question_num'] == 'Provider1':
       answer = final(post_vars['question'])
       providerlist = "" 
       bisonquery = ""
       location = ""
    elif post_vars['question_num'] == 'Provider2':
       answer, providerlist, location, bisonquery = provider2(post_vars['question'])
        #answer = provider23()
    ##answer = final(post_vars['question'])  ###promt_llm(prompt, env_vars)

    return answer, providerlist, location, bisonquery


@functions_framework.http
def main(request):
    """ This is the main function of the Chat Bot"""
    env_vars = get_env_vars()
    #chromadb_client = chromadb.HttpClient(host=env_vars['chromadb_ip'], port=env_vars['chromadb_port'])
    answer = ""
    providerlist = ""
    location = ""
    bisonquery = ""

    if request.method == "POST":
        post_vars = get_post_vars(request)
        answer, providerlist, location, bisonquery = answer_question(env_vars, post_vars)
    else:
        post_vars = {}

    #user_interface = build_ui_body(env_vars, post_vars, answer)
    user_interface = build_ui_body2(env_vars, post_vars, providerlist, location, bisonquery, answer)

    response = make_response(user_interface)

    return response
