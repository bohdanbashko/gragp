import pygame
import sys
import random
from button import Button

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Player dimensions
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

# Enemy dimensions
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50

# Ability cooldowns (in frames)
ABILITY_COOLDOWN = 1

# HP bar dimensions
HP_BAR_WIDTH = 100
HP_BAR_HEIGHT = 10





class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 100
        self.cooldown = 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def use_ability(self, target):
        if self.cooldown == 0:
            if target.hp > 0:
                # Implement ability logic here
                target.hp -= 10  # Example: Ability reduces 10 HP
                print("Ability used! Target HP:", target.hp)
                self.cooldown = ABILITY_COOLDOWN

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 100

# Function to draw HP bar
def draw_hp_bar(surface, entity):
    # Calculate HP bar dimensions
    hp_bar_width = HP_BAR_WIDTH * (entity.hp / 100)
    hp_bar_rect = pygame.Rect(entity.rect.x, entity.rect.y - 20, max(hp_bar_width, 0), HP_BAR_HEIGHT)  # Ensure width doesn't go below 0
    # Draw HP bar
    pygame.draw.rect(surface, GREEN, hp_bar_rect)

def main_menu(screen):
    # Load background image
    bg = pygame.image.load("assets/menu background.png")

    # Function to get font
    def get_font(size):
        return pygame.font.Font("assets/font.ttf", size)

    # Function to handle the main menu
    while True:
        screen.blit(bg, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(330, 400), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(330, 550), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(330, 700), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_pos):
                    return "play"
                elif options_button.checkForInput(mouse_pos):
                    return "options"
                elif quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()

def play_game(screen):

    # Set up fonts
    font = pygame.font.SysFont(None, 40)

    # Set up questions
    questions = [
        {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "options": ["Paris", "London", "Berlin", "Rome"]
        },
        {
            "question": "What is the largest planet in our solar system?",
            "answer": "Jupiter",
            "options": ["Earth", "Mars", "Jupiter", "Saturn"]
        },
        {
            "question": "Who painted the Mona Lisa?",
            "answer": "Leonardo da Vinci",
            "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"]
        }
    ]

    # Set up text for the first question
    current_question_index = 0
    current_question = questions[current_question_index]
    question_text = font.render(current_question["question"], True, BLACK)
    answer_text = font.render(current_question["answer"], True, BLACK)
    option_texts = [font.render(option, True, BLACK) for option in current_question["options"]]

    # Set up button
    next_button = pygame.Rect(50, 200, 200, 50)

    # Set up states
    show_question = True
    show_answer = False

    # Initialize player
    player = Player(RED, 100, 300)

    # Initialize enemies
    enemies = []
    for i in range(3):
        enemy = Enemy(BLUE, 600, 100 * (i + 1))
        enemies.append(enemy)

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(*enemies)

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    winner = None
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    # Check if clicked on an enemy
                    for enemy in enemies:
                        if enemy.rect.collidepoint(event.pos):
                            player.use_ability(enemy)
                
                if next_button.collidepoint(mouse_pos):
                    if show_question:
                        show_question = False
                        show_answer = True
                    elif show_answer:
                        current_question_index += 1
                        if current_question_index < len(questions):
                            current_question = questions[current_question_index]
                            question_text = font.render(current_question["question"], True, BLACK)
                            answer_text = font.render(current_question["answer"], True, BLACK)
                            option_texts = [font.render(option, True, BLACK) for option in current_question["options"]]
                            show_question = True
                            show_answer = False
        
        # Draw button, question text, and options based on states
        if show_question:
            pygame.draw.rect(screen, GREEN, next_button)
            screen.blit(question_text, (next_button.x + 10, next_button.y - 50))
            for i, option_text in enumerate(option_texts):
                screen.blit(option_text, (next_button.x + 10, next_button.y + 20 + i * 40))
        elif show_answer:
            pygame.draw.rect(screen, RED, next_button)
            screen.blit(answer_text, (next_button.x + 10, next_button.y - 30))
        pygame.display.flip()
        # Check for winner
        if all(enemy.hp <= 0 for enemy in enemies):
            winner = "Player"
        elif player.hp <= 0:
            winner = "Enemies"

        # Update
        all_sprites.update()

        # Rendering
        screen.fill(WHITE)
        all_sprites.draw(screen)
        # Draw HP bars
        draw_hp_bar(screen, player)
        for enemy in enemies:
            draw_hp_bar(screen, enemy)

        # Display winner if any
        if winner:
            font = pygame.font.Font(None, 50)
            text_surface = font.render(f"{winner} wins!", True, GREEN)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

def options():
    # Placeholder options function
    pass

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("1v3 Game with Abilities and HP")

# Main loop
while True:
    action = main_menu(screen)
    if action == "play":
        play_game(screen)
    elif action == "options":
        options()