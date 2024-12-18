# main.py
import os
import json
import functions_framework
import logging
from slack_sdk.webhook import WebhookClient
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.http
def contact_me(request):
    """HTTP Cloud Function that sends notifications to Slack.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
    """
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}

    try:
        if request.method != "POST":
            raise ValueError(f"Unsupported method: {request.method}")

        request_json = request.get_json()
        logger.info(f"Received request with payload: {request_json}")

        if not request_json:
            raise ValueError("No JSON payload received")

        # Validate required fields
        required_fields = ["name", "email", "message"]
        for field in required_fields:
            if field not in request_json:
                raise ValueError(f"Missing required field: {field}")

        name = request_json["name"]
        email = request_json["email"]
        message = request_json["message"]

        # Get webhook URL from environment variable
        webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
        if not webhook_url:
            logger.error("SLACK_WEBHOOK_URL environment variable not set")
            raise ValueError("SLACK_WEBHOOK_URL environment variable not set")

        webhook = WebhookClient(webhook_url)
        logger.info("Initialized Slack webhook client")

        # Format the message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slack_message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "New Message Received! 📬",
                        "emoji": True,
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*From:*\n{name}"},
                        {"type": "mrkdwn", "text": f"*Email:*\n{email}"},
                    ],
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Message:*\n{message}"},
                },
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": f"Received at: {timestamp}"}
                    ],
                },
            ]
        }

        # Send the message
        logger.info("Sending message to Slack")
        response = webhook.send_dict(slack_message)

        if response.status_code != 200:
            error_msg = f"Failed to send message to Slack: {response.body}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info("Successfully sent message to Slack")
        return (
            {"success": True, "message": "Notification sent to Slack"},
            200,
            headers,
        )

    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return ({"success": False, "error": str(e)}, 400, headers)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return (
            {"success": False, "error": f"Internal server error: {str(e)}"},
            500,
            headers,
        )
