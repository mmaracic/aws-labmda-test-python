import json
import logging
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def lambda_handler(event: dict, context) -> dict:
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    logger.info("Received event: %s", json.dumps(event))
    ip = None
    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        logger.error("Error fetching IP address: %s", e)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "location": ip.text.replace("\n", "") if ip else "Unavailable",
            "event": json.dumps(event),
        }),
    }
