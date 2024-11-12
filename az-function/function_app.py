import azure.functions as func
import logging
import requests
import json
import os

from copilot_response import create_text_event, create_done_event

# Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def convert_ghcp_extension_to_ai_search(ghcp_extension):
    conversation_id = ghcp_extension["copilot_thread_id"]
    messages = []
    for message in ghcp_extension["messages"]:
        messages.append({
            "role": message["role"],
            "content": message["content"]
        })
    return {
        "conversation_id": conversation_id,
        "messages": messages
    }

@app.function_name(name="query")
@app.route(route="", methods=["POST"])
def query(req):
    logging.info('Python HTTP trigger function processed a request.')
    
    ai_search_endpoint = os.environ["AI_SEARCH_ENDPOINT"]

    gchp_payload = req.get_json()
    # print("\n-- User Message GCHP Payload ----------------\n")
    # print(gchp_payload)
    # print("\n---------------------------------------------\n")
    
    ai_search_payload = convert_ghcp_extension_to_ai_search(gchp_payload)
    # print("\n-- AI Search Payload ------------------------\n")
    # print(ai_search_payload)
    # print("\n---------------------------------------------\n")

    headers = {"Content-Type": "application/json"}
    ai_response = requests.post(ai_search_endpoint, headers=headers, json=ai_search_payload, timeout=30)

    # get the last message from response_json.choices.messages.content
    ai_response_json = ai_response.json()
    last_message = ai_response_json["choices"][-1]["messages"][-1]["content"]
    # print("\n-- AI Search Response ------------------------\n")
    # print(ai_response_json)
    # print("\n---------------------------------------------\n")

    # respond to user in GitHub Copilot Chat
    ghcp_response = {
        "body": create_text_event(last_message) + create_done_event()
    }
    
    ghcp_response_json = json.dumps(ghcp_response)
    return ghcp_response_json