from index import lambda_handler


my_event = {
    "Records": [
        {
            "s3": {
                "bucket": {
                    "name": "cfy-wad-csgy-9223-photobot-store",
                },
                "object": {
                    "key": "b1849bac-fdbb-4c6b-af1b-1b808226b365",
                }
            }
        }
    ]
}


print('HERE!!! my_event')
print(my_event)

test_response = lambda_handler(my_event, {})
print('HERE!!! test response')
print(test_response)


