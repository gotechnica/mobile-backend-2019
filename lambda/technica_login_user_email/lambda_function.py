import random
import boto3
import time
from boto3.dynamodb.conditions import Key, Attr
import json


def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('Technica-Data')
    response = table.scan(FilterExpression=Attr('email').eq(event['email']))
    data = {'user_data': {}}
    if len(response[u'Items']) <= 0:
        raise Exception('Error. Invalid input: Email is Invalid.')
    for item in response[u'Items'][0]:
        if item == u'fav_events':
            data['user_data']['fav_events'] = {}
            for event in response[u'Items'][0][item]:
                data['user_data']['fav_events'][str(event)] = True
        elif item == u'minor_status':
            data['user_data']['minor_status'] = response[u'Items'][0][item]
        elif item == u'organizer':
            data['user_data']['organizer'] = response[u'Items'][0][item]
        elif item == u'dietary_restrictions':
            data['user_data']['dietary_restrictions'] = []
            for restriction in response[u'Items'][0][item]:
                data['user_data']['dietary_restrictions'].append(
                    str(restriction))
        else:
            data['user_data'][item] = str(response[u'Items'][0][item])
    response = table.update_item(
        Key={
            'email': response[u'Items'][0][u'email']
        },
        UpdateExpression='SET checked_in = :checked_in',
        ExpressionAttributeValues={
            ':checked_in': True,
        }
    )
    return {"statusCode": 200, "body": data}
