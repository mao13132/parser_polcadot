import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from src.temp_list import TempList


class PolcadotPostPars:
    def __init__(self, driver, data_post):
        self.driver = driver
        self.source_name = 'Polkadot'
        self.data_post = data_post
        self.post_data = {}

    def get_status(self):
        try:
            status = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'rounded-md')]"
                                                                 f"//*[contains(@class, 'rounded-full')]").text
        except Exception as es:
            print(f'Ошибка при получение статуса {es}')
            status = ''

        return status

    def get_author(self):
        try:
            name_author = self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'By:')]"
                                                                      f"//parent::div"
                                                                      f"//*[contains(@class, 'identityName')]").text
        except Exception as es:
            print(f'Ошибка при получение name_author {es}')
            name_author = ''

        return name_author

    def loop_get_author(self):

        count = 0
        count_ower = 4

        while True:
            count += 1

            if count >= count_ower:
                return ''

            author = self.get_author()

            if '...' in author:
                time.sleep(2)
                continue

            return author

    def get_model(self):
        try:
            model = self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'By:')]"
                                                                f"//parent::div"
                                                                f"//*[contains(text(), 'in')]"
                                                                f"//parent::div/span[2]").text
        except Exception as es:
            print(f'Ошибка при получение model {es}')
            model = ''

        return model

    def get_date_edit(self):
        try:
            date_edit = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'clock')]"
                                                                    f"//parent::span").text
        except Exception as es:
            print(f'Ошибка при получение date_edit {es}')
            date_edit = ''

        return date_edit

    def loop_click_show_more(self):
        count = 0
        count_ower = 4

        while True:
            count += 1

            if count >= count_ower:
                return False

            try:
                self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Show more')]").click()
            except:
                time.sleep(1)
                continue

            try:
                self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Show more')]")
            except:

                return True

    def get_post_text(self):
        try:

            post_text = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'post-content')]").text

        except Exception as es:
            print(f'Ошибка при получение post_text {es}')
            post_text = ''

        return post_text

    def get_post_reactions(self):
        try:

            react_in = self.driver.find_element(by=By.XPATH, value=f"//*[@id='actions-bar']"
                                                                   f"//*[contains(@class, 'reactions')]").text

        except Exception as es:
            print(f'Ошибка при получение get_post_reactions {es}')
            return 0, 0

        try:
            like_post, dislike_post = react_in.split('\n')
        except:
            return 0, 0

        return like_post, dislike_post

    def get_voting(self):
        try:

            voting = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, 'progress-text')]")

        except Exception as es:
            print(f'Ошибка при получение get_voting {es}')
            return '0%', '0%'

        try:
            decision = voting[-2].text
        except:
            decision = '0%'

        try:
            confirmation = voting[-1].text
        except:
            confirmation = '0%'


        return decision, confirmation

    def get_voting2(self):
        try:

            voting = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, 'vote-progress')]//span[contains(@class, 'semibold')]")

        except Exception as es:
            print(f'Ошибка при получение get_voting2 {es}')
            return '0%', '0%'

        try:
            aye = voting[-2].text
        except:
            aye = '0%'

        try:
            nay = voting[-1].text
        except:
            nay = '0%'


        return aye, nay

    def get_full_voting(self):
        try:

            list_voit_in = self.driver.find_elements(by=By.XPATH, value=f"//section[contains(@class, 'grid grid-cols')]")

        except Exception as es:
            print(f'Ошибка при получение get_full_voting {es}')
            return '0', '0', '0', '0'

        try:

            formated_voit_data = list_voit_in[-1].find_elements(by=By.XPATH, value=f".//article")

        except Exception as es:
            print(f'Ошибка при получение get_full_voting formated_voit_data {es}')
            return '0', '0', '0', '0'

        try:
            ayes = formated_voit_data[0].find_elements(by=By.XPATH, value=f".//div")[-1].text
        except:
            ayes = '0'

        try:
            nays = formated_voit_data[1].find_elements(by=By.XPATH, value=f".//div")[-1].text
        except:
            nays = '0'

        try:
            support = formated_voit_data[2].find_elements(by=By.XPATH, value=f".//div")[-1].text
        except:
            support = '0'

        try:
            issuance = formated_voit_data[3].find_elements(by=By.XPATH, value=f".//div")[-1].text
        except:
            issuance = '0'

        return ayes, nays, support, issuance




    def start_pars(self):
        name_author = self.loop_get_author()
        self.post_data['name_author'] = name_author

        status_post = self.get_status()
        self.post_data['status'] = status_post

        model = self.get_model()
        self.post_data['model'] = model

        date_edit = self.get_date_edit()
        self.post_data['date_edit'] = date_edit

        self.loop_click_show_more()

        post_text = self.get_post_text()
        self.post_data['post_text'] = post_text

        like_post, dislike_post = self.get_post_reactions()
        self.post_data['like_post'] = like_post
        self.post_data['dislike_post'] = dislike_post

        decision, confirmation = self.get_voting()
        self.post_data['decision'] = decision
        self.post_data['confirmation'] = confirmation

        aye, nay = self.get_voting2()
        self.post_data['aye'] = aye
        self.post_data['nay'] = nay

        ayes, nays, support, issuance = self.get_full_voting()
        self.post_data['ayes'] = ayes
        self.post_data['nays'] = nays
        self.post_data['support'] = support
        self.post_data['issuance'] = issuance


        print()
        print()
