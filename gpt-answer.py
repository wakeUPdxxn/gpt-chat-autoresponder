import openai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from time import sleep
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread

gptChatApiKey = 'your gpt chat key'
vkToken = 'your vk access token'
phoneNumber = 'your phone number'
accountPassword = 'your password'

options = Options()
# options.add_argument("window-size=800,1000")
# ua = UserAgent()
# user_agent = ua.random
# options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=options)


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
    browser.get('https://m.vk.com/im?')

    phone = browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[1]/section/div[1]/div/div/input').send_keys(phoneNumber)

    browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[2]/div[1]/button/span[1]/span').click()
    sleep(1)

    password = browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[1]/div[3]/div[1]/div/input').send_keys(accountPassword)

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
    browser.get('https://m.vk.com/im?')

    phone = browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[1]/section/div[1]/div/div/input').send_keys(phoneNumber)

    browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[2]/div[1]/button/span[1]/span').click()
    sleep(1)

    browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[4]/div/button[2]').click()
    sleep(0.5)

    password = browser.find_element(
        "xpath", '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[1]/div[3]/div[1]/div/input').send_keys(accountPassword)

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
    vk = vk_api.VkApi(token=vkToken)
    longpool = VkLongPoll(vk)
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me and event.text != "Стоп":
                if event.peer_id == 731564359:
                    if browser.current_url != 'https://m.vk.com/im?sel=731564359':
                        browser.get('https://m.vk.com/im?sel=731564359')
                        gptChatRequest(event.text)
                    else:
                        gptChatRequest(event.text)
                elif event.peer_id == 230713626:
                    if browser.current_url != 'https://m.vk.com/im?sel=230713626':
                        browser.get('https://m.vk.com/im?sel=230713626')
                        gptChatRequest(event.text)
                    else:
                        gptChatRequest(event.text)
                elif event.peer_id == 258024208:
                    if browser.current_url != 'https://m.vk.com/im?sel=258024208':
                        browser.get('https://m.vk.com/im?sel=258024208')
                        gptChatRequest(event.text)
                    else:
                        gptChatRequest(event.text)
                elif event.peer_id == 509403815:
                    if browser.current_url != 'https://m.vk.com/im?sel=509403815':
                        browser.get('https://m.vk.com/im?sel=509403815')
                        gptChatRequest(event.text)
                    else:
                        gptChatRequest(event.text)


def gptChatRequest(request):
    openai.api_key = gptChatApiKey
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


print('1-SignIn with password \n2-SignIn with secure code \n3-Exit from the application')
choise = input()
if choise == '1':
    signInWithPassword()
elif choise == '2':
    signInWithSecureCode()
elif choise == '3':
    browser.close()
    exit(1)

print('For close the application,please type "Exit" or "Stop". Enjoy)')

exitWaiterThread = Thread(target=exitWaiter)
exitWaiterThread.start()

messageWaiter()
