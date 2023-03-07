# content of file conftest.py

import time
import uuid

import pytest
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome, ChromeOptions

@pytest.fixture(autouse=True)
def testing():

   pytest.driver = webdriver.Chrome('X:\aPythonProjectS\BrDrivers/chrDrive.exe')

   # Переход на страницу авторизации PetFriends
   pytest.driver.get('https://petfriends.skillfactory.ru/login')
   pytest.driver.set_window_size(1920, 1080)

   yield

   pytest.driver.quit()

@pytest.fixture()
def page_my_pets():

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
   # Ввод email
   pytest.driver.find_element('id', 'email').send_keys('stest@mail')

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
   # Ввод пароля
   pytest.driver.find_element('id', 'pass').send_keys('stest')

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
   # Нажать на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
   # Нажать на кнопку "Мои питомцы"
   pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()









'''
#-------------------------------------------
@pytest.fixture
def web_browser(request, selenium):
    browser = selenium
    browser.set_window_size(1920, 1080)

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass  # just ignore any errors here

'''


