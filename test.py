import io
import json

from main import publish_birthdays

if __name__ == "__main__":
    from flask import Request

    # Simulate an HTTP request with a JSON body
    request_body = {"mode": "today"}
    mock_request = Request(
        environ={
            "wsgi.input": io.BytesIO(json.dumps(request_body).encode("utf-8")),
            "CONTENT_LENGTH": str(len(json.dumps(request_body))),
            "CONTENT_TYPE": "application/json",
            "REQUEST_METHOD": "POST",
        }
    )

    response = publish_birthdays(mock_request)
