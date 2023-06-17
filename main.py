from browser.createbrowser import CreatBrowser
from src.polcadot_pars import PolcadotPars


def main():
    stels = False
    browser_core = CreatBrowser('polcadot', stels)

    print(f'Парсер запущен')

    response_job = PolcadotPars(browser_core.driver).start_pars()


if __name__ == '__main__':
    main()
