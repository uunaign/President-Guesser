# --- ADIVINADOR DE PRESIDENTES ---

import pandas as pd
import os
import time

df = pd.read_csv('presidentes.csv')

bv = """
██████  ██ ███████ ███    ██ ██    ██ ███████ ███    ██ ██ ██████   ██████       █████           
██   ██ ██ ██      ████   ██ ██    ██ ██      ████   ██ ██ ██   ██ ██    ██     ██   ██          
██████  ██ █████   ██ ██  ██ ██    ██ █████   ██ ██  ██ ██ ██   ██ ██    ██     ███████          
██   ██ ██ ██      ██  ██ ██  ██  ██  ██      ██  ██ ██ ██ ██   ██ ██    ██     ██   ██          
██████  ██ ███████ ██   ████   ████   ███████ ██   ████ ██ ██████   ██████      ██   ██ ██ ██ ██ 
                                                                                                                                                                                                
"""
logo = """
██████  ██████  ███████ ███████ ██ ██████  ███████ ███    ██ ████████      ██████  ██    ██ ███████ ███████ ███████ ███████ ██████  
██   ██ ██   ██ ██      ██      ██ ██   ██ ██      ████   ██    ██        ██       ██    ██ ██      ██      ██      ██      ██   ██ 
██████  ██████  █████   ███████ ██ ██   ██ █████   ██ ██  ██    ██        ██   ███ ██    ██ █████   ███████ ███████ █████   ██████  
██      ██   ██ ██           ██ ██ ██   ██ ██      ██  ██ ██    ██        ██    ██ ██    ██ ██           ██      ██ ██      ██   ██ 
██      ██   ██ ███████ ███████ ██ ██████  ███████ ██   ████    ██         ██████   ██████  ███████ ███████ ███████ ███████ ██   ██ 
                                                                                                                                    
                                                                                                                                    
"""

# - colores -

RESET = "\033[0m"
ROJO    = "\033[31m"
VERDE   = "\033[32m"
AMARILLO = "\033[33m"
AZUL    = "\033[34m"
MAGENTA = "\033[35m"
CIAN    = "\033[36m"
BLANCO  = "\033[37m"

posibles = df.copy()

preguntas_dict = {
    "america_si": "¿Su personaje es del continente Americano?",
    "siglo_21": "¿Gobernó o ha gobernado principalmente en el siglo XXI?",
    "habla_castellano_si": "¿Su idioma nativo es el español?",
    "monarquia_si": "¿En su país existe o existía una monarquía (Rey/Reina)?",
    "militar_si": "¿Tiene o tuvo una carrera militar destacada?",
    "hombre_si": "¿Es un hombre?",
    "hemisferio_norte_si": "¿Su país se encuentra mayoritariamente en el hemisferio norte?",
    "gafas_si": "¿Es habitual o famoso por usar gafas?",
    "rubio_si": "¿Tiene el pelo rubio o muy claro?",
    "derechas_si": "¿Se le considera de tendencia política de derechas?",
    "asesinado_si": "¿Murió víctima de un asesinato o atentado?",
    "premio_nobel": "¿Ha ganado el Premio Nobel de la Paz?",
    "es_isla_si": "¿Su país es una isla o un archipiélago?",
    "partido_unico_si": "¿Gobernó bajo un sistema de partido único o dictadura?",
    "vello_facial_si": "¿Es famoso por tener barba, bigote o vello facial?",
    "edad_mayor_65": "¿Tenía o tiene más de 65 años en su momento de mayor poder (o actualmente)?",
    "continente_europa": "¿Es un líder de un país europeo?",
    "religion_mayoritaria_cristiana": "¿La religión mayoritaria de su país es el cristianismo?",
    "es_frances": "¿La persona en la que piensas preside en Francia?"

}

preguntas_hechas = []

def bienvenida():
    os.system('clear')
    print(VERDE + bv + RESET)
    time.sleep(1)
    os.system('clear')
    print(AMARILLO + logo + RESET)
    time.sleep(1)

def calcular_mejor_pregunta(df_actual, lista_preguntas_hechas):
    atributos_disponibles = [col for col in preguntas_dict.keys() if col not in lista_preguntas_hechas]
    if not atributos_disponibles:
        return None
    
    mejor_columna = ""
    min_distancia = float('inf')

    objetivo = len(df_actual) / 2

    for col in atributos_disponibles:
        conteo_si = df_actual[col].sum()
        distancia = abs(conteo_si - objetivo)
        if distancia < min_distancia:
            min_distancia = distancia
            mejor_columna = col

    return mejor_columna


bienvenida()

while len(posibles) > 1:
    #print(f"--- Candidatos restantes = {len(posibles)} ---")
    #print(posibles['nombre'].tolist())

    columna_a_preguntar = calcular_mejor_pregunta(posibles, preguntas_hechas)

    if not columna_a_preguntar:
        print("Me he quedado sin preguntas y no lo tengo claro")
        break

    texto = preguntas_dict[columna_a_preguntar]
    respuesta = input(f"{texto} (s/n): ").lower().strip()

    valor_buscado = 1 if respuesta == 's' else 0
    posibles = posibles[posibles[columna_a_preguntar] == valor_buscado]

    preguntas_hechas.append(columna_a_preguntar)

    if len(posibles) == 1:
        print(f"\n¡LO TENGO! Estas pensando en {posibles.iloc[0]['nombre']}")
    elif len(posibles) < 1:
        print("vaya, me he quedado sin ideas :( Seguro que has respondido todo correctamente?")
    else:
        print("\nContinuemos con la siguiente pregunta...")