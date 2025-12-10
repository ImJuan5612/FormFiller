from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# --- CONFIGURACIÓN ---
# El link del formulario de prueba (Cambiar por el link del formulario que se desea llenar)
URL_FORMULARIO = "https://forms.gle/sSrxPmvmyw79YNaa9" 
NUM_RESPUESTAS = 1 # Cuántas veces se desea enviar el formulario

# --- DEFINICIÓN DE PREGUNTAS POR PÁGINA ---
# El formulario tiene 3 páginas. Cada tupla es: (Índice_Relativo, Cantidad_Opciones, Tipo)
# Índice_Relativo es la posición de la pregunta en ESA página específica (1, 2, 3...)

# Página 1: Preguntas 1-4
PAGINA_1 = [
    (1, 3, 'radio'),  # Pregunta 1
    (2, 3, 'radio'),  # Pregunta 2
    (3, 3, 'radio'),  # Pregunta 3
]

# Página 2: Preguntas 5-7
PAGINA_2 = [
    (1, 3, 'radio'),  # Pregunta 4
    (2, 3, 'checkbox'),  # Pregunta 5
    (3, 3, 'radio'),     # Pregunta 6
    (4, 3, 'radio'),     # Pregunta 7
]

# Página 3: Preguntas 8-10
PAGINA_3 = [
    (1, 3, 'radio'),     # Pregunta 8
    (2, 3, 'checkbox'),  # Pregunta 9
    (3, 3, 'radio'),     # Pregunta 10
]

def llenar_preguntas_de_pagina(driver, preguntas, num_pagina):
    """Lógica para seleccionar una opción aleatoria para cada pregunta de una página específica."""
    
    # Esperar a que el formulario esté completamente cargado
    wait = WebDriverWait(driver, 10)
    
    for indice_pregunta, num_opciones, tipo in preguntas:
        try:
            print(f"  [DEBUG] Buscando pregunta {indice_pregunta} en página {num_pagina}...")
            
            # 1. Selector Base SIMPLIFICADO: Busca el contenedor de la pregunta por su índice RELATIVO
            xpath_contenedor = f"(//div[@role='listitem'])[{indice_pregunta}]"
            
            # Esperar a que el contenedor esté presente
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, xpath_contenedor)))
            except:
                print(f"  [DEBUG] Contenedor no encontrado con XPath: {xpath_contenedor}")
                # Intentar con el XPath alternativo más amplio
                xpath_contenedor = f"(//div[@role='listitem' or @role='list'])[{indice_pregunta}]"
            
            # 2. SELECTOR RESILIENTE: Busca cualquier elemento que sea una opción clickeable.
            # Primero intenta con role específico del tipo de pregunta
            opciones_clickables = driver.find_elements(By.XPATH, f"{xpath_contenedor}//div[@role='{tipo}']")
            
            print(f"  [DEBUG] Opciones encontradas con role='{tipo}': {len(opciones_clickables)}")
            
            # Si no encuentra con el tipo específico, intenta con 'option' genérico
            if not opciones_clickables:
                opciones_clickables = driver.find_elements(By.XPATH, f"{xpath_contenedor}//div[@role='option']")
                print(f"  [DEBUG] Opciones encontradas con role='option': {len(opciones_clickables)}")
            
            if not opciones_clickables:
                raise ValueError("No se encontraron elementos clickeables para la pregunta.")

            num_opciones_reales = len(opciones_clickables)
            
            # --- LÓGICA DE ALEATORIEDAD ---
            if tipo == 'checkbox':
                # Casillas: Marca aleatoriamente algunas
                seleccionadas = 0
                for opcion in opciones_clickables:
                    # 40% de probabilidad de marcar
                    if random.random() > 0.6: 
                        opcion.click()
                        seleccionadas += 1
                        time.sleep(0.1) 
                
                # Para preguntas obligatorias: si no se marcó nada, marca la última opción
                if seleccionadas == 0 and num_opciones_reales > 0:
                     opciones_clickables[-1].click()
                     
            else:
                # Opción Múltiple: Selecciona solo una al azar
                indice_aleatorio = random.randint(0, num_opciones_reales - 1)
                opciones_clickables[indice_aleatorio].click()
                time.sleep(random.uniform(0.1, 0.3)) 
                
            print(f"Página {num_pagina}, Q{indice_pregunta}: Llenado aleatorio (Tipo: {tipo})")

        except Exception as e:
            print(f"Error al llenar Página {num_pagina}, Q{indice_pregunta}: {type(e).__name__} - {e}")
            continue

