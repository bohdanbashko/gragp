import pygame
import sys
import random

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Quiz Program")

# Set up fonts
font = pygame.font.SysFont(None, 40)

# Set up questions
questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
    {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"}
]

# Shuffle questions
random.shuffle(questions)

# Set up text
current_question = questions.pop(0)
question_text = font.render(current_question["question"], True, BLACK)
answer_text = font.render(current_question["answer"], True, BLACK)

# Set up buttons
question_button = pygame.Rect(50, 200, 200, 50)
answer_button = pygame.Rect(50, 200, 200, 50)

# Set up states
show_question = True
show_answer = False

# Main game loop
while True:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if question_button.collidepoint(mouse_pos) and show_question:
                show_question = False
                show_answer = True
            elif answer_button.collidepoint(mouse_pos) and show_answer:
                show_answer = False
                if questions:
                    current_question = questions.pop(0)
                    question_text = font.render(current_question["question"], True, BLACK)
                    answer_text = font.render(current_question["answer"], True, BLACK)
                    show_question = True
                else:
                    # No more questions, handle end of quiz
                    pass

    # Draw buttons and text based on states
    if show_question:
        pygame.draw.rect(screen, GREEN, question_button)
        screen.blit(question_text, (question_button.x + 10, question_button.y - 30))
    elif show_answer:
        pygame.draw.rect(screen, RED, answer_button)
        screen.blit(answer_text, (answer_button.x + 10, answer_button.y - 30))

    pygame.display.flip()
