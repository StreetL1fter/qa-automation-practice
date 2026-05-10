import pytest
from dotenv import load_dotenv
import os
import allure

load_dotenv()

@pytest.fixture(scope="function")
def base_url():
    return "https://reqres.in/api"

@pytest.fixture
def api_headers():
    return {
        "x-api-key": os.getenv("REQRES_API_KEY")
    }


