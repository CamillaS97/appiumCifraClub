import unittest
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Membros da equipe:
# Camilla Silvestre
# Eduardo Souza
# Helena Juliana
# Tainah Regueira
# Aplicativo escolhido para o teste: Cifra Club

# try catch para otimizar o WebDriverWait
def element_exist(driver, element):
   try:
       wait_time = 1
       WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(element))
       return True
   except:
       return False

# Configuração inicial do appium
class TestCifraClub(unittest.TestCase):
    def setUp(self):
        options = AppiumOptions()
        options.load_capabilities({
            "platformName": "Android",
            "appium:automationName": "uiautomator2",
        })
        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        self.wait_time = 10

# TearDown/Quit
    def tearDown(self):
        if self.driver:
            self.driver.quit()

# Teste 1 | Funcionalidade: barra de pesquisa | Cenário: deve buscar e acessar uma música (Hotel California)
    def test_01_search_song(self):
        # Acessa e clica na barra de pesquisa
        search_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Search")
        search_btn.click()
        # Digita o nome da música e clica no primeiro resultado
        element_exist(self.driver, (AppiumBy.CLASS_NAME, "android.widget.EditText"))
        self.driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText").send_keys("Hotel California")
        element_exist(self.driver, (AppiumBy.XPATH, '(//android.widget.RelativeLayout[@resource-id="com.studiosol.cifraclub:id/cellClickableArea"])[1]/android.widget.LinearLayout'))
        choose_song = self.driver.find_element(by=AppiumBy.XPATH,
                                  value='(//android.widget.RelativeLayout[@resource-id="com.studiosol.cifraclub:id/cellClickableArea"])[1]/android.widget.LinearLayout')
        choose_song.click()
        # Assert para garantir que a música foi de fato selecionada
        element_exist(self.driver, (AppiumBy.ID, 'com.studiosol.cifraclub:id/songListenLayout'))
        song_title = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Hotel California"]')
        self.assertEqual("Hotel California", song_title.text)

# Teste 2 | Funcionalidade: configurações da cifra | Cenário: deve alterar a posição do capotraste na cifra escolhida
    def test_02_change_capo(self):
        # Acessa a aba de configurações de uma cifra
        settings_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Settings")
        settings_btn.click()
        # Acessa o seletor de capotraste e seleciona a opção "1st fret" 
        capo_option = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,value='new UiSelector().text("Capo")')
        capo_option.click()
        element_exist(self.driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"1st fret\")"))
        fret_option = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                               value="new UiSelector().text(\"1st fret\")")
        fret_option.click()
        ok_btn = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/positiveBt")
        ok_btn.click()
        # Retorna à cifra
        settings_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Settings")
        settings_btn.click()
        # Assert para garantir que houve alteração de capotraste
        capo_check = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                              value="new UiSelector().text(\"Capo: 1st fret\")")
        self.assertEqual("Capo: 1st fret", capo_check.text)

# Teste 3 | Funcionalidade: configurações da cifra | Cenário: deve alterar o tom de uma cifra
    def test_03_change_tone(self):
        # Acessa a aba de configurações de uma cifra
        tone_options = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/songToneTxt")
        tone_options.click()
        # Acessa o seletor de tonalidade da cifra e seleciona a opção "TONE: E"
        element_exist(self.driver, (AppiumBy.ID, "com.studiosol.cifraclub:id/tone7"))
        chosen_tone = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/tone7")
        chosen_tone.click()
        ok_btn = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/positiveBt")
        ok_btn.click()
        # Assert para garantir alteração de tom
        updated_result = self.driver.find_element(by=AppiumBy.ID, value="com.studiosol.cifraclub:id/songToneTxt")
        self.assertEqual("TONE: E", updated_result.text)

# Teste 4 | Funcionalidade: barra de pesquisa | Cenário: deve limpar a barra de pesquisa
    def test_04_clear_search(self):
        # Acessa a barra de pesquisa e clica em "Clear history"
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

        # Checa tamanho da lista para garantir que está com len = 1, o que significa que a lista foi limpa
        list = self.driver.find_element(AppiumBy.ID, "com.studiosol.cifraclub:id/listView")
        child_elements = list.find_elements(AppiumBy.XPATH, ".//*")
        self.assertEqual(1, len(child_elements))
