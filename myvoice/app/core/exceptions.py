"""Custom exception classes and global error response format."""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


# ---------------------------------------------------------------------------
# Custom exception classes
# ---------------------------------------------------------------------------

class NotFoundError(HTTPException):
    def __init__(self, entity: str, entity_id: str):
        super().__init__(status_code=404, detail=f"{entity} with id '{entity_id}' not found")


class ConflictError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)


class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "Access denied"):
        super().__init__(status_code=403, detail=detail)


class AuthError(HTTPException):
    """Authentication failure (401)."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=401, detail=detail)


class ValidationError(HTTPException):
    """Business-level validation failure (422)."""
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class ExternalServiceError(HTTPException):
    """Upstream service (OpenAI, etc.) returned an error (502)."""
    def __init__(self, service: str, detail: str = ""):
        message = f"External service error: {service}"
        if detail:
            message = f"{message} — {detail}"
        super().__init__(status_code=502, detail=message)


# ---------------------------------------------------------------------------
# Standard error response format
# {"error": {"code": "...", "message": "...", "detail": ...}}
# ---------------------------------------------------------------------------

def _make_error_body(code: str, message: str, detail=None) -> dict:
    payload: dict = {"code": code, "message": message}
    if detail is not None:
        payload["detail"] = detail
    return {"error": payload}


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    status = exc.status_code
    detail = exc.detail

    # Map status code to a short error code string
    _code_map = {
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "validation_error",
        429: "rate_limit_exceeded",
        500: "internal_error",
        502: "external_service_error",
    }
    code = _code_map.get(status, f"error_{status}")

    if isinstance(detail, str):
        body = _make_error_body(code, detail)
    elif isinstance(detail, dict):
        body = _make_error_body(code, detail.get("message", str(detail)), detail)
    else:
        body = _make_error_body(code, str(detail))

    return JSONResponse(status_code=status, content=body)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    import logging
    logging.getLogger(__name__).exception("Unhandled exception")
    body = _make_error_body("internal_error", "An unexpected error occurred")
    return JSONResponse(status_code=500, content=body)
