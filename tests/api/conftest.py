import pytest
from dotenv import load_dotenv
import os
import allure

load_dotenv()

@pytest.fixture(scope="session")
def api_base_url():
    return "https://reqres.in/api"

@pytest.fixture
def api_headers():
    api_key = os.getenv("REQRES_API_KEY")
    
    if api_key:
        api_key = api_key.replace("'", "").replace('"', '').strip()
        
    return {
        "x-api-key": api_key
    }