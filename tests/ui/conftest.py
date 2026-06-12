import pytest
from playwright.sync_api import Browser, BrowserContext,sync_playwright
from pages.elements_page import Elements
import sqlite3 as sql
from pages.cataloge_page import Catalog
import allure
import pytest
from pages.demoblaze_page import DemoblazePage
import sqlite3

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            slow_mo=1000,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
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


@pytest.fixture
def db_connection():
    conn = sql.connect("autotest-unit.db")
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS test_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                status TEXT NOT NULL
            )        
    """)
    cursor.execute("DELETE FROM test_users")
    cursor.execute(
        "INSERT INTO test_users (login, password, status) VALUES (?, ?, ?)",
        ("ismail_test", "SecretPassword123", "active")
    )
    cursor.execute(
        "INSERT INTO test_users (login, password, status) VALUES (?, ?, ?)",
        ("banned_user", "WrongPassword", "banned")
    )
    conn.commit()
    yield conn

    conn.close()




#Demoblaze

@pytest.fixture
def demo_page(page):
    return DemoblazePage(page)


@pytest.fixture(scope="function")
def db_connection():
    conn = sqlite3.connect("autotest-unit.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("CREATE TABLE IF NOT EXISTS test_users (id INTEGER PRIMARY KEY, login TEXT, password TEXT, status TEXT)")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES test_users(id) ON DELETE CASCADE
        )
    ''')
    cursor.execute("DELETE FROM test_users")
    cursor.execute("INSERT INTO test_users (login, password, status) VALUES (?, ?, ?)", 
                   ("ismail_test", "SecretPassword123", "active"))
    cursor.execute(
        "INSERT INTO test_users (login, password, status) VALUES (?, ?, ?)",
        ("banned_user", "WrongPassword", "banned")  
    )
    conn.commit()
    yield conn
    conn.close()