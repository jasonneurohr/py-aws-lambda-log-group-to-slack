import json
import logging
from base64 import b64decode
from gzip import decompress
from io import StringIO
from os import getenv

import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def event_decoder(event):
    logger.debug(f"Decoding event")

    event_data = event["awslogs"]["data"]
    cwl_compressed_payload = b64decode(event_data)
    cwl_uncompressed_payload = decompress(cwl_compressed_payload)
    cwl_payload = json.loads(cwl_uncompressed_payload)

    return cwl_payload


def send_notification(message, category):
    slack_uri = getenv("SLACK_WEBHOOK")

    # For reference - https://api.slack.com/docs/message-attachments
    attachment = dict(
        {
            "attachments": [
                {
                    "title": f"CloudWatch Log Alarm: {category.upper()}",
                    "text": message,
                    "color": "danger",
                }
            ]
        }
    )

    req_data = json.dumps(attachment)

    req_headers = {"Content-type": "application/json"}
    req = requests.post(url=slack_uri, headers=req_headers, data=req_data)


def lambda_handler(event, context):
    logger.info(f"lambda_handler entered")
    logger.debug(f"Log Stream Name: {context.log_stream_name}")
    logger.debug(f"Log Group Name: {context.log_group_name}")
    logger.debug(f"Log Events: {json.dumps(event)}")

    decoded_event = event_decoder(event)

    logger.debug(f"Decoded: {decoded_event}")

    for event_message in decoded_event["logEvents"]:
        message = event_message["message"]

        if str(message).find("Bad") >= 0:
            send_notification(message, "BAD CONTACT FORM")

        if str(message).find('HTTP/1.1" 418') >= 0:
            send_notification(message, "I'M A TEAPOT")
