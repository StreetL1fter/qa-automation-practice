from playwright.sync_api import sync_playwright
import pytest
import allure

@pytest.mark.parametrize("first_name,last_name,email,phone",[
     ("Ivan", "Ivanov", "ivan@test.com", "1234567890"),
    ("Anna", "Petrova", "anna@example.com", "0987654321"),
    ("Test", "User", "test@qa.local", "1122334455"),
],ids=["user1","user2","user3"])
def test_registration_form(registration_page,first_name,last_name,email,phone):
    is_visible = registration_page.open()\
    .fill_form(first_name,last_name,email,phone)\
    .select_gender()\
    .submit_form()\
    .is_success_modal_visible()

    assert is_visible
        
@pytest.mark.parametrize("bad_email,error_text",
    [("ivan.com","Please match the requested format."),
     ], ids=["invalid_format"])
def test_email_validate(registration_page,bad_email,error_text):
    registration_page.open()
    registration_page.fill_form("Ivan","Ivanov",bad_email,"1234567890")
    registration_page.select_gender()
    registration_page.submit_form()
    assert registration_page.get_error_message() == error_text
    


@pytest.mark.parametrize("product",["macbook","iphone","ноутбук","борцовки"])
def test_search_input(cataloge_page,product):
    assert_open = cataloge_page.open()
    cataloge_page.search_item(product)
    item_count = cataloge_page.get_product_card(product)
    assert item_count > 0, f"Товаров найден было - {item_count}"


@pytest.mark.parametrize("product",["Xiaomi","Iphone"])
def test_basket_item(page,cataloge_page,product):
    page.route("**/*.{css,js,png,jpg,woff,woff2}", lambda route: route.continue_())
    page.route(
        "**/*basket*/**", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            json={
                "data": {
                    "count": 1,
                    "basket": {"value": 1}
                }
            }
        )
    )
    cataloge_page.open()
    cataloge_page.search_item(product)
    cataloge_page.add_first_item_to_basket()
    count = cataloge_page.get_basket_count()
    allure.dynamic.description(f"Проверка добавления {product}. Получено товаров: {count}")
    assert count == "1", f"Ожидали 1 товар в корзине, но получили {count}"



