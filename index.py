import json, os, boto3, requests
from sign import get_signed_headers


s3_client = boto3.client('s3')
rek_client = boto3.client('rekognition')

def lambda_handler(event, context):
    # ************* BUILD ENDPOINT AND PAYLOAD *************
    s3_bucket = event.get('Records', [])[0].get('s3', {}).get('bucket', {}).get('name', None)
    s3_key = event.get('Records', [])[0].get('s3', {}).get('object', {}).get('key', None)
    metadata = s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
    metadata_labels = metadata.get('Metadata', {}).get('customlabels', None)
    s3_custom_labels = [] if metadata_labels is None else metadata_labels.split(',')
    endpoint = f"https://{os.environ['OPENSEARCH_ENDPOINT']}/photos/_doc/{s3_key}"

    rek_response = rek_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': s3_bucket,
                'Name': s3_key,
            }
        },
        MaxLabels=12,
    )

    print('LOG rekognition response:')
    print(json.dumps(rek_response))
    rek_labels = rek_response.get('Labels', []) or []
    rek_label_names = [
        label.get('Name', '')
        for label in rek_labels
    ]

    payload = {
        "labels" : s3_custom_labels + rek_label_names
    }

    # ************* SIGN THE REQUEST *************
    headers = get_signed_headers(
        method='PUT',
        payload=payload,
        service='es',
        host=os.environ['OPENSEARCH_ENDPOINT'],
        canonical_uri=f"/photos/_doc/{s3_key}",
        request_parameters='',
        region = 'us-east-1',
    )

    # ************* SEND THE REQUEST *************
    r = requests.put(endpoint, headers=headers, data=json.dumps(payload))

    # ************* SEND THE RESPONSE *************
    # Primarily for testing, as this us de-coupled from client's request
    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": '*' },
        "body": r.text,
    }
