from typing import Any, Dict

from fastapi import HTTPException, status


class HTTPExceptionWithDetail(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, detail: str | None = None, **kwargs: Dict[str, Any]) -> None:
        if detail is not None:
            self.DETAIL = detail

        super().__init__(
            status_code=self.STATUS_CODE,
            detail=self.DETAIL,
            **kwargs,
        )


class BadRequest(HTTPExceptionWithDetail):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class NotAuthenticated(HTTPExceptionWithDetail):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class PermissionDenied(HTTPExceptionWithDetail):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(HTTPExceptionWithDetail):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Not Found"


class AlreadyExists(HTTPExceptionWithDetail):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Already Exists"
