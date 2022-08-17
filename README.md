# Photobot Index

A Lambda function that indexes photos for the Photobot app, created in the final project of CS-GY 9223 at NYU.

The Lambda function is invoked via an S3 event trigger whenever the user uploads a new picture. This function asks Rekognition for labels of image content, and stores those labels, along with any user-provided labels, in an OpenSearch index.

## Development

Make changes to `index.py`. 

`test_lambda.py` is provided as a convenient way to execute your Lambda handler locally.

`.env.template` shows the expected environment variables.

## Deployment

This app is deployed to Lambda through a CodePipeline pipeline defined in https://github.com/wdickerson/csgy-9223-photobot-infrastructure. Any modification to the `main` branch results in a new deployment.
