from browser.createbrowser import CreatBrowser
from src.polcadot_pars import PolcadotPars


def main():

    filter_24_date = True

    filter_count_day = 8

    browser_core = CreatBrowser()

    print(f'Парсер запущен. Захожу на сайт')

    response_job = PolcadotPars(browser_core.driver, filter_count_day).start_pars()

    print(f'Работу закончил. Сохранил \n{response_job}.xlsx\n{response_job}.json')


if __name__ == '__main__':
    main()
