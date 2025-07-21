import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plyer import notification
import platform
import os

# Configuration
URL = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=5.2286902_43.3910329_5.5324758_43.1696205"
# checks every 30 seconds   
CHECK_INTERVAL = 30  
ALARM_SOUND = "alarm.wav"  # Path to your alarm sound

# SUisng headleass mode for chrome
def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service()  # Make sure chromedriver is in your PATH
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# this function plays the alarm sound in a loop until the user stops it
def play_alarm_loop():
    print("Alarm started! Press Enter to stop.")
    while True:
        play_alarm_once()
        time.sleep(2)
        if input(" Press Enter to stop the alarm...") == "":
            break

def play_alarm_once():
    system = platform.system()
    if system == "Windows":
        import winsound
        winsound.PlaySound(ALARM_SOUND, winsound.SND_FILENAME)
    elif system == "Darwin":
        os.system(f"afplay {ALARM_SOUND}")
    elif system == "Linux":
        os.system(f"aplay {ALARM_SOUND}")
    else:
        print(" Unsupported OS for alarm sound.")

# Shows desktop notification
def send_notification(title, message):
    notification.notify(title=title, message=message, timeout=10)

# Check for availability
def check_availability(driver):
    driver.get(URL)
    try:
        heading = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.SearchResults-desktop"))
        )
        text = heading.text.strip().lower()
        print(" Heading text:", text)

        if "aucun logement trouvé" in text:
            print(" No housing available.")
            return False
        elif "logement" in text and "trouvé" in text:
            print("Housing available!")
            return True
        else:
            print("Unexpected heading content. Defaulting to no housing.")
            return False

    except Exception as e:
        print("Error checking housing:", e)
        return False

# Main loop
def main():
    driver = setup_driver()
    print(" Monitoring started...")
    try:
        while True:
            if check_availability(driver):
                message = f"Housing is available!\nCheck: {URL}"
                send_notification(" CROUS Housing Alert", message)
                play_alarm_loop()
                break
            time.sleep(CHECK_INTERVAL)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
