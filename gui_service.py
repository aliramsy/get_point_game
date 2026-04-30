import pygame
import redis
import random
import time
import logging

# 1. Setup Logging (Bonus Requirement)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SCORE: %(message)s',
    handlers=[logging.FileHandler("game_logs.log"), logging.StreamHandler()]
)

# 2. Redis Setup (Using Pub/Sub Bonus)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe("aim_direction")

# 3. Pygame Setup
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Hand Tracking - Get Point Game")
clock = pygame.time.Clock()

# Colors & Fonts
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.SysFont("Arial", 24)

# Game Objects
player_pos = [WIDTH // 2, HEIGHT // 2]
target_pos = [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]
score = 0
speed = 15

def draw_plus(surface, color, pos, size=20):
    # Draws the "Plus Sign"
    pygame.draw.line(surface, color, (pos[0] - size, pos[1]), (pos[0] + size, pos[1]), 3)
    pygame.draw.line(surface, color, (pos[0], pos[1] - size), (pos[0], pos[1] + size), 3)

running = True
print("GUI Service started. Waiting for Redis messages...")

while running:
    screen.fill(WHITE)
    
    # Handle Pygame Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 4. Check Redis for new directions (Non-blocking)
    message = pubsub.get_message()
    if message and message['type'] == 'message':
        direction = message['data']
        
        if direction == "UP":    player_pos[1] -= speed
        if direction == "DOWN":  player_pos[1] += speed
        if direction == "LEFT":  player_pos[0] -= speed
        if direction == "RIGHT": player_pos[0] += speed

    # Keep player on screen
    player_pos[0] = max(0, min(WIDTH, player_pos[0]))
    player_pos[1] = max(0, min(HEIGHT, player_pos[1]))

    # 5. Collision Detection (Scoring)
    distance = ((player_pos[0] - target_pos[0])**2 + (player_pos[1] - target_pos[1])**2)**0.5
    if distance < 30:
        score += 1
        logging.info(f"{score}") # Log to file/console
        target_pos = [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]

    # 6. Drawing
    pygame.draw.circle(screen, RED, target_pos, 15) # Goal
    draw_plus(screen, BLUE, player_pos)             # Plus Sign
    
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30) # 30 FPS

pygame.quit()