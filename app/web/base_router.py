from fastapi import APIRouter

class WebRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(
            tags=["Web"],
            responses={
                404: {"description": "Endpoint not found"},
                403: {"description": "Forbidden access"},
                200: {"description": "Success response"},
                400: {"description": "Bad Request"},
                401: {"description": "Unauthorized access"}
            },
            *args, 
            **kwargs
        )