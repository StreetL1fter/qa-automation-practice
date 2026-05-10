import pytest
from playwright.sync_api import Browser, BrowserContext,sync_playwright
from pages.elements_page import Elements
from pages.cataloge_page import Catalog
import allure


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                 "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox"
            ]
        )
        yield browser
        browser.close()


##################Создание агента

@pytest.fixture
def context(browser: Browser):
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        viewport={"width": 1440, "height": 900}

    )
    yield context
    context.close()

@pytest.fixture
def page(context: BrowserContext):
    page = context.new_page()
    page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })""")
    yield page
########################

@pytest.fixture
def registration_page(page):
    reg_page = Elements(page)
    allure.attach(
        page.screenshot(),
        name="screenshot",
        attachment_type=allure.attachment_type.PNG
    )
    return reg_page

@pytest.fixture
def cataloge_page(page):
    catalog_page = Catalog(page)
    allure.attach(
        page.screenshot(),
        name="screenshot",
        attachment_type=allure.attachment_type.PNG
    ) 
    return catalog_page