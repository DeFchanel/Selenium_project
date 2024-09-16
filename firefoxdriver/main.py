from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import os



service = Service(executable_path=GeckoDriverManager().install())
firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Firefox(service=service, options=firefox_options)


def read_links(driver):
    if 'https://www.google.ru/search?' in driver.current_url:
        main_links = driver.find_elements('xpath', "//a[@jsname='UWckNb']//h3")
        sub_links = driver.find_elements('xpath', "//a[@class='l']")
        all_links = main_links + sub_links
        for link in all_links:
            content = driver.execute_script('return arguments[0].textContent;', link)
            print(content)
    elif 'https://yandex.ru/search' in driver.current_url or 'https://ya.ru/search' in driver.current_url:
        try:
            links = driver.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]//span')
            for link in links:
                content = driver.execute_script('return arguments[0].textContent;', link)
                print(content)
        except:
            driver.find_element('class name', 'Distribution-SplashScreenModalCloseButtonOuter').click()
            links = driver.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]//span')
            for link in links:
                content = driver.execute_script('return arguments[0].textContent;', link)
                print(content)



def read_text(driver):
    print(driver.find_element('xpath', "/html/body").text)


def back(driver):
    driver.back()


def forward(driver):
    driver.forward()


def refresh(driver):
    driver.refresh()


def find(driver, target):
    driver.get('https://www.google.ru')
    find_field = driver.find_element('class name', 'gLFyf')
    find_field.send_keys(target)
    find_field.send_keys(Keys.ENTER)
    time.sleep(2)


def window_switch_to(driver, tab):
    tabs = driver.window_handles
    try:
        driver.switch_to.window(tabs[tab - 1])
    except IndexError:
        print('Вкладка не найдена')


def click_to(driver, text):
    links = driver.find_elements('xpath', f'//a//*[text()="{text}"]/parent::a') + driver.find_elements('xpath', f'//a[text()="{text}"]')
    buttons = driver.find_elements('xpath', f'//button//*[text()="{text}"]/parent::button') + driver.find_elements('xpath', f'//button[text()="{text}"]')
    elements = links + buttons
    if len(elements) == 0:
        print('Такой элемент не найден или он не является кликабельным')
    elif len(elements) > 1:
        print('Подходящих элементов несколько, выберите номер нужного элемента')
        number = int(input())
        elements[number - 1].click()
    else:
        driver.find_elements('xpath', f'//a//*[text()="{text}"]/parent::a')[0].click()



def choose_link(driver, number):
    if 'https://www.google.ru/search?' in driver.current_url:
        links = driver.find_elements('xpath', '//a[@jsname="UWckNb"]')
        links[number - 1].click()
    elif 'https://yandex.ru/search' in driver.current_url or 'https://ya.ru/search' in driver.current_url:
        try:
            links = driver.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]')
            links[number - 1].click()
        except:
            driver.find_element('class name', 'Distribution-SplashScreenModalCloseButtonOuter').click()
            links = driver.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]')
            links[number - 1].click()

try:
    find(driver, 'привет')
    choose_link(driver, 2)
    
except Exception as ex:
    print(ex)