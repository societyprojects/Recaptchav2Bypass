#!/usr/bin/env python3

import os
import time
import pydub
import urllib
import speech_recognition

from tempfile import gettempdir
from datetime import datetime

import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver import ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SeleniumDriver:

    """
    The SeleniumDriver class is designed to manage the creation and configuration of a Selenium WebDriver instance for automated web browsing. 
    It utilizes undetected-chromedriver (uc) to handle interactions with Chrome in a way that minimizes the chance of detection by websites using anti-bot mechanisms.

    Key Features:

        1. Initialization (__init__):

            * The class accepts a headless_mode argument that determines whether the browser will run in headless mode (without a visible UI).
            * Initializes a driver attribute set to None at the start.

        2. Context Manager (__enter__):

            * When entering the context (via a with statement), the class configures the Chrome browser by setting up ChromeService with an automatically downloaded driver using ChromeDriverManager.
            * Configures the Chrome options for the WebDriver:

                - Disables automation flags to avoid detection (--disable-blink-features=AutomationControlled).
                - Disables unnecessary features like extensions and GPU usage for better performance.
                - Sets a custom user-agent string (likely to simulate a real browser environment).
                - Optionally enables headless mode based on the headless_mode flag.
                - Creates a Chrome WebDriver instance (uc.Chrome), applies the configurations, and sets a page load timeout of 10 seconds.
                - Returns the WebDriver instance for use within the with block.

        3. Exit (__exit__):

            * The __exit__ method is a placeholder that ensures proper cleanup and exit behavior when leaving the context. 
              Currently, it does nothing but could be expanded for proper resource management (e.g. closing the driver).
              
    """

    def __init__(self, headless_mode:bool):
        self.headless = headless_mode
        self.driver = None

    def __enter__(self):
        chrome_service = ChromeService(ChromeDriverManager().install())

        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument(f"--user-agent={random_agent}")

        if self.headless:
            options.add_argument("--headless=new")

        self.driver = uc.Chrome(service=chrome_service, options=options)
        self.driver.set_page_load_timeout(10)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Recaptchav2Bypass:

    """
    The Recaptchav2Bypass class is an advanced solution for bypassing reCAPTCHA v2 challenges, specifically designed for handling audio-based CAPTCHAs. 
    Using Selenium, undetected-chromedriver, and various media-processing libraries, it automates the process of solving the CAPTCHA by downloading, converting, and transcribing audio challenges. 
    The class also incorporates detailed logging, debugging, and error handling to ensure smooth and efficient operation, even in environments with strict bot protection.

    Key Features:
    
        1. Initialization (__init__):

            * The class is initialized with debug and headless_mode flags, allowing control over the debugging output and 
              whether the browser runs in headless mode (without a visible UI).
            * It also initializes instances of Console and Reports to handle logging and reporting during execution.

        2. reCAPTCHA Handling (recaptcha_service):

            * This asynchronous method automates the process of solving a reCAPTCHA by interacting with the CAPTCHA iframe, clicking the checkbox, and navigating through the audio challenge.
            * The method performs several actions in sequence:

                - Switching to the reCAPTCHA iframe.
                - Clicking the reCAPTCHA checkbox and waiting for it to become clickable.
                - Switching back to the default frame.
                - Locating the audio challenge iframe and clicking the audio button.
                - Retrieving the audio source URL.
                - Downloading, converting, and decoding the audio to extract the CAPTCHA key.
                - Entering the transcribed key and submitting the response.

        3. Audio CAPTCHA Processing:

            * The handle_audio_captcha method is responsible for downloading the audio file, converting it from MP3 to WAV format, and 
              decoding it to extract the text. The transcription is handled using the speech_recognition library.
            * Temporary files (MP3 and WAV) are cleaned up after processing to ensure no unnecessary files remain on the system.

        4. Audio Download and Conversion:

            * The download_audio method downloads the audio file to a temporary directory.
            * The convert_mp3_to_wav method converts the downloaded MP3 audio to WAV format using the pydub library.

        5. Transcription and Cleanup:

            * The audio is transcribed using the Google Speech Recognition API. If transcription fails, appropriate exceptions are raised.
            * Temporary audio files are cleaned up after the process, ensuring proper resource management.

        6. Error Handling:

            * If any CAPTCHA challenge cannot be completed, or if the IP address is blocked, relevant error messages are logged and displayed. 
              The system gracefully handles exceptions like NoSuchElementException and TimeoutException, ensuring robust operation.

        7. IP Blocking Detection (is_blocked):

            * This method checks if the IP address has been blocked by detecting the "captcha body text" indicating a block. 
              It helps in identifying if reCAPTCHA protection is preventing further attempts.

        8. Solve CAPTCHA (solve_captcha):

            * This asynchronous method accepts a URL, launches a Selenium WebDriver, and 
              attempts to solve the CAPTCHA on the page using the previously mentioned methods.
            * The process is wrapped in a try-except block to handle errors gracefully, with reports and console logs to provide real-time feedback.

    """

    def __init__(self, headless_mode:bool):
        self.headless = headless_mode
        self.wait = None
    
    async def recaptcha_service(self, driver):
        # Switching to iframe containing reCAPTCHA
        try:
            iframe_inner = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
            driver.switch_to.frame(iframe_inner)
        except NoSuchElementException:
            raise GodorkException("Failed to locate reCAPTCHA iframe element")

        time.sleep(1)

        # Clicking the reCAPTCHA checkbox
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".rc-anchor-content"))
            ).click()
        except TimeoutException:
            raise TimeoutError("Failed to click reCAPTCHA checkbox")

        # Switch back to the default frame
        driver.switch_to.default_content()

        time.sleep(1)

        # Locating audio challenge iframe
        try:
            iframe = driver.find_element(By.XPATH, "//iframe[contains(@title, 'recaptcha')]")
            driver.switch_to.frame(iframe)
        except NoSuchElementException:
            raise Exception("Failed to locate reCAPTCHA iframe element")

        try:
            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#recaptcha-audio-button"))
            ).click()
        except TimeoutException:
            raise TimeoutError("Failed to click audio button")

        time.sleep(1)

        # Wait for the audio source to load
        try:
            audio_source = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-source"))
            )
            src = audio_source.get_attribute("src")
        except TimeoutException:
            raise TimeoutError("Failed to load audio source")

        # Download, convert, and decode audio reCAPTCHA
        try:
            key = await self.handle_audio_captcha(src)
        except (speech_recognition.exceptions.UnknownValueError, speech_recognition.exceptions.RequestError):
            raise Exception("Failed to recognize")

        # Input the key
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-response"))
            ).send_keys(key.lower())
        except TimeoutException:
            raise TimeoutError("Failed to input key")

        # Submit the key
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#audio-response"))
            ).send_keys(Keys.RETURN)
        except TimeoutException:
            raise TimeoutError("Failed to submit key")

        # Waiting briefly for reCAPTCHA to process the input
        time.sleep(4)

        if self.is_blocked(driver):
            return

        print("Successfully bypassed v2 protection")
    
    async def handle_audio_captcha(self, src_url):
        """Main handler to download, convert and decode audio CAPTCHA"""
        mp3_path, wav_path = self.get_temp_audio_paths()

        self.download_audio(src_url, mp3_path)
        self.convert_mp3_to_wav(mp3_path, wav_path)

        try:
            phrase = await self.async_decode_audio(wav_path)
        finally:
            # Delete temporary files
            self.cleanup_temp_files(mp3_path, wav_path)

        return phrase
    
    def download_audio(self, src, save_path):
        urllib.request.urlretrieve(src, save_path)

    def convert_mp3_to_wav(self, mp3_path, wav_path):
        sound = pydub.AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")

    async def async_decode_audio(self, wav_path):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.decode_audio, wav_path)
    
    def decode_audio(self, wav_path):
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)

    def cleanup_temp_files(self, *paths):
        for path in paths:
            try:
                os.remove(path)
            except Exception as e:
                print(f"Failed to delete {path}: {e}")

    def get_temp_audio_paths(self):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        mp3 = os.path.join(gettempdir(), f"{timestamp}.mp3")
        wav = os.path.join(gettempdir(), f"{timestamp}.wav")

        return mp3, wav

    def get_text_blocked(self, driver):
        try:
            recaptcha_header = driver.find_element(By.CLASS_NAME, "rc-doscaptcha-body-text")
            return recaptcha_header
        except NoSuchElementException:
            return None

    def is_blocked(self, driver):
        blocked = self.get_text_blocked(driver)
        if blocked is not None:
            print(f"Failed to bypass v2 protection. IP has been blocked! {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:{blocked.text}")

        if driver.current_url == "https://www.google.com/sorry/index":
            print("Unexpected response comes from search engines")
    
    async def solve_captcha(self, url):
        with SeleniumDriver(headless_mode=self.headless) as driver:
            self.wait = WebDriverWait(driver, 5)

            try:
                driver.get(url)
                await self.recaptcha_service(driver)
                return driver
            except KeyboardInterrupt:
                driver.quit()
            except (Exception, TimeoutError) as err:
                print(f"Failed to bypass v2 protection. {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:{err}")
