import json
import base64
import os
import logging
import requests
import hmac
import hashlib
import yaml
import boto3

from libraries.api import API

docs_url = "http://api.colourbox.com/docs-internal.yml"

def get_api_credentials():
    ssm_client = boto3.client('ssm')
    key = ssm_client.get_parameter(
            Name='/config/api/root/key', WithDecryption=True)['Parameter']['Value']
    print("FOUND KEY")
    secret = ssm_client.get_parameter(
            Name='/config/api/root/secret', WithDecryption=True)['Parameter']['Value']
    print("FOUND SECRET")
    return (key, secret)

def lambda_handler(event, context):
    key, secret = get_api_credentials()
    api = API(key, secret, base_url = docs_url)
    print("initialized client")
    auth_str = api.get_authorization_header(key, secret)
    headers = {'Authorization': auth_str}
    print("ABOUT TO SEND REQUEST")
    r = requests.get(docs_url, headers=headers)
    print("REQUEST RETURNED")
    r.raise_for_status()
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
