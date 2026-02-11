from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import retrieve_phone_code
import time


class UrbanRoutesPage:
    # PREENCHER CAMPO "DE" E "PARA"
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # SELECIONAR TARIFA E CHAMAR TAXI
    taxi_option_locator = (By.XPATH, '//button[contains(text(),"Chamar")]')
    comfort_icon_locator = (By.XPATH, '//img[@src="/static/media/kids.075fd8d4.svg"]')
    comfort_active = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')

    # NÚMERO DE TELEFONE
    number_text_locator = (By.CSS_SELECTOR, '.np-button')
    number_enter = (By.ID, 'phone')
    number_confirm = (By.CSS_SELECTOR, '.button.full')
    number_code = (By.ID, 'code')
    code_confirm = (By.XPATH, '//button[contains(text(),"Confirmar")]')
    number_finish = (By.CSS_SELECTOR, '.np-text')

    # METODO DE PAGAMENTO
    add_metodo_pagamento = (By.CSS_SELECTOR, '.pp-button.filled')
    add_card = (By.CLASS_NAME, 'pp-plus')
    number_card = (By.ID, 'number')
    code_card = (By.CSS_SELECTOR, 'input.card-input#code')
    add_finish_card = (By.XPATH, '//button[contains(text(),"Adicionar")]')
    close_button_card = (By.CSS_SELECTOR, '.payment-picker.open .close-button')
    confirm_card_locator = (By.CSS_SELECTOR, '.pp-value-text')

    # ADICIONAR COMENTÁRIO
    add_comment_locator = (By.ID, 'comment')

    # PEDIR LENÇÓIS E COBERTOR
    switch_blanket_locator = (By.CSS_SELECTOR, '.switch')
    switch_blanket_active_locator = (By.CSS_SELECTOR, 'input.switch-input')

    # PEDIR SORVETE
    add_icecream_locator = (By.CSS_SELECTOR, '.counter-plus')
    qnt_icecream_locator = (By.CSS_SELECTOR, '.counter-value')

    call_taxi_button = (By.CSS_SELECTOR, '.smart-button')
    pop_up_locator = (By.CSS_SELECTOR, '.order-header-title')



    def __init__(self, driver):
        self.driver = driver

    def enter_from_location(self, from_text):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_text)

    def enter_to_location(self, to_text):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_text)

    def enter_locations(self, from_text, to_text):
        self.enter_from_location(from_text)
        self.enter_to_location(to_text)

    def get_from_location_value(self):
        return WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.from_field)
        ).get_attribute('value')

    def get_to_location_value(self):
        return WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.to_field)
        ).get_attribute('value')

    def click_taxi_option(self):
        self.driver.find_element(*self.taxi_option_locator).click()

    def click_comfort_icon(self):
        active = self.driver.find_element(*self.comfort_active)
        if "active" not in active.get_attribute("class"):
            self.driver.find_element(*self.comfort_icon_locator).click()

    def is_comfort_active(self):
        try:
            active_button = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.comfort_active))
            return "active" in active_button.get_attribute('class')
        except:
            return False

    def click_number_text(self, phone_number):
        self.driver.find_element(*self.number_text_locator).click()
        self.driver.find_element(*self.number_enter).send_keys(phone_number)
        self.driver.find_element(*self.number_confirm).click()

        code = retrieve_phone_code(self.driver)  # Digitar código
        code_input = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.number_code)
        )
        code_input.clear()
        code_input.send_keys(code)
        self.driver.find_element(*self.code_confirm).click()

    def confirmation_number(self):
        number = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.number_text_locator))
        return number.text

    def click_add_card(self, card, code):
        self.driver.find_element(*self.add_metodo_pagamento).click()
        self.driver.find_element(*self.add_card).click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.number_card))
        self.driver.find_element(*self.number_card).send_keys(card)
        self.driver.find_element(*self.code_card).send_keys(code)
        self.driver.find_element(*self.code_card).send_keys(Keys.TAB)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.add_finish_card))
        self.driver.find_element(*self.add_finish_card).click()
        self.driver.find_element(*self.close_button_card).click()

    def confirm_card(self):
        return self.driver.find_element(*self.confirm_card_locator).text

    def add_comment(self, comment):
        self.driver.find_element(*self.add_comment_locator).send_keys(comment)

    def comment_confirm(self):
        return self.driver.find_element(*self.add_comment_locator).get_attribute('value')

    def switch_blanket(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.switch_blanket_locator)
        ).click()

    def is_switch_blanket_active(self):
        switch_input = self.driver.find_element(*self.switch_blanket_active_locator)
        return switch_input.is_selected()

    def add_ice(self):
        self.driver.find_element(*self.add_icecream_locator).click()

    def qnt_icecream(self):
        return self.driver.find_element(*self.qnt_icecream_locator).text

    def call_taxi(self):
        self.driver.find_element(*self.call_taxi_button).click()

    def get_pop_up_text(self):
        pop_up = WebDriverWait(self.driver, 5).until( EC.visibility_of_element_located(self.pop_up_locator))
        return pop_up.text
