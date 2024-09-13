import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.image.load("ss.jpeg")

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

POWER_UP_WIDTH = 20
POWER_UP_HEIGHT = 20

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars, power_ups, score):
    WIN.blit(BG, (0, 0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", True, (255, 255, 255))
    WIN.blit(time_text, (10, 10))
    
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    
    pygame.draw.rect(WIN, (255, 182, 193), player)
    
    for star in stars:
        pygame.draw.rect(WIN, (255, 255, 255), star)

    for power_up in power_ups:
        pygame.draw.rect(WIN, (0, 255, 0), power_up)

    pygame.display.update()

def main():
    run = True
    
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    
    start_time = time.time()
    elapsed_time = 0
    
    star_add_increment = 2000
    star_count = 0
    
    stars = []
    power_ups = []
    hit = False
    score = 0
    
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        current_star_vel = STAR_VEL + (elapsed_time // 10)
        
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
                
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0
        
        if random.randint(1, 1000) > 987:
            power_up_x = random.randint(0, WIDTH - POWER_UP_WIDTH)
            power_up = pygame.Rect(power_up_x, -POWER_UP_HEIGHT, POWER_UP_WIDTH, POWER_UP_HEIGHT)
            power_ups.append(power_up)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
            
        for star in stars[:]:
            star.y += current_star_vel
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                hit = True
                break

        for power_up in power_ups[:]:
            power_up.y += 3
            if power_up.y > HEIGHT:
                power_ups.remove(power_up)
            elif power_up.colliderect(player):
                power_ups.remove(power_up)
                score += 1

        if hit:
            lost_text = FONT.render(f"You Lost!", True, (255, 255, 0))
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            lost_text = FONT.render(f"Final Score: {score}", True, (255, 255, 0) )
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, + HEIGHT / 2 - lost_text.get_height() / 2 + 50))
            lost_text = FONT.render(f"Time: {round(elapsed_time)} s", True, (255, 255, 0))
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, + HEIGHT / 2 - lost_text.get_height() / 2 + 100))
            
            pygame.display.update()
            pygame.time.delay(4000)
            break
            
        draw(player, elapsed_time, stars, power_ups, score)
        
    pygame.quit()
    
if __name__ == "__main__":
    main()


