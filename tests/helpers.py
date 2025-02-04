from typing import Any
from httpx import AsyncClient
import logging


logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")

async def validate_invalid_parameter(
    data: dict,
    parameter_name: str,
    parameter_value: Any,
    test_client: AsyncClient,
    method: str,
    url: str,
    expected_error_message: str,
    expected_error_code: int,
    path_parameter: Any = None,
    expected_error_type: str | None = None,
    
):
    method_map = {
        "post": test_client.post,
        "patch": lambda u, j: test_client.patch(f'{u}/{path_parameter}', json=j)
    }

    
    data[parameter_name] = parameter_value
    response = await method_map[method](url, json=data)
    
    logging.debug(f"Request {method.upper()} {url} with {data}")
    logging.debug(f"Response: {response.status_code} - {response.json()}")

    
    if expected_error_type == None:
        error = response.json()["detail"]
        assert response.status_code == expected_error_code
        assert error == expected_error_message
        
    
    else:
        error = response.json()["detail"][0]
        assert response.status_code == expected_error_code 
        assert error["type"] == expected_error_type
        assert error["msg"] == expected_error_message
    
