import json, os, boto3, requests
from sign import get_signed_headers

s3_client = boto3.client('s3')


# def sign(key, msg):
#     return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

# def getSignatureKey(key, dateStamp, regionName, serviceName):
#     kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
#     kRegion = sign(kDate, regionName)
#     kService = sign(kRegion, serviceName)
#     kSigning = sign(kService, 'aws4_request')
#     return kSigning

def lambda_handler(event, context):
    # ************* BUILD ENDPOINT AND PAYLOAD *************
    s3_bucket = event.get('Records', [])[0].get('s3', {}).get('bucket', {}).get('name', None)
    s3_key = event.get('Records', [])[0].get('s3', {}).get('object', {}).get('key', None)
    metadata = s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
    s3_custom_labels = metadata.get('Metadata', {}).get('customlabels', '').split(',')
    payload = {
        "labels" : s3_custom_labels
    }
    endpoint = f"https://{os.environ['OPENSEARCH_ENDPOINT']}/photos/_doc/{s3_key}"

    # ************* REQUEST VALUES *************
    # method = 'PUT'
    # service = 'es'
    # host = os.environ['OPENSEARCH_ENDPOINT']
    # region = 'us-east-1'

    

    # request_parameters = ''
    # credentials = boto3.Session().get_credentials()

    # t = datetime.datetime.utcnow()
    # amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    # datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
    # canonical_uri = f"/photos/_doc/{s3_key}"
    # canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
    # signed_headers = 'host;x-amz-date'
    # payload_hash = hashlib.sha256((json.dumps(payload)).encode('utf-8')).hexdigest()
    # canonical_request = method + '\n' + canonical_uri + '\n' + request_parameters + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    # canonical_request = method + '\n' + canonical_uri + '\n' + request_parameters + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    # algorithm = 'AWS4-HMAC-SHA256'
    # credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
    # string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    # signing_key = getSignatureKey(credentials.secret_key, datestamp, region, service)
    # signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
    # authorization_header = algorithm + ' ' + 'Credential=' + credentials.access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    # headers = {
    #     'Content-Type': 'application/json',
    #     'x-amz-date': amzdate,
    #     'x-amz-security-token': credentials.token,
    #     'Authorization': authorization_header
    # }

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
    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": '*' },
        "body": r.text,
    }
