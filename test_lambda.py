import json

from lambda_function import lambda_handler

if __name__ == "__main__":

    # Simulate an HTTP request with a JSON body
    event = {
        "body": json.dumps({
            "mode": "week"
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }

    response = lambda_handler(event, None)
    print(response)