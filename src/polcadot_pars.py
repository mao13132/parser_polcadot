import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from src.polcadot_post_itter import PolcadotPostItter
from src.temp_list import TempList

class PolcadotPars:
    def __init__(self, driver):
        self.driver = driver
        self.url = f'https://polkadot.polkassembly.io/opengov'
        self.source_name = 'Polkadot'
        self.links_post = []

    def load_page(self, url):
        try:
            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на стартовую страницу "{es}"')
            return False

    def __check_load_page(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Latest Activity')]")))
            return True
        except:
            print(f'Ошибка при загрузке стартовой страницы страницы')
            return False

    def get_thema(self):
        try:
            list_thema = self.driver.find_elements(by=By.XPATH,
                                                   value=f"//*[contains(@class, 'nav-list')]/div")
        except Exception as es:
            print(f'Ошибка при обработке тем "{es}"')
            return False

        return list_thema

    def get_row_start_page(self):
        try:
            table = self.driver.find_elements(by=By.XPATH,
                                              value=f"(//*[contains(@class, 'tabs-card')]//tbody[contains(@class, 'ant-table-tbody')])")

            # list_row = self.driver.find_elements(by=By.XPATH,
            #                                      value=f"//*[contains(@class, 'tabs-card')]//*[contains(@class, 'ant-table-tbody')]/tr")
        except Exception as es:
            print(f'Ошибка при получении строк "{es}"')
            return []

        try:
            list_row = table[-1].find_elements(by=By.XPATH, value=f".//tr")
        except Exception as es:
            print(f'Ошибка при получении строк "{es}"')
            return []

        return list_row

    def loop_click_theme(self, them):
        count = 0
        count_ower = 4

        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог кликнуть на категорию')
                return False

            try:
                them.click()
            except:
                time.sleep(2)
                continue

            try:
                _active = them.get_attribute('class')
            except:
                time.sleep(2)
                continue

            if 'active' in _active:
                return True

    def get_name_count_theme(self, them):
        try:
            name_them = them.text.split('\n')
            count_post = int(name_them[1].replace('(', '').replace(')', ''))
            name_them = name_them[0]
        except:
            name_them = 'Root'
            count_post = 0

        return name_them, count_post

    def filter_date(self, row):
        try:
            _id_post = row.find_elements(by=By.XPATH,
                                         value=f".//td")
            id_post = _id_post[-1].text
        except:
            return True

        if 'hour' in id_post:
            return id_post
        if 'day' in id_post:
            try:
                coun_day = int(id_post.split()[0])
            except:
                return id_post
            if coun_day > 1:
                return False


        return id_post

    def generet_links(self, list_row, name_them):

        list_links = []

        link = 'https://polkadot.polkassembly.io'

        for row in list_row:

            if name_them.lower() == 'discussions':
                slug = 'post'

                try:
                    id_post = row.get_attribute('data-row-key')
                except:
                    continue

                if id_post is None:
                    continue
            else:
                slug = 'referenda'

                try:
                    _id_post = row.find_elements(by=By.XPATH,
                                                 value=f".//td")
                    id_post = _id_post[0].text
                except:
                    continue

                if id_post is None or id_post == '':
                    continue

            try:
                _name_post = row.find_elements(by=By.XPATH,
                                             value=f".//td")
                name_post = _name_post[1].text
            except:
                name_post = ''

            date_post = self.filter_date(row)

            if not date_post:
                """Фильтр по дате в 24 часа"""
                continue


            good_links = f'{link}/{slug}/{id_post}'

            # print(good_links)

            post_data = {}
            post_data['link'] = good_links
            post_data['id'] = id_post
            post_data['name_post'] = name_post
            post_data['date'] = date_post

            list_links.append(post_data)

        return list_links

    def loop_find_comments(self):
        count = 0
        count_ower = 4

        while True:
            count += 1

            if count >= count_ower:
                print(f'Не смог спарсить комментарии')
                return False

            try:
                elements = self.driver.find_elements(by=By.XPATH,
                                                     value=f"//*[contains(text(), 'Upcoming Events')]//parent::div//parent::div//*[contains(@class, 'ant-spin-container')]")
            except Exception as es:
                print(f'Ошибка при 1 парсинге комментариев "{es}"')
                time.sleep(1)
                continue

            try:
                list_com_in = elements[1].find_elements(by=By.XPATH, value=f".//li")

            except Exception as es:
                print(f'Ошибка при 2 парсинге комментариев "{es}"')
                time.sleep(1)
                continue

            if len(list_com_in) > 0:

                return list_com_in

            time.sleep(1)


    def scrap_comment(self):
        good_comments = []

        list_com_in = self.loop_find_comments()

        if not list_com_in:
            return False

        print(f'Обнаружил {len(list_com_in)} комментариев')

        for comments in list_com_in:
            try:
                data_com, time_comm, author_comm, text_comm = comments.text.split('\n')
            except Exception as es:
                print(f'Ошибка при сплите комментария "{es}"')
                continue

            dict_comm = {}
            dict_comm['data_com'] = data_com
            dict_comm['time_comm'] = time_comm
            dict_comm['author_comm'] = author_comm
            dict_comm['text_comm'] = text_comm


            good_comments.append(dict_comm)

        return good_comments




    def loop_scrap_rows(self, list_them):
        for them in list_them[1:-1]:
            list_row = []

            name_them, count_post = self.get_name_count_theme(them)

            if count_post == 0:
                continue

            active_theme = self.loop_click_theme(them)

            if not active_theme:
                continue

            #TODO вставить парсер комментариев



            list_row = self.get_row_start_page()

            if not list_row:
                continue

            list_links = self.generet_links(list_row, name_them)

            good_itter = {}

            good_itter['name_them'] = name_them
            good_itter['links'] = list_links

            self.links_post.append(good_itter)

            print(f'Спарсил {count_post} тем на {name_them}')

        return self.links_post

    def show_table(self):
        try:
            table_theme = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'tabs-card')]"
                                                                      f"//*[contains(@role, 'tablist')]")
        except:
            return False

        try:
            self.driver.execute_script("arguments[0].setAttribute('class','123')", table_theme)
        except:

            return False

        return True

    def load_start_site(self):
        start_page = self.load_page(self.url)

        if not start_page:
            return False

        check_page = self.__check_load_page()

        if not check_page:
            return False

        print(f'Успешно зашёл на {self.source_name}')

        return True

    def pars_step1_rows(self):


        list_them = self.get_thema()

        if not list_them:
            return False

        response_show_table = self.show_table()

        if not response_show_table:
            print(f'Не получилось расширить таблицу с темами. Пропускаю пункт')

        response_pars_row = self.loop_scrap_rows(list_them)

        if response_pars_row == []:
            print(f'Не нашёл тем на {self.source_name} завершаюсь')
            return False



    def start_pars(self):

        # result_start_page = self.load_start_site()
        #
        # if not result_start_page:
        #     return False
        #
        #
        # list_comments = self.scrap_comment()
        #
        # response = self.pars_step1_rows()

        list_comments = TempList.list_comments
        links_post = TempList.link_posts

        list_good_pars_post = PolcadotPostItter(self.driver, links_post).start_post_pars()


        print()
