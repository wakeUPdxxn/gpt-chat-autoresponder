import openai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from time import sleep
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread
from os import path
import json

userData = {"gptApiKey": 'null', "vkToken": 'null',
            "phone": 'null', "pass": 'null'}

options = Options()
# options.add_argument("window-size=800,1000")
# ua = UserAgent()
# user_agent = ua.random
# options.add_argument(f'user-agent={user_agent}')
browser = any


def dataEditor(option):
    if option == 'add':
        with open("data.json", "w") as fh:
            json.dump(userData, fh)


def dataReader():
    if str(path.exists('data.json')) != 'True':
        return 1
    with open("data.json", "r") as fh:
        userData = json.load(fh)
    for key, value in userData.items():
        if value == 'null':
            print('User Data is not full')


def isFirstTime():
    if str(path.exists('data.json')) != 'True':
        print('Seems its your first time there.Lets make a data setup?[Y/n]')
        choise = input()
        if choise == 'Y' or choise == 'y':
            print('Please,enter your phone number: ')
            userData['phone'] = input()
            print('Please,enter your account pass: ')
            userData['pass'] = input()
            print('Please,enter your vk token: ')
            userData['vkToken'] = input()
            print('Please,enter your gptChat api key: ')
            userData['gptApiKey'] = input()

            dataEditor('add')
        else:
            return
    else:
        return


def exitWaiter():
    word = input()
    if word == 'Exit' or word == 'Stop':
        browser.close()
        exit(1)


def secureCodeWaiter():
    while True:
        print('Your secure code: ')
        code = input()
        if code == '':
            continue
        else:
            return code


def signInWithSecureCode():
    browser = webdriver.Chrome(options=options)
    browser.get('https://m.vk.com/im?')

    phone = browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[1]/section/div[1]/div/div/input').send_keys(userData['phone'])

    browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[2]/div[1]/button/span[1]/span').click()
    sleep(1)

    password = browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[1]/div[3]/div[1]/div/input').send_keys(userData['pass'])

    browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[2]/button/span[1]/span').click()

    secureCode = secureCodeWaiter()

    number = browser.find_element(
        "xpath", '//*[@id="otp"]').send_keys(secureCode)

    browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[3]/div/button/span[1]/span/span').click()
    sleep(2)
    if browser.current_url != 'https://m.vk.com/mail':
        signInWithSecureCode()


def signInWithPassword():
    browser = webdriver.Chrome(options=options)
    browser.get('https://m.vk.com/im?')

    phone = browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[1]/section/div[1]/div/div/input').send_keys(userData['phone'])

    browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[2]/div[1]/button/span[1]/span').click()
    sleep(1)

    browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[4]/div/button[2]').click()
    sleep(0.5)

    password = browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[1]/div[3]/div[1]/div/input').send_keys(userData['pass'])

    browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[2]/button/span[1]/span').click()
    sleep(4)


def makeAnswer(answer):
    msg = browser.find_element(
        "xpath", '//*[@id="mcont"]/div/div[2]/div[2]/div[5]/div[2]/form/div[4]/div[4]/textarea').send_keys(answer)
    sleep(1)

    browser.find_element(
        "xpath", '//*[@id="mcont"]/div/div[2]/div[2]/div[5]/div[2]/form/div[4]/button/div[8]').click()
    sleep(1)


def messageWaiter():
    vk = vk_api.VkApi(token=userData['vkToken'])
    longpool = VkLongPoll(vk)
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me and event.text != "Стоп":
                if event.peer_id == #DIALOG ID HERE:
                    if browser.current_url != 'https://m.vk.com/im?sel=731564359':
                        browser.get('https://m.vk.com/im?sel=731564359')
                        gptChatRequest(event.text)
                    else:
                        gptChatRequest(event.text)
                elif event.peer_id == #ANOTHER DIALOG ID:
                    if browser.current_url != 'https://m.vk.com/im?sel=230713626':
                        browser.get('https://m.vk.com/im?sel=230713626')
                        gptChatRequest(event.text)
                    else:
                        gptChatRequest(event.text)

def gptChatRequest(request):
    openai.api_key = userData['gptApiKey']
    messages = [{"role": "system", "content":
                 request}]
    try:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    except:
        print("GptChat limit reached")
        sleep(25)
        gptChatRequest(request)
    else:
        reply = chat.choices[0].message.content
        makeAnswer(reply)


def main():
    dataStatus = dataReader()
    if dataStatus == 1:
        print('User data is not fully filled out! \n')
    print('1-SignIn with password \n2-SignIn with secure code \n3-Exit from the application \n')
    choise = input()
    if choise == '1':
        signInWithPassword()
    elif choise == '2':
        signInWithSecureCode()
    elif choise == '3':
        exit(1)
    print('For close the application,please type "Exit" or "Stop". Enjoy)')

    exitWaiterThread = Thread(target=exitWaiter)
    exitWaiterThread.start()

    messageWaiter()


isFirstTime()
main()
