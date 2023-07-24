from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.polcadot_post_pars import PolcadotPostPars


class PolcadotPostItter:
    def __init__(self, driver, links_post):
        self.driver = driver
        self.source_name = 'Polkadot'
        self.links_post = links_post

    def load_page(self, url):
        try:

            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на "{url}" "{es}"')
            return False

    def __check_load_page(self, name_post):
        try:
            # WebDriverWait(self.driver, 60).until(
            #     EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{name_post[:-3]}")]')))
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(@class, 'children')]")))
            return True
        except Exception as es:
            print(f'Ошибка при загрузке "{name_post}" поста "{es}"')
            return False

    def loop_load_page(self, post):
        coun = 0
        coun_ower = 4

        while True:
            coun += 1

            if coun >= coun_ower:
                print(f'Не смог зайти в пост {post["name_post"]}')
                return False

            response = self.load_page(post['link'])

            if not response:
                continue

            result_load = self.__check_load_page(post['name_post'])

            if not result_load:
                return False

            return True

    def itter_posts(self, posts, count_seld_dict):
        for count, post in enumerate(posts):

            result_load_page = self.loop_load_page(post)

            if not result_load_page:
                continue

            data_pars = PolcadotPostPars(self.driver, post).start_pars()

            self.links_post[count_seld_dict]['links'][count]['data'] = data_pars

            # print(f'Обработал пост {post["name_post"][:10]}')

    def itter_dict_them(self):
        for count_seld_dict, post in enumerate(self.links_post):
            print(f'Начинаю обработку группы постов {post["name_them"]}')

            response_itter_links = self.itter_posts(post['links'], count_seld_dict)

            print()

        return True

    def start_post_pars(self):

        response_itter_post = self.itter_dict_them()

        return self.links_post
