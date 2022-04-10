import socket
import uuid

from asgi_correlation_id import CorrelationIdMiddleware
import fastapi
import structlog
import uvicorn

from logapi import logic

logger = structlog.get_logger()
app = fastapi.FastAPI(title="Logging API")
app.add_middleware(CorrelationIdMiddleware)


@app.get("/hello-world/{name}")
def say_hallo(request: fastapi.Request, name: str):
    log = logger.new(
        request_id=str(request.headers.get("X-Request-ID", str(uuid.uuid4()))),
        server=socket.gethostname(),
        route="/hello-world"
    )
    log.info("Endpoint Called", path=request.path_params)
    res = logic.say_hello(name)
    log.info("Return result")
    return res


if __name__ == '__main__':
    structlog.configure(
        context_class=structlog.threadlocal.wrap_dict(dict)
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)
