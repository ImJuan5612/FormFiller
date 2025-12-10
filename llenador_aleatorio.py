from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

URL = "https://forms.gle/sSrxPmvmyw79YNaa9"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get(URL)

def responder_seccion():
    print("\n[DEBUG] === NUEVA SECCIÓN ===")

    time.sleep(1)

    # Radio groups
    radios = driver.find_elements(By.CSS_SELECTOR, "div[role='radiogroup']")
    print(f"[DEBUG] Radios encontrados: {len(radios)}")

    for idx, group in enumerate(radios, start=1):
        opciones = group.find_elements(By.CSS_SELECTOR, "div[role='radio']")
        print(f"[DEBUG]   Pregunta radio #{idx} → {len(opciones)} opciones")

        if opciones:
            opcion = random.choice(opciones)
            driver.execute_script("arguments[0].click();", opcion)

    # Checkbox groups
    checks = driver.find_elements(By.CSS_SELECTOR, "div[role='group'], div[role='list']")
    print(f"[DEBUG] Checkboxes encontrados: {len(checks)}")

    for idx, group in enumerate(checks, start=1):
        opciones = group.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
        print(f"[DEBUG]   Pregunta checkbox #{idx} → {len(opciones)} opciones")

        if opciones:
            # Selección aleatoria de 1 a n
            k = random.randint(1, len(opciones))
            seleccion = random.sample(opciones, k)
            for opcion in seleccion:
                driver.execute_script("arguments[0].click();", opcion)

def click_siguiente():
    botones = driver.find_elements(By.CSS_SELECTOR, "div[role='button']")
    for b in botones:
        txt = b.text.lower().strip()
        if "siguiente" in txt or "next" in txt:
            print("[DEBUG] Clic en botón SIGUIENTE")
            driver.execute_script("arguments[0].click();", b)
            time.sleep(1)
            return True
    return False

def click_enviar():
    botones = driver.find_elements(By.CSS_SELECTOR, "div[role='button']")
    for b in botones:
        if "enviar" in b.text.lower():
            print("[DEBUG] Clic en ENVIAR")
            driver.execute_script("arguments[0].click();", b)
            time.sleep(1)
            return True
    return False

# Bucle principal para recorrer todas las secciones
while True:
    responder_seccion()
    if click_siguiente():
        continue
    if click_enviar():
        break
    print("[DEBUG] No hay más botones, fin.")
    break

print("\n[DEBUG] Formulario completado.")
time.sleep(3)
driver.quit()
