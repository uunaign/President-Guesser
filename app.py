import pandas as pd
import gradio as gr

# --- CONFIGURACIÓN DE DATOS ---
df = pd.read_csv('presidentes.csv')

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

# --- LÓGICA DEL JUEGO ---

def calcular_mejor_pregunta(df_actual, lista_preguntas_hechas):
    atributos_disponibles = [col for col in preguntas_dict.keys() if col not in lista_preguntas_hechas]
    if not atributos_disponibles or len(df_actual) <= 1:
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

def jugar(respuesta, historial_df, preguntas_hechas, columna_actual):
    # Convertir el historial de nuevo a DataFrame
    posibles = pd.DataFrame(historial_df)
    
    # Si hay una pregunta activa, filtrar según la respuesta del usuario
    if columna_actual:
        valor_buscado = 1 if respuesta == "Sí" else 0
        posibles = posibles[posibles[columna_actual] == valor_buscado]
        preguntas_hechas.append(columna_actual)

    # Comprobar estado del juego
    if len(posibles) == 1:
        nombre = posibles.iloc[0]['nombre']
        return f"¡LO TENGO! Estás pensando en: {nombre}", [], [], None, gr.update(visible=False), gr.update(visible=True)
    
    if len(posibles) == 0:
        return "Vaya, me he quedado sin ideas. ¿Seguro que respondiste correctamente?", [], [], None, gr.update(visible=False), gr.update(visible=True)

    # Buscar la siguiente pregunta
    siguiente_columna = calcular_mejor_pregunta(posibles, preguntas_hechas)
    
    if not siguiente_columna:
        nombres = ", ".join(posibles['nombre'].tolist())
        return f"No puedo decidirme, podría ser: {nombres}", [], [], None, gr.update(visible=False), gr.update(visible=True)

    texto_pregunta = preguntas_dict[siguiente_columna]
    
    # Devolver estado actualizado a los componentes invisibles de Gradio
    return texto_pregunta, posibles.to_dict(), preguntas_hechas, siguiente_columna, gr.update(visible=True), gr.update(visible=False)

def reiniciar():
    return jugar(None, df.to_dict(), [], None)

# --- INTERFAZ GRADIO ---

with gr.Blocks() as demo:
    gr.Markdown("# 🏛️ Adivinador de Presidentes")
    gr.Markdown("Piensa en un presidente y yo intentaré adivinarlo.")
    
    # Variables de estado (invisibles para el usuario)
    estado_df = gr.State(df.to_dict())
    estado_preguntas = gr.State([])
    columna_actual = gr.State(None)
    
    # Interfaz visual
    pregunta_txt = gr.Textbox(label="Mi pregunta:", interactive=False)
    
    with gr.Row() as fila_botones:
        btn_si = gr.Button("Sí", variant="primary")
        btn_no = gr.Button("No", variant="stop")
    
    resultado_final = gr.Markdown("")
    btn_reintentar = gr.Button("Jugar de nuevo", visible=False)

    # Eventos
    btn_si.click(jugar, [gr.State("Sí"), estado_df, estado_preguntas, columna_actual], 
                 [pregunta_txt, estado_df, estado_preguntas, columna_actual, fila_botones, btn_reintentar])
    
    btn_no.click(jugar, [gr.State("No"), estado_df, estado_preguntas, columna_actual], 
                 [pregunta_txt, estado_df, estado_preguntas, columna_actual, fila_botones, btn_reintentar])
    
    btn_reintentar.click(reiniciar, None, [pregunta_txt, estado_df, estado_preguntas, columna_actual, fila_botones, btn_reintentar])

    # Cargar primera pregunta al iniciar
    demo.load(reiniciar, None, [pregunta_txt, estado_df, estado_preguntas, columna_actual, fila_botones, btn_reintentar])

demo.launch()