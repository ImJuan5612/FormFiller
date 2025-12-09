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
# La lista usa tuplas: (Índice_Pregunta, Cantidad_Opciones)
PREGUNTAS_A_LLENAR = [
    # Formato de tupla: (Num_Pregunta, Cantidad_Opciones)
    (1, 3),
    (2, 3),
    (3, 3),
    (4, 3),
    (5, 3),
    (6, 3),
    (7, 3),
    (8, 3),
    (9, 3),
    (10, 3),
]


def llenar_formulario_aleatorio(driver):
    """Lógica para seleccionar una opción aleatoria para cada pregunta."""
    
    # XPath general que busca todos los contenedores de preguntas listados
    xpath_contenedor_base = "//div[@role='listitem']"

    for indice, (num_opciones_declaradas) in enumerate(PREGUNTAS_A_LLENAR):
        # El índice de la pregunta en el DOM empieza en 1, por eso usamos (indice + 1)
        indice_pregunta_dom = indice + 1

        try:
            # 1. Selector de la Pregunta Específica: Busca el contenedor [div] de la pregunta por su posición
            xpath_pregunta = f"{xpath_contenedor_base}[{indice_pregunta_dom}]"
            
            # 2. Selector de Opciones: Busca los elementos clickeables (div[@role='radio']) dentro de esa pregunta
            opciones_clickables = driver.find_elements(By.XPATH, f"{xpath_pregunta}//div[@role='radio']")
            
            if not opciones_clickables:
                 raise ValueError("No se encontraron opciones clickeables (radio buttons).")

            num_opciones_reales = len(opciones_clickables)
            
            # Verificación de que el número de opciones coincida con el declarado
            if num_opciones_reales != num_opciones_declaradas:
                 print(f"Advertencia Q{indice_pregunta_dom}: Esperaba {num_opciones_declaradas} opciones, encontré {num_opciones_reales}. Ajustando.")
            
            # --- LÓGICA DE ALEATORIEDAD ---
            # Selecciona un índice aleatorio entre 0 y el número de opciones encontradas
            indice_aleatorio = random.randint(0, num_opciones_reales - 1)
            
            # Simula el clic en el elemento clickeable seleccionado al azar
            opciones_clickables[indice_aleatorio].click()
            
            # Pausa breve entre preguntas para simular tiempo de lectura
            time.sleep(random.uniform(0.1, 0.3)) 
            
            print(f"Q{indice_pregunta_dom}: Seleccionada opción {indice_aleatorio + 1} de {num_opciones_reales}")

        except Exception as e:
            print(f"Error grave al llenar Q{indice_pregunta_dom}: {type(e).__name__} - {e}")
            # Continuar con la siguiente pregunta si falla una


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