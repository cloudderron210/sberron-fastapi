from typing import Any
from httpx import AsyncClient
import logging



async def validate_invalid_parameter(
    data: dict,
    parameter_name: str,
    parameter_value: Any,
    test_client: AsyncClient,
    method: str,
    url: str,
    expected_error_message: str,
    expected_error_code: int,
    expected_error_type: str,
    path_parameter: Any = None,
    
):
    method_map = {
        "post": test_client.post,
        "patch": lambda u, j: test_client.patch(f'{u}/{path_parameter}', json=j)
    }

    
    data[parameter_name] = parameter_value
    response = await method_map[method](url, json=data)
    
    logging.error(f"Request {method.upper()} {url} with {data}\n expected_error_code: {expected_error_code} - expected_error_type: {expected_error_type} - expected_error_message: {expected_error_message} - ")
    logging.error(f"Response: {response.status_code} - {response.json()}")
    
    error = response.json()["detail"][0]
    assert response.status_code == expected_error_code 
    assert error["type"] == expected_error_type
    assert expected_error_message in error["msg"] 
    
