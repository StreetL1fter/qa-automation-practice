import allure
import pytest
import random
import allure

@pytest.mark.smoke
@pytest.mark.regression
def test_full_user_lifecycle(demo_page, db_connection):
    unique_id = random.randint(100, 999)
    test_user = f"ismail_{unique_id}"
    test_pass = "Pass12345"
    
    demo_page.open()
    demo_page.register(test_user, test_pass)
    
    cursor = db_connection.cursor()
    cursor.execute(
        "INSERT INTO test_users (login, password, status) VALUES (?, ?, ?)",
        (test_user, test_pass, "active")
    )
    db_connection.commit()

    user_from_db = cursor.execute(
        "SELECT login, password FROM test_users WHERE login = ?", (test_user,)
    ).fetchone()
    
    demo_page.page.reload()
    demo_page.login(user_from_db['login'], user_from_db['password'])

    actual_name = demo_page.get_logged_user_name()
    assert user_from_db['login'] in actual_name

@pytest.mark.regression
def test_login_banned_user(demo_page, db_connection):
    cursor = db_connection.cursor()
    user_banned = cursor.execute(
        "SELECT login, password FROM test_users WHERE status = 'banned'"
    ).fetchone()

    demo_page.open()
    demo_page.login(user_banned['login'], user_banned['password'], expect_success=False)
    assert demo_page.page.is_visible("#login2")


