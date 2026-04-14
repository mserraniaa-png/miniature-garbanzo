import pygame
import sys
import time
from Blackjack.logic import Card, Deck, Hand, Player, Participant
from Blackjack.assets import Assets, GREEN_TABLE, DARK_GREEN_TABLE, WHITE, GOLD, RED, GRAY, BLUE

# Configuración de pantalla
WIDTH, HEIGHT = 1000, 700
FPS = 60

class BlackjackGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Blackjack - Pygame Casino")
        self.clock = pygame.time.Clock()
        
        # Inicializar lógica
        self.deck = Deck()
        self.dealer = Participant("Dealer")
        self.human = Player("Tú", balance=100, is_bot=False)
        self.bots = [
            Player("Bot 1", balance=100, is_bot=True),
            Player("Bot 2", balance=100, is_bot=True),
            Player("Bot 3", balance=100, is_bot=True)
        ]
        self.all_players = [self.bots[0], self.bots[1], self.human, self.bots[2]]
        
        # Estado del juego
        self.state = "BETTING" # BETTING, DEALING, PLAYER_TURN, BOT_TURNS, DEALER_TURN, RESULTS
        self.current_turn_index = 0 # Quién está jugando
        self.selected_chip = 50
        self.message = "Haz tu apuesta"
        
        # Posiciones en pantalla
        self.positions = {
            "Dealer": (WIDTH // 2 - 35, 50),
            self.bots[0]: (100, 350),
            self.bots[1]: (300, 450),
            self.human: (WIDTH // 2 - 35, 500),
            self.bots[2]: (700, 450),
        }

    def reset_round(self):
        if self.human.balance < 50:
             self.human.balance = 100 # Recarga automática para seguir jugando
             self.message = "Balance recargado. Haz tu apuesta."
        else:
             self.message = "Nueva ronda. Haz tu apuesta."
             
        self.deck = Deck()
        self.dealer.reset()
        for p in self.all_players:
            p.reset()
        self.state = "BETTING"
        self.current_turn_index = 0

    def start_deal(self):
        self.state = "DEALING"
        # Repartir 2 a cada uno
        for _ in range(2):
            for p in self.all_players:
                p.hand.add_card(self.deck.deal_card())
            self.dealer.hand.add_card(self.deck.deal_card())
        
        self.state = "BOT_TURNS"
        self.current_turn_index = 0

    def handle_bot_turn(self):
        current_p = self.all_players[self.current_turn_index]
        if not current_p.is_bot:
            self.state = "PLAYER_TURN"
            self.message = "Tu turno. ¿Pedir o Plantarse?"
            return

        # Lógica IA: Pedir si < 17
        if current_p.score < 17 and not current_p.busted:
            current_p.hand.add_card(self.deck.deal_card())
            time.sleep(0.5) # Pequeña demora para visualización
        else:
            current_p.is_standing = True
            self.current_turn_index += 1
            if self.current_turn_index >= len(self.all_players):
                self.state = "DEALER_TURN"

    def handle_dealer_turn(self):
        if self.dealer.score < 17 and not self.dealer.busted:
            self.dealer.hand.add_card(self.deck.deal_card())
            time.sleep(0.5)
        else:
            self.state = "RESULTS"
            self.calculate_results()

    def calculate_results(self):
        d_score = self.dealer.score
        d_busted = self.dealer.busted
        
        for p in self.all_players:
            if p.busted:
                p.lose()
            elif d_busted or p.score > d_score:
                p.win()
            elif p.score == d_score:
                p.push()
            else:
                p.lose()
        
        if self.human.busted:
            self.message = "¡Te pasaste! Perdiste."
        elif d_busted or self.human.score > d_score:
            self.message = "¡Ganaste!"
        elif self.human.score == d_score:
            self.message = "Empate (Push)."
        else:
            self.message = "La casa gana."

    def draw(self):
        self.screen.fill(GREEN_TABLE)
        
        # Dibujar Dealer
        dx, dy = self.positions["Dealer"]
        for i, card in enumerate(self.dealer.hand.cards):
            hidden = (i == 0 and self.state != "RESULTS" and self.state != "DEALER_TURN")
            Assets.draw_card(self.screen, dx + i*20, dy, card, hidden)
        
        # Dibujar Jugadores
        for p in self.all_players:
            px, py = self.positions[p]
            # Nombre y Balance
            font = pygame.font.SysFont('Arial', 18, bold=True)
            color = GOLD if p == self.human else WHITE
            name_txt = font.render(f"{p.name}: {p.score}", True, color)
            self.screen.blit(name_txt, (px, py - 30))
            
            # Chips y apuesta
            if p.current_bet > 0:
                Assets.draw_chip(self.screen, px - 30, py + 50, p.current_bet)
            
            if p == self.human:
                bal_txt = font.render(f"Saldo: ${p.balance}", True, GOLD)
                self.screen.blit(bal_txt, (px, py + 120))

            # Cartas
            for i, card in enumerate(p.hand.cards):
                Assets.draw_card(self.screen, px + i*20, py, card)
            
            if p.busted:
                over_txt = font.render("PASADO", True, RED)
                self.screen.blit(over_txt, (px, py + 105))

        # UI lateral / Inferior
        self.draw_ui()
        
        pygame.display.flip()

    def draw_ui(self):
        font = pygame.font.SysFont('Arial', 24, bold=True)
        msg_surf = font.render(self.message, True, WHITE)
        msg_rect = msg_surf.get_rect(center=(WIDTH//2, HEIGHT - 150))
        self.screen.blit(msg_surf, msg_rect)

        if self.state == "BETTING":
            # Chips para elegir
            for i, val in enumerate([50, 100, 200, 500]):
                Assets.draw_chip(self.screen, 200 + i*100, HEIGHT - 60, val, self.selected_chip == val)
            
            self.btn_bet = Assets.draw_button(self.screen, 650, HEIGHT - 80, 150, 40, "APOSTAR", GOLD)
        
        elif self.state == "PLAYER_TURN":
            self.btn_hit = Assets.draw_button(self.screen, WIDTH//2 - 160, HEIGHT - 80, 150, 40, "PEDIR", (0, 150, 0))
            self.btn_stand = Assets.draw_button(self.screen, WIDTH//2 + 10, HEIGHT - 80, 150, 40, "PLANTARSE", RED)
            
        elif self.state == "RESULTS":
            self.btn_next = Assets.draw_button(self.screen, WIDTH//2 - 75, HEIGHT - 80, 150, 40, "OTRA RONDA", BLUE)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.state == "BETTING":
                        # Selección de fichas
                        for i, val in enumerate([50, 100, 200, 500]):
                            center = (200 + i*100, HEIGHT - 60)
                            if (pos[0]-center[0])**2 + (pos[1]-center[1])**2 < 25**2:
                                self.selected_chip = val
                        
                        if hasattr(self, 'btn_bet') and self.btn_bet.collidepoint(pos):
                            if self.human.place_bet(self.selected_chip):
                                # Bots también apuestan lo mismo o aleatorio
                                for b in self.bots:
                                    b.place_bet(50) 
                                self.start_deal()
                            else:
                                self.message = "Saldo insuficiente"
                                
                    elif self.state == "PLAYER_TURN":
                        if hasattr(self, 'btn_hit') and self.btn_hit.collidepoint(pos):
                            self.human.hand.add_card(self.deck.deal_card())
                            if self.human.busted:
                                self.current_turn_index += 1
                                self.state = "BOT_TURNS"
                        elif hasattr(self, 'btn_stand') and self.btn_stand.collidepoint(pos):
                            self.human.is_standing = True
                            self.current_turn_index += 1
                            self.state = "BOT_TURNS"
                    
                    elif self.state == "RESULTS":
                        if hasattr(self, 'btn_next') and self.btn_next.collidepoint(pos):
                            self.reset_round()

            # Lógica automática
            if self.state == "BOT_TURNS":
                if self.current_turn_index < len(self.all_players):
                    self.handle_bot_turn()
                else:
                    self.state = "DEALER_TURN"
            
            elif self.state == "DEALER_TURN":
                self.handle_dealer_turn()

            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = BlackjackGame()
    game.run()
