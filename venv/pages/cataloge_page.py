from playwright.sync_api import Page
import allure



class Catalog:
    URL = "https://www.wildberries.ru"
    search_id = "#searchInput"
    product_card = ".product-card__wrapper"
    button_basket = "a.j-add-to-basket"
    basket_count = ".navbar-pc__notify"
    button_close = "button.popup__close"

    def __init__(self,page:Page):
        self.page = page


    @allure.step("Открываю страницу")
    def open(self):
        self.page.goto(self.URL)
        try:    
            self.page.locator(self.button_close).click(timeout=6000)
        except:
            pass
        return self
    
    def search_item(self,item_name:str):
        self.page.fill(self.search_id,item_name)
        self.page.locator(self.search_id).press("Enter")
        self.page.wait_for_selector(self.product_card, state="visible", timeout=10000)
        return self

    def get_product_card(self,product_card:str):
        self.page.wait_for_selector(self.product_card)
        count = self.page.locator(self.product_card).count()
        return count
    
    def click_product_card(self):
        self.page.locator(self.product_card).first.click()
        return self

    def add_first_item_to_basket(self):
        first_card = self.page.locator(self.product_card).first
        first_card.scroll_into_view_if_needed()
        first_card.hover()
        add_btn = first_card.locator(self.button_basket)
        add_btn.wait_for(state="visible",timeout=15000)
        add_btn.click(force=True)
        return self

    def get_basket_count(self):
        self.page.wait_for_timeout(3000)
        notify_badge = self.page.locator(self.basket_count)
        try:
            notify_badge.wait_for(state="attached", timeout=5000)
            return notify_badge.inner_text()
        except Exception as ex:
            allure.attach(self.page.screenshot(), name="basket_error", attachment_type=allure.attachment_type.PNG)
            print(f"{ex}")
            return "0"

