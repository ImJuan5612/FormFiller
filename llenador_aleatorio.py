from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time

# --- CONFIGURACIÓN ---
# El link del formulario de prueba (Cambiar por el link del formulario que se desea llenar)
URL_FORMULARIO = "https://forms.gle/sSrxPmvmyw79YNaa9" 
NUM_RESPUESTAS = 10 # Cuántas veces se desea enviar el formulario

# --- DEFINICIÓN DE PREGUNTAS ---
# Este formulario tiene 10 preguntas de opción múltiple con 3 opciones cada una [cite: 9-71].
# La lista usa tuplas: (Índice_Pregunta, Cantidad_Opciones, Tipo)
PREGUNTAS_A_LLENAR = [
    # Formato de tupla: (Num_Pregunta, Cantidad_Opciones, Tipo)
    (1, 3, 'radio'),
    (2, 3, 'radio'),
    (3, 3, 'radio'),
    (4, 3, 'radio'),
    (5, 3, 'checkbox'),
    (11, 3, 'radio'),
    (12, 3, 'radio'),
    (13, 3, 'radio'),
    (14, 3, 'checkbox'),
    (15, 3, 'radio'),
]

def llenar_formulario_aleatorio(driver):
    """Lógica para seleccionar una opción aleatoria para cada pregunta."""

    for indice_pregunta, num_opciones, tipo in PREGUNTAS_A_LLENAR:
        try:
            # 1. Selector Base: Busca el contenedor de la pregunta por su índice
            xpath_contenedor = f"(//form//div[starts-with(@role, 'listitem') or contains(@class, 'fvv-list-item')])[{indice_pregunta}]" 
            # f"(//div[@role='listitem'])[{indice_pregunta}]"
            
            # 2. SELECTOR RESILIENTE: Busca cualquier elemento que sea una opción clickeable.
            # Los elementos clickeables en Forms son a menudo div[@role='option'], div[@role='radio'] o div[@role='checkbox']
            
            if tipo in ['radio', 'checkbox']:
                # Intenta buscar el selector más genérico para la opción
                opciones_clickables = driver.find_elements(By.XPATH, f"{xpath_contenedor}//div[@role='option']")
                
                # Si no encuentra 'option', intenta buscar el selector específico (radio o checkbox)
                if not opciones_clickables:
                    opciones_clickables = driver.find_elements(By.XPATH, f"{xpath_contenedor}//div[@role='{tipo}']")
            else:
                continue
            
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
                
            print(f"Q{indice_pregunta}: Llenado aleatorio (Tipo: {tipo})")

        except Exception as e:
            print(f"Error grave al intentar llenar Q{indice_pregunta}: {type(e).__name__} - {e}")
            continue

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
            # 1. Abrir el formulario y maximizar (opcional)
            driver.get(URL_FORMULARIO)
            driver.maximize_window()
            time.sleep(random.uniform(2, 4)) 

            # 2. Llenar todas las preguntas aleatoriamente
            llenar_formulario_aleatorio(driver)

            # 3. Encontrar y hacer clic en el botón de Enviar
            # Buscamos el texto 'Enviar' dentro de un botón genérico
            boton_enviar = driver.find_element(By.XPATH, "//span[text()='Enviar']")
            
            # Usamos JavaScript para hacer clic, ya que es más confiable que el clic nativo de Selenium
            driver.execute_script("arguments[0].click();", boton_enviar.find_element(By.XPATH, './ancestor::div[@role="button"]'))
            
            print(f"Envío {i + 1} de {NUM_RESPUESTAS} completado.")

            # 4. PAUSA ANTIDETECCIÓN (CRUCIAL)
            pausa_aleatoria = random.randint(10, 25)
            print(f"Esperando {pausa_aleatoria} segundos para simular tiempo de lectura...")
            time.sleep(pausa_aleatoria)

        except Exception as e:
            print(f"Error grave durante el ciclo {i + 1}: {type(e).__name__} - {e}")
            # Si el formulario falla, esperamos más tiempo antes de reintentar
            time.sleep(30)
            continue
            
    driver.quit()
    print("Proceso de automatización finalizado.")

if __name__ == "__main__":
    automatizar_envios()