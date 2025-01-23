import unittest
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def element_exist(driver, element):
   try:
       wait_time = 1
       WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(element))
       return True
   except:
       return False


class TestCifraClub(unittest.TestCase):
    def setUp(self):
        options = AppiumOptions()
        options.load_capabilities({
            "platformName": "Android",
            "appium:automationName": "uiautomator2",
        })
        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        self.wait_time = 10

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_01_search_song(self):
        search_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Search")
        search_btn.click()
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
        self.driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText").send_keys("Hotel California")
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.RelativeLayout[@resource-id="com.studiosol.cifraclub:id/cellClickableArea"])[1]/android.widget.LinearLayout')))
        choose_song = self.driver.find_element(by=AppiumBy.XPATH,
                                  value='(//android.widget.RelativeLayout[@resource-id="com.studiosol.cifraclub:id/cellClickableArea"])[1]/android.widget.LinearLayout')
        choose_song.click()
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((AppiumBy.ID, 'com.studiosol.cifraclub:id/songListenLayout')))
        song_title = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Hotel California"]')
        self.assertEqual("Hotel California", song_title.text)

    def test_02_clear_search(self):
        if not element_exist(self.driver, (AppiumBy.ACCESSIBILITY_ID, "Navigate up")):
            search_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Search")
            search_btn.click()
            if element_exist(self.driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Clear history\")")):
                clear_btn = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                               value="new UiSelector().text(\"Clear history\")")
                clear_btn.click()
        else:
            back_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Navigate up")
            back_btn.click()
            clear_search = self.driver.find_element(by=AppiumBy.XPATH,
                                      value='//android.view.ViewGroup[@resource-id="com.studiosol.cifraclub:id/toolbar"]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView')
            clear_search.click()
            clear_btn = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Clear history\")")
            clear_btn.click()

        list = self.driver.find_element(AppiumBy.ID, "com.studiosol.cifraclub:id/listView")
        child_elements = list.find_elements(AppiumBy.XPATH, ".//*")
        #Obs: printa um que eh o proprio listview, significa que a lista esta vazia
        self.assertEqual(1, len(child_elements))

    def test_03_change_capo(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
        self.driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText").send_keys("Hotel California")
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.RelativeLayout[@resource-id="com.studiosol.cifraclub:id/cellClickableArea"])[1]/android.widget.LinearLayout')))
        choose_song = self.driver.find_element(by=AppiumBy.XPATH,
                                value='(//android.widget.RelativeLayout[@resource-id="com.studiosol.cifraclub:id/cellClickableArea"])[1]/android.widget.LinearLayout')
        choose_song.click()
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((AppiumBy.ID, 'com.studiosol.cifraclub:id/songListenLayout')))
        settings_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Settings")
        settings_btn.click()
        capo_option = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,value='new UiSelector().text("Capo")')
        capo_option.click()
        WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"1st fret\")")))
        fret_option = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                               value="new UiSelector().text(\"1st fret\")")
        fret_option.click()
        ok_btn = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/positiveBt")
        ok_btn.click()
        settings_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Settings")
        settings_btn.click()
        capo_check = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                              value="new UiSelector().text(\"Capo: 1st fret\")")
        self.assertEqual("Capo: 1st fret", capo_check.text)

    def test_04_change_tone(self):
        tone_options = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/songToneTxt")
        tone_options.click()
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((AppiumBy.ID, "com.studiosol.cifraclub:id/tone7")))
        chosen_tone = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/tone7")
        chosen_tone.click()
        ok_btn = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/positiveBt")
        ok_btn.click()
        updated_result = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/songToneTxt")
        self.assertEqual("TONE: E", updated_result.text)
