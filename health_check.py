import json
import os
import boto3

def lambda_handler(event, context):
    table_name = os.environ.get("TABLE_NAME", "ITHelpDeskTickets")
    dynamodb = boto3.client("dynamodb")
    try:
        dynamodb.describe_table(TableName=table_name)
        return {"statusCode": 200, "body": json.dumps({"status": "healthy", "table": table_name})}
    except Exception as exc:
        return {"statusCode": 503, "body": json.dumps({"status": "unhealthy", "error": str(exc)})}
