from playwright.sync_api import Page
import allure

class Elements:
    URL = "https://demoqa.com/automation-practice-form"
    INPUT_FIRST_NAME = "#firstName"
    INPUT_LAST_NAME = "#lastName"
    INPUT_EMAIL = "#userEmail"
    INPUT_PHONE = "#userNumber"
    RADIO_GENDER_MALE = 'label[for="gender-radio-1"]'
    BTN_SUBMIT = "#submit"
    MODAL_CONTENT = ".modal-content"
    MODAL_BODY = ".modal-body"
  

    def __init__(self,page:Page):
        self.page = page
    
    @allure.step("Открываю страницу")
    def open(self):
        self.page.goto(self.URL)
        self.page.wait_for_selector(self.INPUT_FIRST_NAME,state="visible")
        return self
    @allure.step("Заполняю форму имя {first_name}, фамилия {last_name}")
    def fill_form(self,first_name:str,last_name:str,email:str,phone:str):
        self.page.fill(self.INPUT_FIRST_NAME,first_name)
        self.page.fill(self.INPUT_LAST_NAME,last_name)
        self.page.fill(self.INPUT_EMAIL,email)
        self.page.fill(self.INPUT_PHONE,phone)
        return self
    
    def select_gender(self):
        self.page.locator(self.RADIO_GENDER_MALE).click()
        return self
    

    def get_error_message(self):
        return self.page.locator(self.INPUT_EMAIL).evaluate("node => node.validationMessage")

    def submit_form(self):
        self.page.locator(self.BTN_SUBMIT).click()
        return self
    
    def is_success_modal_visible(self):
        return self.page.locator(self.MODAL_BODY).is_visible()
        

    
        

