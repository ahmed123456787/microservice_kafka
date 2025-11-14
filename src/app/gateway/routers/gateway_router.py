from config.settings import BaseSettings
from fastapi import APIRouter, HTTPException, Request
from utils.http_client import proxy_request

router = APIRouter()
settings = BaseSettings()

@router.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def gateway_proxy(service: str,path: str, request: Request):

    if service not in settings.service_mapping:
        raise HTTPException(status_code=404, detail="Service not found")

    service_obj = settings.service_mapping[service]

    target_url = f"{service_obj.url}/{path}"

    # 4. Extract request body if needed
    body = await request.json() if request.method in ["POST", "PUT"] else None

    # 5. Proxy the request
    response = await proxy_request(
        method=request.method,
        url=target_url,
        body=body,
        headers=request.headers
    )

    return response.json()