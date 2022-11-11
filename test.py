import json

import handler

class MockLambdaContext:
    def __init__(self, aws_request_id: str) -> None:
        self.aws_request_id = aws_request_id

if __name__ == "__main__":
    req = {
        "model": "CMUDict",
        "N": 6,
        "M": 10
    }

    res = handler.handler({
        "body": json.dumps(req)
        }, MockLambdaContext(aws_request_id="abcd1234"))
    print(res)
