import json

class ErrorResponseBuilder:
    def __init__(self, execution_id: str) -> None:
        self.execution_id = execution_id

    def format_error_response(self, statusCode: int, message: str):
        return {
            "execution_id": self.execution_id,
            "statusCode": statusCode,
            "body": json.dumps({
                "error": message
            })
        }
