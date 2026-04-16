import pygame

# Colores
GREEN_TABLE = (20, 80, 20)
DARK_GREEN_TABLE = (15, 60, 15)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GOLD = (212, 175, 55)
GRAY = (100, 100, 100)
BLUE = (0, 0, 200)

class Assets:
    @staticmethod
    def draw_card(surface, x, y, card, hidden=False):
        width, height = 70, 100
        rect = pygame.Rect(x, y, width, height)
        
        # Borde y fondo
        pygame.draw.rect(surface, WHITE, rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, rect, width=2, border_radius=5)
        
        if hidden:
            # Dibujar dorso de carta
            pygame.draw.rect(surface, BLUE, (x+5, y+5, width-10, height-10), border_radius=3)
            pygame.draw.line(surface, WHITE, (x+5, y+5), (x+width-5, y+height-5), 2)
            pygame.draw.line(surface, WHITE, (x+width-5, y+5), (x+5, y+height-5), 2)
            return

        # Dibujar contenido de la carta
        color = RED if card.suit in ['Hearts', 'Diamonds'] else BLACK
        font = pygame.font.SysFont('Arial', 24, bold=True)
        small_font = pygame.font.SysFont('Arial', 16)
        
        # Símbolo y Rank
        rank_text = font.render(card.rank, True, color)
        surface.blit(rank_text, (x + 5, y + 5))
        
        # Símbolos representados por texto o formas simples
        suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        suit_text = font.render(suit_symbols[card.suit], True, color)
        surface.blit(suit_text, (x + width - 25, y + height - 30))

    @staticmethod
    def draw_chip(surface, x, y, value, selected=False):
        radius = 25
        colors = {50: (200, 0, 0), 100: (0, 0, 150), 200: (0, 150, 0), 500: (150, 150, 0)}
        color = colors.get(value, GRAY)
        
        # Círculo exterior
        pygame.draw.circle(surface, color, (x, y), radius)
        pygame.draw.circle(surface, WHITE, (x, y), radius, width=2)
        
        if selected:
            pygame.draw.circle(surface, GOLD, (x, y), radius + 4, width=3)
            
        # Valor
        font = pygame.font.SysFont('Arial', 18, bold=True)
        text = font.render(str(value), True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

    @staticmethod
    def draw_button(surface, x, y, w, h, text, color, active=True):
        rect = pygame.Rect(x, y, w, h)
        draw_color = color if active else (50, 50, 50)
        
        pygame.draw.rect(surface, draw_color, rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, rect, width=2, border_radius=10)
        
        font = pygame.font.SysFont('Arial', 20, bold=True)
        text_surf = font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
        return rect
