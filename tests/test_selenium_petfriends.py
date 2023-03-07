import time
from idlelib import browser
import uuid
import pytest
import selenium
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome, ChromeOptions
'''
Написать тест, который проверяет, что на странице со списком питомцев пользователя:
  1.Присутствуют все питомцы.
  2.Хотя бы у половины питомцев есть фото.
  3.У всех питомцев есть имя, возраст и порода.
  4.У всех питомцев разные имена.
  5.В списке нет повторяющихся питомцев. (Сложное задание).
  
  Добавьте неявные ожидания элементов (фото, имя питомца, его возраст)
'''

'''
Подсказки для решения:
1.Количество питомцев взято из статистики пользователя
2.Количество питомцев с фото тоже можно посчитать, взяв статистику пользователя.
3.Необходимо собрать в массив имена питомцев
4.Повторяющиеся питомцы — это питомцы, у которых одинаковое имя, порода и возраст
'''

'''
python -m pytest -v --driver Chrome --driver-path X:\aPythonProjectS\BrDrivers/chrDrive tests\test_selenium_petfriends.py

.implicitly_wait(10) неявн
WebDriverWait(pytest.driver, 10) явн
'''

def test_all_pets_on_the_page(page_my_pets):
   '''1. Проверка наличия всех питомцев пользователя на странице "мои питомцы"'''


   element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left')))

   # Статистику пользователя сохранить в statistic
   statistic = pytest.driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')

   element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

   # Сохранить в переменную pets элементы карточек питомцев
   pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   # Получаем количество питомцев из статистики пользователя
   number = statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])
   # Получаем количество питомцев в таблице
   number_of_pets = len(pets)
   print(f'\n\nКОЛИЧЕСТВО ПИТОМЦЕВ ({number}) = КОЛИЧЕСТВО ЗАПИСЕЙ В ТАБЛИЦЕ ({number_of_pets})')

   # ПРОВЕРКА: КОЛИЧЕСТВО ПИТОМЦЕВ ИЗ СТАТИСТИКИ = КОЛИЧЕСТВО ПИТОМЦЕВ В ТАБЛИЦЕ
   assert number == number_of_pets



def test_half_of_the_pets_have_photos(page_my_pets):  #(половина или больше)
   '''2. Поверка наличия фото хотя бы у половины питомцев на странице "мои питомцы"'''

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
   # Статистику пользователя сохранить в statistic
   statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

   # Сохранить в images элементы с атрибутом img
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

   # Взять количество питомцев из статистики пользователя и поделить на 2
   number = statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])
   half = number // 2
   # Количество питомцев с фотографией
   number_of_photos = 0

   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         number_of_photos += 1

   print(f'\nПоловина питомцев = : {half}')
   print(f'\nКоличество фото: {number_of_photos}')
   # ПРОВЕРКА: количество питомцев с фото >= 1/2 количества питомцев
   assert number_of_photos >= half




def test_all_pets_have_name_and_age_and_breed(page_my_pets):
   '''3. Поверка наличия у всех питомцев страницы "мои питомцы" имени, возраста и породы'''

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
   # Сохранить в переменную pet_data данные о питомцах
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   # Перебираем данные из pet_data, оставляем имя, возраст, и породу и разделяем по пробелу. Находим количество элементов в получившемся списке и сравниваем их с ожидаемым результатом
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      result = len(split_data_pet)
      assert result == 3



def test_all_pets_have_different_names(page_my_pets):
   '''4. На странице "мои питомцы" у всех питомцев разные имена'''

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
   # Сохранить данные о питомцах в pet_data
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   # Перебираем данные из pet_data (имя, возраст, породу), остальное меняем на пустую строку и разделяем по пробелу.
   # Имена добавляем в список pets_name.
   pets_name = []
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')

      pets_name.append(split_data_pet[0])

   # Перебрать имена и если имя повторяется, прибавить к счетчику r единицу.
   # Проверяем, если povtor == 0 то повторяющихся имен нет.
   povtor = 0
   for i in range(len(pets_name)):
      if pets_name.count(pets_name[i]) > 1:
         povtor += 1
   assert povtor == 0
   print('\nПовторяющихся имён: ', povtor)
   print(pets_name)




def test_no_duplicate_pets(page_my_pets):
   '''5. В списке "Мои питомцыы" нет повторяющихся питомцев'''

   # Явное ожидание
   element = WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
   # Сохранить в pet_data элементы с информацией о питомцах
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
   # Перебрать данные из pet_data, оставить имя, возраст, породу, остальное заменить на пустую строку и разделить по пробелу.
   list_data = []
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      list_data.append(split_data_pet)
   # Объединить имя, возраст и породу в строку
   line = ''
   for i in list_data:
      line += ''.join(i)
      line += ' '

   list_line = line.split(' ')

   # Превращаем список в множество
   set_list_line = set(list_line)

   # Находим количество элементов списка и множества
   a = len(list_line)
   b = len(set_list_line)

   # ПРОВЕРКА: A-B, если количество элементов = 0 => записи с одинаковыми данными о питомцах отсутствуют
   result = a - b
   assert result == 0
   print("\nПовторяющихся питомцев: ", result)







def test_show_my_pets():
   '''25.5.1 Проверка карточек питомцев'''
   # Неявное ожидание
   pytest.driver.implicitly_wait(10)

   pytest.driver.find_element('id', 'email').send_keys('stest@mail')
   pytest.driver.find_element('id', 'pass').send_keys('stest')
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'

   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   assert names[0].text != ''

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[1].text != ''
      assert ',' in descriptions[i].text
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0


def test_pets_table():
   '''25.5.1 проверка таблицы питомцев "Мои питомцы"'''
   # Явное ожидание
   element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
   # Ввод email
   pytest.driver.find_element('id', 'email').send_keys('stest@mail')
   element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))
   # Ввод password
   pytest.driver.find_element('id', 'pass').send_keys('stest')

   element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
   # Нажимаем на кнопку входа
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
   # Нажимаем на "Мои питомцы"
   pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

   # ПРОВЕРКА: пользователю открылась таблица с питомцами на странице "Мои питомцы"
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'





