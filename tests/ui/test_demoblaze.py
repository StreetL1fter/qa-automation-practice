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


def check_user_orders_in_db(username,db_connection):
    cursor = db_connection.cursor()
    query = '''
        SELECT test_users.login, orders.item_name, orders.price 
        FROM orders
        INNER JOIN test_users ON orders.user_id = test_users.id
        WHERE test_users.login = ?
    '''
    cursor.execute(query, (username,))
    result = cursor.fetchall() # Получаем все заказы пользователя
    return result


@allure.feature("Корзина и База Данных")
@allure.story("Интеграционный сценарий покупки товара с валидацией в реляционной БД")
@pytest.mark.regression
def test_user_purchase_with_db_validation(page, demo_page, db_connection):
    test_user = "ismail_test"
    test_password = "SecretPassword123"
    product_name = "Samsung galaxy s6"
    product_price = 360.0

    with allure.step("Регистрация пользователя на реальном сайте Demoblaze"):
        # Открываем сайт
        page.goto("https://www.demoblaze.com/")
        
        # Кликаем "Sign up", вводим данные и регистрируем
        page.locator("#signin2").click()
        page.locator("#sign-username").fill(test_user)
        page.locator("#sign-password").fill(test_password)
        
        # Перехватываем алерт об успешной регистрации ("Sign up successful.")
        page.once("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name="Sign up").click()
        page.wait_for_timeout(1000) # Даем секунду серверу

    with allure.step("Авторизация пользователя на UI платформы Demoblaze"):
        page.goto(demo_page.URL if hasattr(demo_page, 'URL') else "https://www.demoblaze.com/")
        # Проходим авторизацию под существующим в БД пользователем
        demo_page.login(test_user, test_password, expect_success=True)

    with allure.step(f"Имитация добавления товара '{product_name}' в корзину"):
        demo_page.add_product_to_cart(product_name)

    with allure.step("Эмуляция транзакции: запись совершенного заказа в таблицу 'orders'"):
        cursor = db_connection.cursor()
        
        # Сначала получаем динамический id пользователя из таблицы test_users
        cursor.execute("SELECT id FROM test_users WHERE login = ?", (test_user,))
        user_row = cursor.fetchone()
        user_id = user_row["id"]
        
        # Записываем заказ, жестко привязывая его к Foreign Key (user_id) нашего юзера
        cursor.execute(
            "INSERT INTO orders (item_name, price, user_id) VALUES (?, ?, ?)",
            (product_name, product_price, user_id)
        )
        db_connection.commit()

    with allure.step("Валидация данных: проверка связки таблиц 'test_users' и 'orders' через INNER JOIN"):
        orders_in_db = check_user_orders_in_db(test_user, db_connection)
        
        # Проверяем, что вернулся ровно 1 заказ
        assert len(orders_in_db) == 1, f"Ожидался 1 заказ в БД для {test_user}, но найдено {len(orders_in_db)}"
        
        # Проверяем корректность данных в строке (благодаря sqlite3.Row обращаемся по именам колонок)
        assert orders_in_db[0]["item_name"] == product_name, \
            f"Ожидался товар {product_name}, но в базе записан {orders_in_db[0]['item_name']}"
            
        assert orders_in_db[0]["price"] == product_price, \
            f"Ожидалась цена {product_price}, но в базе записана {orders_in_db[0]['price']}"
            
        assert orders_in_db[0]["login"] == test_user, \
            f"Заказ привязался к пользователю {orders_in_db[0]['login']}, а должен был к {test_user}"