# Pygame Blackjack

Un juego de Blackjack interactivo desarrollado en Python utilizando la librería **Pygame**. Incluye multijugador simulado con inteligencia artificial y un sistema de apuestas con fichas.

## Características

- **Gráficos Vectoriales**: Cartas y fichas dibujadas dinámicamente con Pygame.
- **IA de Jugadores**: 3 bots que juegan automáticamente siguiendo las reglas estándar de casino.
- **Sistema de Apuestas**: Gestión de balance y fichas de diferentes valores ($50, $100, $200, $500).
- **Reglas Estándar**:
  - Un solo mazo de 52 cartas.
  - La casa se planta en 17.
  - El As se ajusta automáticamente (1 u 11).

## Requisitos

- Python 3.x
- Pygame

Para instalar las dependencias:
```bash
pip install pygame
```

## Cómo jugar

Ejecuta el archivo principal:
```bash
python main.py
```

1. **Apostar**: Selecciona una ficha haciendo clic sobre ella y presiona el botón **APOSTAR**.
2. **Acciones**: Durante tu turno, puedes elegir entre **PEDIR** (Hit) o **PLANTARSE** (Stand).
3. **Bots**: Observa cómo juegan los demás jugadores y el crupier.
4. **Continuar**: Al finalizar la ronda, presiona **OTRA RONDA** para seguir jugando.

## Estructura del Proyecto

- `main.py`: Bucle principal y lógica de estados.
- `logic.py`: Clases de Mazo, Cartas, Manos y Jugadores.
- `assets.py`: Funciones de renderizado para UI y activos visuales.
