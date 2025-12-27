from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


driver.get("https://www.sunbeaminfo.in/internship")
driver.implicitly_wait(10)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

plus_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//a[@href='#collapseSix']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", plus_btn)
plus_btn.click()


rows = driver.find_element(By.ID, "collapseSix") \
             .find_element(By.TAG_NAME, "tbody") \
             .find_elements(By.TAG_NAME, "tr")[1:]

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    data.append({
        "Technology": cols[0].text.strip(),
        "Aim": cols[1].text.strip(),
        "Prerequisite": cols[2].text.strip(),
        "Learning": cols[3].text.strip(),
        "Location": cols[4].text.strip()
    })


pd.DataFrame(data).to_csv("internship_programs_info.csv", index=False)
driver.quit()
