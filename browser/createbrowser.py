import os
import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


import getpass


class CreatBrowser:

    def __init__(self, name_profile, stels=True):
        platform_to_os = platform.system()

        # if platform_to_os == "Linux":
        #     from xvfbwrapper import Xvfb
        #     vdisplay = Xvfb(width=1280, height=720)
        #     vdisplay.start()

        self.windowsUser = getpass.getuser()

        options = webdriver.ChromeOptions()

        # options.add_argument(f"user-agent=Mozilla/5.0 (Android 10; Mobile; rv:106.0) Gecko/106.0 Firefox/106.0")

        if platform_to_os == "Linux":
            binary = self.get_chrome()
            options.binary_location = binary

        options.add_argument("no-sandbox")
        options.add_argument("--remote-debugging-port=9222")

        if stels:
            options.add_argument("--headless")

        options.add_argument('--disable-dev-shm-usage')

        prefs = {"enable_do_not_track": True}
        options.add_experimental_option("prefs", prefs)

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-infobars")
        options.add_argument("--ignore-certificate-errors")


        options.add_argument(
            "--disable-application-cache")
        options.add_argument(f"start-maximized")

        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")



        s = Service(executable_path=r"/usr/local/bin/chromedriver")

        self.driver = webdriver.Chrome(service=s, options=options)

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                  '''
        })


    def get_chrome(self):
        if os.path.isfile('/usr/bin/chromium-browser'):
            return '/usr/bin/chromium-browser'
        elif os.path.isfile('/usr/bin/chromium'):
            return '/usr/bin/chromium'
        elif os.path.isfile('/usr/bin/chrome'):
            return '/usr/bin/chrome'
        elif os.path.isfile('/usr/bin/google-chrome'):
            return '/usr/bin/google-chrome'
        else:
            return None
