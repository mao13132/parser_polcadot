from browser.createbrowser import CreatBrowser
from src.polcadot_pars import PolcadotPars


def main():
    stels = True
    browser_core = CreatBrowser('polcadot', stels)

    print(f'Парсер запущен. Захожу на сайт')

    response_job = PolcadotPars(browser_core.driver, stels).start_pars()


if __name__ == '__main__':
    main()
