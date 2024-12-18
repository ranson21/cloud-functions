import os
import json
import functions_framework
import logging
from slack_sdk.webhook import WebhookClient
from datetime import datetime
from google.cloud import secretmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def access_secret_version(project_id, secret_id, version_id="latest"):
    """
    Access the secret version from Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


@functions_framework.http
def handle_request(request):
    """HTTP Cloud Function that handles both health checks and Slack notifications.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
    """
    # Add health check endpoint
    if request.method == "GET" and request.path == "/health":
        return ({"status": "healthy"}, 200, {"Access-Control-Allow-Origin": "*"})

    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
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

        # Get webhook URL from Secret Manager
        project_id = os.environ.get("GCP_PROJECT")
        webhook_url = access_secret_version(project_id, "slack_webhook_url")
        logger.info("Retrieved webhook URL from Secret Manager")

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
