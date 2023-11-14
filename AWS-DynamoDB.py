import boto3
from pprint import pprint
from botocore.exceptions import ClientError
from decimal import Decimal


ACCESS_KEY = "AKIAV6MB************"
SECRET_KEY = "vaGNEXitEeqqt1C63****************"

client = boto3.client(
    'dynamodb',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

sts = boto3.client('sts')

try:
    response = sts.get_caller_identity()
    print("Caller identity:", response)
except Exception as e:
    print("Error:", e)


#create DynamoDb table
def create_table():
    table = client.create_table(
        TableName = 'Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

## Create a record in table Movie
def put_movie(title, year, plot, rating, like_dislike):
    response = client.put_item(
        TableName='Movies',
        Item={
            'year': {
                'N': "{}".format(year)
            },
            'title': {
                'S': "{}".format(title)
            },
            'plot': {
                "S": "{}".format(plot),
            },
            'rating': {
                "N": "{}".format(rating),
            },
            'like_dislike': {
                "S": "{}".format(like_dislike),
            }
        }
    )
    return response

def get_movie(title, year):
    try:
        response = client.get_item(       
                TableName='Movies',
                Key={
                        'year': {
                                'N': "{}".format(year),
                        },
                        'title': {
                                'S': "{}".format(title),
                        }
                    }
                )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']
    
def delete_underrated_movie(title, year, rating):
    try:
        response = client.delete_item(
            TableName = 'Movies',
            Key={
                'year': {
                    'N': "{}".format(year)
                },
                'title': {
                    'S': "{}".format(title)
                }
            },
            ConditionExpression = "rating <= :a",
            ExpressionAttributeValues = {
                ':a': {
                    'N': "{}".format(rating)
                }
            }
            
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

def update_movie_record(title, year, rating, plot, actors):
    response = client.update_item(
        TableName='Movies',
        Key={
            'year': {
                    'N': "{}".format(year),
            },
            'title': {
                    'S': "{}".format(title),
            }
        },
        ExpressionAttributeNames={
            '#R': 'rating',
            '#P': 'plot',
            '#A': 'actors'
        },
        ExpressionAttributeValues={
            ':r': {
                'N': "{}".format(rating),
            },
            ':p': {
                'S': "{}".format(plot),
            },
            ':a': {
                'SS': actors,
            }
        },
        UpdateExpression='SET #R = :r, #P = :p, #A = :a',
        ReturnValues="UPDATED_NEW"
    )
    return response

## Increment an Atomic Counter in DynamoDB table
def increase_rating(title, year, rating_increase):
    response = client.update_item(
        TableName='Movies',
        Key={
            'year': {
                    'N': "{}".format(year),
            },
            'title': {
                    'S': "{}".format(title),
            }
        },
        ExpressionAttributeNames={
            '#R': 'rating'
        },
        ExpressionAttributeValues={
            ':r': {
                'N': "{}".format(Decimal(rating_increase)),
            }
        },
        UpdateExpression='SET #R = #R + :r',
        ReturnValues="UPDATED_NEW"
    )
    return response


if __name__ == "__main__":
    
    ## Create DynamoDB table
    movie_table = create_table()
    print("Dynamodb Table created...")
    print("Table status: {}".format(movie_table))
    
    ## Insert in DynamoDB
    add_movie = put_movie("Pathan", 2023, "nothing", 3, "dislike")
    print("Record is inserted...........")
    pprint(add_movie) 
    
    ## Get an item from DynamoDB
    movie = get_movie("Avengers", 2014,)
    if movie:
       print("Get an item from DynamoDB succeeded............")
       pprint(movie, sort_dicts=False)
    
    ## Delete an item from DynamoDB
    delete_response = delete_underrated_movie("Avengersss", 2014, 5.5)
    if delete_response:
        print("Delete an Item in DynamoDB table.........................")
        pprint(delete_response, sort_dicts=False)
    
    ## Update an item in DynamoDB
    update_response = update_movie_record( "Avengers", 2014, 6.5, "warning.",["RDJ", "Moe", "Curly"])
    print("Update and item in  DynamoDB succeeded............")
    pprint(update_response, sort_dicts=False)
 
    ## Increment an Atomic Counter in DynamoDB
    update_response = increase_rating("Avengers", 2014, 0.5)
    print("Increment an Atomic Counter in DynamoDB succeeded............")
    pprint(update_response, sort_dicts=False)