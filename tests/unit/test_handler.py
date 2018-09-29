import json
import pytest
from src import app


def apigw_slack_base_event():
    """ Generates a fake slack challenge event.

    This is the base event and has no body. So you should add
    to whatever you need based on what you need the anything else to be.
    """

    return {'resource': '/slack',
            'path': '/slack',
            'httpMethod': 'POST',
            'headers': {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip,deflate',
                'Content-Type': 'application/json',
                'Host': '<OBSFUCATED>',
                'User-Agent': 'Slackbot 1.0 (+https://api.slack.com/robots)',
                'X-Forwarded-For': '34.226.200.251', 'X-Forwarded-Port': '443',
                'X-Forwarded-Proto': 'https',
                'X-Slack-Request-Timestamp': '<OBSFUCATED>',
                'X-Slack-Signature': '<OBSFUCATED>'
            },
            'multiValueHeaders': {
                'Accept': ['*/*'],
                'Accept-Encoding': ['gzip,deflate'],
                'Content-Type': ['application/json'],
                'Host': ['<OBSFUCATED>'],
                'User-Agent': ['Slackbot 1.0 (+ht tps://api.slack.com/robots)'],
                'X-Amzn-Trace-Id': ['<OBSFUCATED>'],
                'X-Forwarded-For': ['<OBSFUCATED>'],
                'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https'],
                'X-Slack-Request-Timestamp': ['<OBSFUCATED>'],
                'X-Slack-Signature': ['<OBSFUCATED>']
            },
            'queryStringParameters': None,
            'multiValueQueryStringParameters': None,
            'pathParameters': None,
            'stageVariables': {'Stage': '<OBSFUCATED>',
                               'ApiLambdaFunction': '<OBSFUCATED>'},
            'requestContext': {'resourceId': 'o17wi2', 'resourcePath': '/slack', 'httpMethod': 'POST',
                               'extendedRequestId': 'N5lBUHOoywMFXFg=', 'requestTime': '<OBSFUCATED>',
                               'path': '<OBSFUCATED>', 'accountId': '<OBSFUCATED>', 'protocol': 'HTTP/1.1',
                               'stage': '<OBSFUCATED>', 'requestTimeEpoch': 1538084565280,
                               'requestId': '<OBSFUCATED>',
                               'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None,
                                            'caller': None, 'sourceIp': '<OBSFUCATED>', 'accessKey': None,
                                            'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None,
                                            'userArn': None,
                                            'userAgent': 'Slackbot 1.0 (+https://api.slack.com/robots)', 'user': None},
                               'apiId': '<OBSFUCATED>'},
            'isBase64Encoded': False}


@pytest.fixture()
def apigw_slack_challenge_event():
    """Forms a basic slack challenge event.
    """
    slack_challenge_event = apigw_slack_base_event()
    slack_challenge_event["body"] = '{"token":"<OBSFUCATED>","challenge":"somerandomdigits","type":"url_verification"}'
    return slack_challenge_event


def test_lambda_handler(apigw_slack_challenge_event):
    ret = app.lambda_handler(apigw_slack_challenge_event, "")
    assert ret['statusCode'] == 200

    data = json.loads(ret['body'])
    assert data == {"challenge": "somerandomdigits"}
