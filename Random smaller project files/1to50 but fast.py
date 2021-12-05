from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = Chrome(executable_path='Bigger personal projects\\Selenium chrome drivers\\chromedriver.exe')

driver.get('http://zzzscore.com/1to50')
myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@style='z-index:99']")))
print("Done Waiting!")

button_num = 99
for i in range(50):
    current_num = driver.find_element_by_xpath("//span[@style='z-index:{}']".format(button_num))
    current_num.click()
    button_num -= 1

print("Buttons Clicked!")