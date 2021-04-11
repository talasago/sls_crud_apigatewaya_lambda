import json


def updates(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed PUT method successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
