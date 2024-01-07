from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.firefox.options import Options
from .model.screenshot_request import ScreenshotRequest
from .model.screenshot_model import ScreenshotModel

import os

import configparser

class ScreenshotService:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        self.screenshot_dir = config['ScreenshotService']['screenshot_dir']
        self.driver = None
        self.wait = None
        self.width = int(config['ScreenshotService']['width'])
        self.height = int(config['ScreenshotService']['height'])

    def __setup_driver(self, url: str):
        options = Options()
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        self.driver =  webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 10)

        self.driver.set_window_size(width=self.width, height=self.height)
        self.driver.get(url)

    def __take_screenshot(self, screenshot_request: ScreenshotRequest, method: By) -> ScreenshotModel:
        self.__setup_driver(screenshot_request.url)
        search = self.wait.until(EC.presence_of_element_located((method, screenshot_request.handle)))
        self.driver.execute_script("window.focus();")

        # action = ActionChains(self.driver)
        # action.move_to_element(search)
        # action.perform()

        base_path = f"{self.screenshot_dir}/{screenshot_request.folder_name}"
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        full_path = f"{base_path}/{screenshot_request.file_name}.png"

        fp = open(full_path, "wb")
        fp.write(search.screenshot_as_png)
        fp.close()
        return full_path
    
    def __take_screenshot_from_single_url(self, screenshot_request: ScreenshotRequest, method: By) -> ScreenshotModel:
        search = self.wait.until(EC.presence_of_element_located((method, screenshot_request.handle)))
        self.driver.execute_script("window.focus();")

        # action = ActionChains(self.driver)
        # action.move_to_element(search)
        # action.perform()

        base_path = f"{self.screenshot_dir}/{screenshot_request.folder_name}"
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        full_path = f"{base_path}/{screenshot_request.file_name}.png"

        fp = open(full_path, "wb")
        fp.write(search.screenshot_as_png)
        fp.close()
        screenshot_model: ScreenshotModel = ScreenshotModel()
        screenshot_model.id = screenshot_request.id
        screenshot_model.path = full_path
        return screenshot_model

    # def take_screenshot_by_id(self, screenshot_request: ScreenshotRequest) -> ScreenshotModel:
    #     return self.__take_screenshot(
    #         screenshot_request=screenshot_request,
    #         method=By.ID
    #         )

    def __take_screenshots(self, screenshot_requests: list[ScreenshotRequest], method: By) -> list[ScreenshotModel]:
        self.__setup_driver(screenshot_requests[0].url)
        screenshot_models = []
        for screenshot_request in screenshot_requests:
            model: ScreenshotModel = self.__take_screenshot_from_single_url(screenshot_request=screenshot_request, method=method)
            screenshot_models.append(model)
        self.driver.quit()
        return screenshot_models
    
    def take_screenshots_by_ID(self, screenshot_requests: list[ScreenshotRequest]) -> list[ScreenshotModel]:
        return self.__take_screenshots(screenshot_requests=screenshot_requests, method=By.ID)
    
    def take_screenshots_by_ID(self, screenshot_requests: list[ScreenshotRequest]) -> list[ScreenshotModel]:
        return self.__take_screenshots(screenshot_requests=screenshot_requests, method=By.XPATH)
