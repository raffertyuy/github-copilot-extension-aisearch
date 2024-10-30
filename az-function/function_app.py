import azure.functions as func
import logging
import requests
import json

from copilot_response import create_text_event, create_done_event

# Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name(name="EchoMessage")
@app.route(route="", methods=["POST"])
def EchoMessage(req):
    logging.info('Python HTTP trigger function processed a request.')
    
    username = "user"
    token_for_user = req.headers.get("X-GitHub-Token")
    
    if token_for_user:
        headers = {
            "Authorization": f"token {token_for_user}",
            "Accept": "application/vnd.github.v3+json"
        }
        try:
            user_response = requests.get("https://api.github.com/user", headers=headers)
            user_response.raise_for_status()
            user_data = user_response.json()
            username = user_data["login"]
        except requests.exceptions.RequestException as error:
            print(f"Error fetching user: {error}")

    payload = req.get_json()
    print("Payload:", payload)

    messages = payload.get("messages", [])
    last_message = messages[-1]["content"] if messages else ""

    new_message = f"Hello, {username}! You said: \"{last_message}\""
    print("Response:", new_message)

    response = {
        "body": create_text_event(new_message) + create_done_event()
    }
    
    response_json = json.dumps(response)
    return response_json