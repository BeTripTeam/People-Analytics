from bottle import HTTPResponse
from json import dumps


class ResponseBuilder:
    @staticmethod
    def buildErrorResponse(e: Exception):
        msg = "Wrong action exception. Check params and token expire date, please."
        body = {
            "code": 500,
            "message": msg
        }
        try:
            body['message'] = e.args[0].message
        except:
            body["message"] = msg
            
        return HTTPResponse(status=500, body=body, headers={'content_type': 'application/json'})
    
    @staticmethod
    def buildSuccessResponse(body):
        try:
            body = dumps(body)
            return HTTPResponse(status=200, body=body, headers={'content_type': 'application/json'})
        except Exception as e:
            return ResponseBuilder.buildErrorResponse(Exception("Internal Server Error"))
