from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# URL del formulario
URL = "https://forms.gle/sSrxPmvmyw79YNaa9" # INSERTAR LA URL DEL FORMULARIO QUE SE LLENARÁ

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

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
            # "Al menos una, pero no todas"
            n = len(opciones)
            # Si n=1, elegimos 1. Si n>1, elegimos entre 1 y n-1.
            max_k = n - 1 if n > 1 else 1
            k = random.randint(1, max_k)
            
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

# --- Bloque principal ---
if __name__ == "__main__":
    try:
        n_veces = int(input("¿Cuántas veces deseas completar el formulario? "))
    except ValueError:
        print("Entrada no válida. Usando 1 vez por defecto.")
        n_veces = 1

    print(f"[INFO] Se ejecutará el robot {n_veces} veces.")

    for i in range(1, n_veces + 1):
        print(f"\n[INFO] >>> Iniciando iteración {i} de {n_veces} <<<")
        driver.get(URL)
        
        # Bucle para recorrer secciones de UNA iteración
        while True:
            responder_seccion()
            if click_siguiente():
                continue
            if click_enviar():
                print(f"[INFO] Formulario enviado (iteración {i}).")
                break
            print("[DEBUG] No hay más botones, fin del formulario (o error).")
            break
        
        # Espera entre iteraciones (si no es la última)
        if i < n_veces:
            espera = random.randint(15, 30)
            print(f"[INFO] Esperando {espera} segundos antes de la siguiente iteración...")
            time.sleep(espera)

    print("\n[INFO] Todas las iteraciones completadas.")
    time.sleep(3)
    driver.quit()
