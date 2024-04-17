import pygame
import sys

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
                    else:
                        # No more questions, handle end of quiz
                        pygame.quit()
                        sys.exit()

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
