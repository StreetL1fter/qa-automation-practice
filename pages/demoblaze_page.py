import allure

class DemoblazePage:
    def __init__(self, page):
        self.page = page
        self.login_menu_button = "#login2"
        self.login_username_field = "#loginusername"
        self.login_password_field = "#loginpassword"
        self.login_submit_button = "#logInModal .btn-primary"
        self.name_user_display = "#nameofuser"

    @allure.step("Открыть главную страницу Demoblaze")
    def open(self):
        self.page.goto("https://www.demoblaze.com/")

    @allure.step("Зарегистрировать нового пользователя {username}")
    def register(self, username, password):
        self.page.click("#signin2") # Кнопка Sign up
        self.page.fill("#sign-username", username)
        self.page.fill("#sign-password", password)
        
        self.page.click("button[onclick='register()']")
        self.page.wait_for_timeout(2000)


    @allure.step("Авторизоваться под пользователем {username}")
    def login(self, username, password,expect_success=True):
        self.page.click(self.login_menu_button)
        self.page.wait_for_selector(self.login_username_field, state="visible")
        self.page.fill(self.login_username_field, username)
        self.page.fill(self.login_password_field, password)
        self.page.wait_for_timeout(500)
        self.page.click(self.login_submit_button)
        if expect_success:
            self.page.wait_for_selector(self.name_user_display, state="visible", timeout=5000)
        else:
            self.page.wait_for_timeout(1000)

    @allure.step("Получить имя авторизованного пользователя")
    def get_logged_user_name(self):
        return self.page.locator(self.name_user_display).text_content()