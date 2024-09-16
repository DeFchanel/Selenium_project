import speech_recognition
import pyttsx3
import random
import datetime
from data import numbers, lang_codes
from selenium import webdriver
from translate import Translator
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from art import tprint
from selenium.webdriver.firefox.service import Service
from time import sleep

class VoiceAssistant:
    names = []
    sex = ""
    speech_language = ""
    recognition_language = ""

def refresh(driver):
    driver.get(driver.current_url)

def add_new_tab(driver):
    driver.execute_script("window.open('https://www.google.com')")

def window_switch_to(driver, tab):
    tabs = driver.window_handles
    number = int(numbers[tab])
    try:
        driver.switch_to.window(tabs[number - 1])
    except IndexError:
        say('Вкладка не найдена')

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

def read_text(driver):
    print(driver.find_element('xpath', "/html/body").text)

def listen():
    speech = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        speech.pause_threshold = 1 
        speech.adjust_for_ambient_noise(source, duration = 0.5)
        try:
            result_speech = speech.recognize_google(speech.listen(source), language="ru-RU").lower()
            print(result_speech)
        except:
            result_speech = listen()
    return result_speech


def find(driver, target):
    driver.get('https://www.google.ru')
    find_field = driver.find_element('class name', 'gLFyf')
    find_field.send_keys(target)
    find_field.send_keys(Keys.ENTER)


def choose_link(driver, target):
    number = int(numbers[target])
    if 'https://www.google.ru/search?' in driver.current_url:
        links = driver.find_elements('xpath', '//a[@jsname="UWckNb"]')
        links2 = []
        for el in links:
            if el.is_displayed() and el.is_enabled():
                links2.append(el)
        links2[number - 1].click()
    elif 'https://yandex.ru/search' in driver.current_url or 'https://ya.ru/search' in driver.current_url:
        try:
            links = driver.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]')
            links[number - 1].click()
        except:
            driver.find_element('class name', 'Distribution-SplashScreenModalCloseButtonOuter').click()
            links = driver.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]')
            links[number - 1].click()


def setup_assistant_voice():
    voices = ttsEngine.getProperty("voices")
    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        if assistant.sex == "female":
            ttsEngine.setProperty("voice", voices[1].id)
        else:
            ttsEngine.setProperty("voice", voices[2].id)
    else:
        assistant.recognition_language = "ru-RU"
        ttsEngine.setProperty("voice", voices[0].id)


def say(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def get_translation(translate_object):
    if translate_object != '':
        say('Выберите язык для перевода.')
        lang_from = listen()
        try:
            lang_from_code = lang_codes[lang_from]
        except:
            say('Язык не найден')
            return
        say('На какой язык перевести?')
        lang_to = listen()
        try:
            lang_to_code = lang_codes[lang_to]
        except:
            say('Язык не найден')
            return
        translator = Translator(from_lang=lang_from_code, to_lang=lang_to_code)
        result = translator.translate(translate_object)
        print(result)
        say(result)


def record_and_recognize_audio(*args: tuple):
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)
        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()
        except speech_recognition.UnknownValueError:
            pass
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")
        return recognized_data


def finish_programm():
    global to_break
    say("Завершаю...")
    driver.quit()
    to_break = True


def play_farewells_and_quit():
    global to_break
    say("До свидания")
    driver.quit()
    to_break = True


def play_greeting():
    greeting = random.choice(greetings)
    say(greeting)


def get_time():
    now = datetime.datetime.now()
    now_time = f'Сейчас {now.hour} {now.minute}' 
    if len(now_time) != 12:
        say(f'Сейчас {now.hour} 0 {now.minute}')
    else:
        say(now_time)
    ttsEngine.runAndWait()


if __name__ == "__main__":
    tprint("I'm V.I.C.E :)")
    service = Service(executable_path=GeckoDriverManager().install())
    firefox_options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=service, options=firefox_options)
    commands = {
        ('найди', 'google', 'загугли', 'поищи', 'найти'): find,
        ("перевод", "перевести", "переведи"): get_translation,
        ("открой новую вкладку", "новая вкладка"): add_new_tab,
        ("привет", "здравствуй", "добрый день", "здарова", "приветик"): play_greeting,
        ("пока", "до свидания", "прощай"): play_farewells_and_quit,
        ("переключись на вкладку под номером", "переключись на вкладку потом номер", "переключись на вкладку с номером",  "переключись на вкладку номер", "переключись на вкладку"): window_switch_to,
        ("перезагрузи", "перезагрузка", "перезагрузи страницу", "перезагрузка страницы"): refresh,
        ("заверши работу программы", "заверши программу", "заверши работу", "закончить работу", "завершил работу", "выключи программу", "завершить программу", "завершить работу", "останови программу"): finish_programm,
        ("который час", "сколько времени", 'скажи время', "сколько сейчас времени", "Время"): get_time,
        ("открой ссылку под номером", "открой ссылку с номером", "открой ссылку номер", "перейди по ссылке под номером", "перейди по ссылке с номером", "перейди по ссылке номер", "выбери ссылку под номером", "выбери ссылку с номером", "выбери ссылку номер", "перейди по ссылке", "нажми на ссылку под номером", "нажми на ссылку с номером", "нажми на ссылку номер", "выбери ссылку", "нажми на ссылку"): choose_link,
        ("закончи диалог", 'хватит', "закончить диалог", "хватит болтать", "закончи разговор", "закончить разговор", "завершить диалог", "завершить разговор", "разговор окончен", "заверши диалог"): 'stop_talk',
    }
    greetings = ["привет", "здравствуйте", "добрый день"]
    farewells = ["пока", "до свидания", "увидимся", "до встречи"]
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    ttsEngine = pyttsx3.init()
    rate = ttsEngine.getProperty('rate')
    ttsEngine.setProperty('rate', rate-50)
    volume = ttsEngine.getProperty('volume')
    ttsEngine.setProperty('volume', volume+10)
    assistant = VoiceAssistant()
    assistant.names = ["вайс", "вася", "ice", "айс", "vice", "wise", "вась"]
    assistant.sex = "male"
    assistant.speech_language = "ru"
    setup_assistant_voice()
    to_break = False
    while not to_break:
        done = False
        in_commands = False
        voice_input = listen()
        if voice_input in assistant.names:
            try:
                say("Слушаю вас")
                while (not done) and (not to_break):
                    in_commands = False
                    voice_input = listen()
                    for key in commands.keys():
                        if done or in_commands:
                            break
                        for key2 in key:
                            if key2 in voice_input:
                                in_commands = True
                                target = voice_input.replace(key2, '')
                                if commands[key] == 'stop_talk':
                                    say('Перестаю вас слушать')
                                    done = True
                                    break
                                elif commands[key] == find:
                                    find(driver, target)
                                    break
                                elif commands[key] == add_new_tab:
                                    add_new_tab(driver)
                                    break
                                elif commands[key] == get_translation:
                                    to_translate = target[1:]
                                    get_translation(to_translate)
                                    break
                                elif commands[key] == choose_link:
                                    choose_link(driver, target)
                                    break
                                elif commands[key] == window_switch_to:
                                    window_switch_to(driver, target)
                                    break
                                elif commands[key] == refresh:
                                    refresh(driver)
                                    break
                                else:
                                    if key2 == voice_input:
                                        commands[key]()
                                        break
            except:
                say('Что-то пошло не так')
    exit()

