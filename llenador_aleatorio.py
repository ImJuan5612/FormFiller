from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import random
import time

# El código buscará e instalará ChromeDriver automáticamente
driver = webdriver.Chrome()
# ... o si prefieres Firefox
# driver = webdriver.Firefox()

# --- CONFIGURACIÓN ---
URL_FORMULARIO = "https://forms.gle/sSrxPmvmyw79YNaa9"
NUM_RESPUESTAS = 10 # Cuántas veces quieres enviar el formulario
# Ruta a tu WebDriver (si no está en el PATH del sistema)
# PATH_DRIVER = "C:/Ruta/a/chromedriver.exe"


# --- DEFINICIÓN DE PREGUNTAS Y OPCIONES ---
# Lista de tuplas: (XPath base para todas las opciones, Cantidad total de opciones)
# EJEMPLOS BASADOS EN TU PDF (¡DEBES OBTENER LOS XPATHS REALES!)
PREGUNTAS_A_LLENAR = [
    # Q1. Sexo (Mujer, Hombre) -> 2 opciones
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div/span/div", 3),
    # Q2. Edad (18 a 29, 30 a 39, ..., 60 y más) -> 5 opciones
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/div/span/div", 3),
    # Q3. Discapacidad (Casillas de verificación) -> 6 opciones
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div[1]/div/span/div", 3),
    # Q4. Soporte económico (Sí, No) -> 2 opciones
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div[1]/div/span/div", 3),
    # Q5. Oportunidades (Nunca, Algunas veces, ..., No aplica) -> 5 opciones
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div[1]", 3),
    # Q6. Oportunidades (Nunca, Algunas veces, ..., No aplica) -> 5 opciones
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[6]/div/div/div[2]/div[1]/div/span/div", 3),
    # Q7. Oportunidades (Nunca, Algunas veces, ..., No aplica) -> 5 opciones
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[7]/div/div/div[2]/div[1]/div/span/div", 3),
    # Q8
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[8]/div/div/div[2]/div[1]/div/span/div", 3),
    # Q9
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[9]/div/div/div[2]/div[1]", 3),
    # Q10
    ("/html/body/div/div[3]/form/div[2]/div/div[2]/div[10]/div/div/div[2]/div[1]/div/span/div", 3),
    # NOTA: Los índices de las preguntas continuarán hasta la 72.
]

def llenar_formulario_aleatorio(driver):
    """Lógica para seleccionar una opción aleatoria para cada pregunta."""

    for i, (xpath_base, num_opciones) in enumerate(PREGUNTAS_A_LLENAR):
        # 1. Encontrar todas las opciones posibles para esta pregunta
        opciones = driver.find_elements(By.XPATH, f"{xpath_base}/div") # Busca las opciones dentro del contenedor
        
        if not opciones:
            print(f"Advertencia: No se encontraron opciones para la pregunta {i+1}.")
            continue

        # --- LÓGICA DE ALEATORIEDAD ---
        if 'checkbox' in xpath_base:
            # Preguntas de Casillas de Verificación (Puede marcar varias o ninguna)
            for opcion in opciones:
                if random.random() > 0.6: # 40% de probabilidad de marcar
                    opcion.click()
                    time.sleep(0.2) # Pausa breve para simular el click
        else:
            # Preguntas de Opción Múltiple (Radio Button)
            indice_aleatorio = random.randint(0, len(opciones) - 1)
            opciones[indice_aleatorio].click()
            
            # Pausa muy breve entre preguntas para evitar ser detectado
            time.sleep(random.uniform(0.5, 1.5))


def automatizar_envios():
    """Bucle principal para controlar la automatización y evitar el bloqueo."""
    
    # Inicializar el navegador
    # service = webdriver.ChromeService(executable_path=PATH_DRIVER)
    # Recomendación: Usar un User Agent normal para evitar ser detectado
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    
    print(f"Iniciando el envío de {NUM_RESPUESTAS} respuestas aleatorias...")

    for i in range(NUM_RESPUESTAS):
        try:
            # 1. Abrir el formulario
            driver.get(URL_FORMULARIO)
            # Esperar a que la página cargue completamente
            time.sleep(random.uniform(2, 4)) 

            # 2. Llenar todas las preguntas
            llenar_formulario_aleatorio(driver)

            # 3. Encontrar y hacer clic en el botón de Enviar
            # (El selector del botón de Enviar suele ser: div[role="button"][jsname="RgeWac"])
            boton_enviar = driver.find_element(By.XPATH, "//span[text()='Enviar']/parent::*")
            boton_enviar.click()
            
            print(f"Envío {i + 1} de {NUM_RESPUESTAS} completado.")

            # 4. PAUSA ANTIDETECCIÓN (CRUCIAL)
            # Esperar un tiempo significativo e irregular (ej., 10 a 25 segundos)
            pausa_aleatoria = random.randint(10, 25)
            print(f"Esperando {pausa_aleatoria} segundos para simular tiempo de lectura...")
            time.sleep(pausa_aleatoria)

        except Exception as e:
            print(f"Error durante el ciclo {i + 1}: {e}")
            time.sleep(30)
            continue
            
    driver.quit()
    print("Proceso de automatización finalizado.")

if __name__ == "__main__":
    automatizar_envios()