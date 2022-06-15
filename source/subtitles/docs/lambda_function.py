import json
import base64
import boto3
import os
import logging
import requests
import hmac
import hashlib
import yaml

from libraries.api import API

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_api_credentials():
    ssm_client = boto3.client('ssm')
    key = ssm_client.get_parameter(
            Name='/config/api/root/key', WithDecryption=True)['Parameter']['Value']
    logger.info("FOUND KEY")
    secret = ssm_client.get_parameter(
            Name='/config/api/root/secret', WithDecryption=True)['Parameter']['Value']
    logger.info("FOUND SECRET")
    return (key, secret)

def lambda_handler(event, context):
    logger.info("ARE WE EVEN HERE?!")
    docs_url = os.environ.get('API_URL')
    key, secret = get_api_credentials()
    api = API(key, secret, base_url = docs_url)
    logger.info("initialized client")
    auth_str = api.get_authorization_header(key, secret)
    headers = {'Authorization': auth_str}
    logger.info("ABOUT TO SEND REQUEST")
    r = requests.get(docs_url)
    logger.info("REQUEST RETURNED")
    r.raise_for_status()
    logger.info("RAISED FOR STATUS, NOW RETURNING")
    return {
            "statusCode": 200,
            "body": r.text,
            "headers": {
                'Content-Type': 'application/x-yaml',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': "GET",
                'Access-Control-Allow-Headers': "Content-type, api_key, Authorization",
                },
            }
