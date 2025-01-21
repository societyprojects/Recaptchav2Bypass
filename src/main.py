#!/usr/bin/env python3

import os
import time
import pydub
import urllib
import speech_recognition

from tempfile import gettempdir
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ChromeService
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Rcptchv2Bypss:

    def __init__(self, page_timeout:float, headless_mode:bool):
        self.page_timeout = page_timeout
        self.headless_mode = headless_mode

        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.option_driver)
        self.driver.set_page_load_timeout(self.page_timeout)

    @property
    def option_driver(self):
        options = ChromeOptions()
        if self.headless_mode == False:
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")

        if self.headless_mode == True:
            options.add_argument("--headless")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")

        return options
    
    def recaptcha_service(self, driver):
        # Switch to the iframe containing the recaptcha
        iframe_inner = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
        driver.switch_to.frame(iframe_inner)

        time.sleep(1)

        # Click on the recaptcha
        try:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".rc-anchor-content"))
            ).click()
        except TimeoutException:
            raise TimeoutError("Failed to click recaptcha")

        # Switch back to the default frame
        driver.switch_to.default_content()

        time.sleep(1)

        # Get the new iframe for audio
        iframe = driver.find_element(By.XPATH, "//iframe[contains(@title, 'recaptcha')]")
        driver.switch_to.frame(iframe)

        # Click on the audio button
        try:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#recaptcha-audio-button"))
            ).click()
        except TimeoutException:
            raise TimeoutError("Failed to click audio button")

        time.sleep(1)

        # Wait for the audio source to load
        try:
            audio_source = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-source"))
            )
            src = audio_source.get_attribute("src")
        except TimeoutException:
            raise TimeoutError("Failed to load audio source")

        # Download the audio to the temp folder
        path_to_mp3 = f"{gettempdir()}/{str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))}.mp3"
        path_to_wav = f"{gettempdir()}/{str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))}.wav"
        
        urllib.request.urlretrieve(src, path_to_mp3)

        # Convert mp3 to wav
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")

        sample_audio = speech_recognition.AudioFile(path_to_wav)
        r = speech_recognition.Recognizer()

        try:
            with sample_audio as source:
                audio = r.record(source)
            # Recognize the audio
            key = r.recognize_google(audio)
        except (speech_recognition.exceptions.UnknownValueError, speech_recognition.exceptions.RequestError):
            raise Exception("Failed to recognize")

        # Input the key
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-response"))
            ).send_keys(key.lower())
        except TimeoutException:
            raise TimeoutError("Failed to input key")

        # Submit the key
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-response"))
            ).send_keys(Keys.RETURN)
        except TimeoutException:
            raise TimeoutError("Failed to submit key")

        # Wait for a short period to allow the recaptcha to process the input
        time.sleep(2)
        
        print("\033[34minfo\033[0m:Successfully bypassed recaptcha protection")
        
        # Delete temporary files
        try:
            os.remove(path_to_mp3)
            os.remove(path_to_wav)
        except Exception:
            raise Exception("Failed to delete temporary files")
        
    def solve_captcha(self, url:str):
        try:
            self.driver.get(url)
            self.recaptcha_service(self.driver)
            return self.driver
        except (Exception, TimeoutError) as err:
            print(f"\033[31merror\033[0m:Failed to bypass recaptcha protection \033[34mreason\033[0m:{err}")
            self.driver.quit()
            return None
