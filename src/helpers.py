import boto3
import logging
import json
import urllib

# Set up logging here
LOGGER = logging.getLogger(__name__)

# Define the URL of the targeted Slack API resource.
SLACK_URL = "https://slack.com/api/chat.postMessage"


def get_secrets(secret_name: str) -> str:
    """Gets values from secrets manager

    Args:
        secret_name (str): The secrets name

    Returns:
        A string of the secrets in secrets manager. You will need to jsonify it if its in json.
    """
    client = boto3.client(
        service_name='secretsmanager'
    )
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    return get_secret_value_response['SecretString']


def form_response(status_code: int, body: dict):
    """Generates a JSON response

    Args:
        status_code (int): A integer of the applicable status code
        body (dict): A dictionary to send as a response.

    Returns:
        A properly formed response
    """
    return {
        "isBase64Encoded": True,
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def send_slack_request(data: dict, bot_token: str, request_method: str= "POST"):
    """ Sends a request to the slack API. This sends it manually using urllib but you should use the slack
    client defined in the app.py.

    Args:
        data: A dictionary of the json data you would like to send
        bot_token: The secret bot token that authroizes the app to send it as that bot
        request_method: The request method. Default: POST
    """

    # First dump the data into a string and encode it as bytes as this is necessary
    data = json.dumps(data).encode('utf-8')

    # Add headers specifying that we are sending a JSON response
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {bot_token}"
    }

    # Construct the HTTP request that will be sent to the Slack API.
    request = urllib.request.Request(
        SLACK_URL,
        data=data,
        method=request_method,
        headers=headers
    )

    # Fire off the request!
    urllib.request.urlopen(request).read()
    return
