# President-Guesser
Este proyecto es un sistema diseñado para la identificación de líderes políticos mediante un árbol de decisión dinámico. El motor optimiza la selección de preguntas basándose en la maximización de la ganancia de información (Information Gain).

# Lógica matemática

El motor de este proyecto se basa en la Entropía de Shannon. En teoría de la información, la entropía (H) mide la incertidumbre de un conjunto de datos. Cuanto más desordenado está el dataset (más presidentes posibles), mayor es la entropía.

$$H(S) = - \sum_{i=1}^{n} p_i \log_2(p_i)$$

Para adivinar al personaje rápido, el algoritmo busca reducir esa entropía lo máximo posible en cada pregunta. Esto se conoce como Ganancia de Información.

## Explicación:

Imagina que tienes 100 presidentes.

Si haces una pregunta que solo descarta a 1 persona (ej. "¿Es de Andorra?"), te quedan 99. Has ganado muy poca información.

Si haces una pregunta que descarta a 50 personas (ej. "¿Es de Europa?"), has cortado el problema por la mitad.

Mi algoritmo analiza todas las columnas del CSV en cada turno y elige la que divide a los candidatos supervivientes en dos grupos lo más parecidos posible (50/50). Matemáticamente, esto convierte una búsqueda lineal eterna en una búsqueda binaria. Por eso, aunque el dataset crezca, el número de preguntas apenas sube: es el poder del crecimiento logarítmico.
