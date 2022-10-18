import os

from dotenv import load_dotenv

import requests

from seleniumwire import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep


load_dotenv()

def interceptor(request):
    del request.headers["User-Agent"]
    request.headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"


slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
if not slack_webhook_url:
    raise Exception("Missing environment variable: SLACK_WEBHOOK_URL")

try:
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=opts)
    driver.request_interceptor = interceptor

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen")
    sleep(2.0)

    driver.find_element("link text", "Termin buchen").click()
    print("Termin Buchen")
    sleep(2.0)

    driver.find_element("id", "xi-cb-1").click()
    print(
        "Ich erkläre hiermit, die Informationen auf dieser Seite gelesen und verstanden zu haben. Mit der Nutzung dieses Service-Angebots erteile ich meine Zustimmung zur Erhebung und Nutzung meiner persönlichen Daten.*"
    )
    sleep(2.0)

    driver.find_element("id", "applicationForm:managedForm:proceed").click()
    print("Weiter")
    sleep(4.0)

    nationality = Select(driver.find_element("id", "xi-sel-400"))
    try:
        nationality.select_by_visible_text("Brasilien")
    except:
        nationality.select_by_visible_text("Brazil")
    print("Ich bin Brasilien")
    sleep(2.0)

    persons = Select(driver.find_element("id", "xi-sel-422"))
    persons.select_by_visible_text("eine Person")
    print("Nur mich")
    sleep(2.0)

    plusFamily = Select(driver.find_element("id", "xi-sel-427"))
    plusFamily.select_by_visible_text("nein")
    print("Kein familien")
    sleep(2.0)

    driver.find_element("id", "applicationForm:managedForm:proceed").click()
    print("Weiter")
    sleep(4.0)

    driver.find_element("class name", "kachel-327-0-1").click()
    print("Aufenthaltstitel - beantragen")
    sleep(3.0)

    driver.find_element("class name", "accordion-327-0-1-1").click()
    print("Erwerbstätigkeit")
    sleep(3.0)

    driver.find_element("id", "SERVICEWAHL_DE327-0-1-1-305304").click()
    print("Aufenthaltserlaubnis für Fachkräfte mit Berufsausbildung (§ 18a)")
    sleep(3.0)

    driver.find_element("id", "applicationForm:managedForm:proceed").click()
    print("Weiter")
    sleep(7.0)

    err = driver.find_element("class name", "errorMessage")
    if not err:
        requests.post(url=slack_webhook_url, data='{"text":"Available slot detected! Run to the PC!"}')
        print("Waiting for finishing the appointment")
    else:
        print(
            "Für die gewählte Dienstleistung sind aktuell keine Termine frei! Bitte versuchen Sie es zu einem späteren Zeitpunkt erneut."
        )
        driver.close()
except:
    driver.close()