def hacer_clic_boton_siguiente(driver):
    """Hace clic en el botón 'Siguiente' para avanzar a la siguiente página."""
    try:
        # Buscar el botón "Siguiente" por el texto del span
        boton_siguiente = driver.find_element(By.XPATH, "//span[text()='Siguiente']")
        # Encontrar el div padre con role='button' y hacer clic
        boton_div = boton_siguiente.find_element(By.XPATH, './ancestor::div[@role="button"]')
        driver.execute_script("arguments[0].click();", boton_div)
        print("[OK] Boton 'Siguiente' clickeado")
        # IMPORTANTE: Esperar más tiempo para que el DOM de la nueva página se cargue completamente
        time.sleep(random.uniform(3, 4))
        return True
    except Exception as e:
        print(f"Error al hacer clic en 'Siguiente': {type(e).__name__} - {e}")
        return False

def hacer_clic_boton_enviar(driver):
    """Hace clic en el botón 'Enviar' en la última página."""
    try:
        # Buscar el botón "Enviar" por el texto del span
        boton_enviar = driver.find_element(By.XPATH, "//span[text()='Enviar']")
        # Encontrar el div padre con role='button' y hacer clic
        boton_div = boton_enviar.find_element(By.XPATH, './ancestor::div[@role="button"]')
        driver.execute_script("arguments[0].click();", boton_div)
        print("[OK] Boton 'Enviar' clickeado")
        time.sleep(random.uniform(1, 2))
        return True
    except Exception as e:
        print(f"Error al hacer clic en 'Enviar': {type(e).__name__} - {e}")
        return False

def llenar_formulario_completo(driver):
    """Llena todas las páginas del formulario."""
    
    # PÁGINA 1
    print("\n=== Llenando Página 1 ===")
    llenar_preguntas_de_pagina(driver, PAGINA_1, 1)
    if not hacer_clic_boton_siguiente(driver):
        raise Exception("No se pudo avanzar de la Página 1")
    
    # PÁGINA 2
    print("\n=== Llenando Página 2 ===")
    llenar_preguntas_de_pagina(driver, PAGINA_2, 2)
    if not hacer_clic_boton_siguiente(driver):
        raise Exception("No se pudo avanzar de la Página 2")
    
    # PÁGINA 3
    print("\n=== Llenando Página 3 ===")
    llenar_preguntas_de_pagina(driver, PAGINA_3, 3)
    if not hacer_clic_boton_enviar(driver):
        raise Exception("No se pudo enviar el formulario")

def automatizar_envios():
    """Bucle principal para controlar la automatización y evitar el bloqueo."""
    
    # Inicialización Simplificada
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
    
    # Inicialización automática con Selenium Manager
    driver = webdriver.Chrome(options=options)
    
    print(f"Iniciando el envío de {NUM_RESPUESTAS} respuestas aleatorias...")

    for i in range(NUM_RESPUESTAS):
        try:
            print(f"\n{'='*60}")
            print(f"ENVÍO {i + 1} DE {NUM_RESPUESTAS}")
            print(f"{'='*60}")
            
            # 1. Abrir el formulario y maximizar (opcional)
            driver.get(URL_FORMULARIO)
            # driver.maximize_window()
            time.sleep(random.uniform(2, 4)) 

            # 2. Llenar todas las páginas del formulario
            llenar_formulario_completo(driver)

            print(f"\n[OK] Envio {i + 1} de {NUM_RESPUESTAS} completado exitosamente.")

            # 3. PAUSA ANTIDETECCIÓN (CRUCIAL)
            pausa_aleatoria = random.randint(10, 25)
            print(f"[WAIT] Esperando {pausa_aleatoria} segundos para simular tiempo de lectura...")
            time.sleep(pausa_aleatoria)

        except Exception as e:
            print(f"\n[ERROR] Error grave durante el envio {i + 1}: {type(e).__name__} - {e}")
            # Si el formulario falla, esperamos más tiempo antes de reintentar
            time.sleep(30)
            continue
            
    driver.quit()
    print("\n" + "="*60)
    print("[OK] Proceso de automatizacion finalizado.")
    print("="*60)

if __name__ == "__main__":
    automatizar_envios()