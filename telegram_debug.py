import requests

import base64

class SendlerOneCreate:
    def __init__(self, driver):
        self.TOKEN = ''
        self.ADMIN_TELEGRAM = '331583382'
        self.driver = driver


    def send_error_tg_img(self):
        filename = "screenshot1.png"

        self.driver.save_screenshot(filename)

        self.send_image(filename)

    def send(self, file):

        # file = open(r'media/ads.jpg', 'rb')
        open_files = {'photo': base64.b64decode(file)}
        cap = {'caption': 'test'}

        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendPhoto?chat_id=" + self.ADMIN_TELEGRAM

        # requests.post(self.api_url + method, data={'chat_id': chat_id}, files={'document': document})

        requests.post(url_req, files=open_files, data=cap)

        file.close()

        print(f"Отправил объявление в телеграм")

    #TODO написать что бы входящий поток был driver_page_source and driver.screen_shoot
    def send_html_and_screen(self, file):
        print(f'{file}')


        file_in = open(file, 'rb')
        open_files = {'document': file_in}

        # cap = {'caption': 'test'}

        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendDocument?chat_id=" + self.ADMIN_TELEGRAM

        response = requests.post(url_req, files=open_files)

        file_in.close()

        print(f"Отправил html в телеграм")

# if __name__ == '__main__':

    def send_image(self, filename):

        file = open(filename, 'rb')

        open_files = {'photo': file}

        cap = {'caption': filename}

        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendPhoto?chat_id=" + self.ADMIN_TELEGRAM

        response = requests.post(url_req, files=open_files, data=cap)

        file.close()

        print(f"Отправил изображение в телеграм")
