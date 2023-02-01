"""This is my first game made using pygame, following a tutorial which
I then added upon.
"""

from random import randint
import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_r,
    K_q,
)

pygame.init()

thepath = "C:\\Users\\s-alduan\\OneDrive - Lake Washington School District" \
"\\coding\\pygame\\first\\tutorialgame"

def updateScore(file, score: int, newline=True):
    """Updates score files"""
    append = str(score)
    if newline: append += "\n"
    file.write(append)
    return None

class Player(pygame.sprite.Sprite):
    """Player class"""
    def __init__(self):
        """Creates sprite"""
        super(Player, self).__init__()
        self.surf_normal = pygame.image.load(
            f"{thepath}\\sprites\\player.png"
        ).convert()
        self.surf_normal.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf_invincible = pygame.image.load(
            f"{thepath}\\sprites\\invincible.png"
        ).convert()
        self.surf_invincible.set_colorkey((255,255,255), RLEACCEL)
        self.surf = self.surf_normal
        self.rect = self.surf.get_rect()
        self.speed = 10
        self.lives = 3
        self.isInvincible = False

    def update(self, pressed_keys):
        """Update position logic"""
        # Update sprite if invincible
        if self.isInvincible:
            self.surf = self.surf_invincible
        else:
            self.surf = self.surf_normal
        # Move
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        # Check if it has hit the border of screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        return None
        
class Enemy(pygame.sprite.Sprite):
    """Enemy class"""
    def __init__(self):
        """Generates a new enemy"""
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(
            f"{thepath}\\sprites\\arrow.png"
        ).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                randint(WIDTH + 20, WIDTH + 100),
                randint(0, HEIGHT),
            )
        )
        self.speed = randint(15, 30)

    def update(self):
        """Update enemy position"""
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        return None

class Heart(pygame.sprite.Sprite):
    """Heart class"""
    def __init__(self):
        """Creates a random heart"""
        super(Heart, self).__init__()
        self.surf = pygame.image.load(
            f"{thepath}\\sprites\\heart.png"
        ).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                randint(WIDTH + 20, WIDTH + 100),
                randint(0, HEIGHT),
            )
        )
        self.speed = randint(15, 30)

    def update(self):
        """Update position"""
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        return None

def game():
    """Pretty much all of main(), organized only because making a 
    game over screen turned out to be harder than expected.
    """
    # Create entities
    player = Player()
    enemies = pygame.sprite.Group()
    hearts = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Timer for adding enemies
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 100)
    ADDHEART = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDHEART, 4000)

    # Display highscore
    top = font.render(f"High Score: {s}", True, (255,255,255), None)
    toprect = top.get_rect()

    clock = pygame.time.Clock()
    running = True
    frame = 1
    ticks = pygame.time.get_ticks()
    
    # Game loop
    while running:
        # Either quits, or adds a new enemy
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == ADDHEART:
                new_heart = Heart()
                hearts.add(new_heart)
                all_sprites.add(new_heart)

        # Update entities
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        if (pygame.time.get_ticks() - ticks >= 999
            and player.isInvincible):
            player.isInvincible = False


        enemies.update()    
        hearts.update()

        # Set background
        screen.fill((0,0,0))

        # Render scores
        screen.blit(top, toprect)
        score = font.render(f"Score: {frame}", True, (255,255,255), None)
        scorerect = score.get_rect()
        scorerect.center = (
            scorerect.width//2,
            toprect.height + scorerect.height//2,
        )
        screen.blit(score, scorerect)

        # Healthbar
        bar = f"{thepath}\\sprites\\healthbar{player.lives}.png"
        healthbar = pygame.image.load(bar).convert()
        healthbar.set_colorkey((255, 255, 255), RLEACCEL)
        healthrect = healthbar.get_rect()
        healthrect.center = (
            healthrect.width//2,
            toprect.height + scorerect.height + healthrect.height//2,
        )
        screen.blit(healthbar, healthrect)

        # Render entities
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # On collision with enemy
        if pygame.sprite.spritecollideany(player, enemies):
            # If the time since last hit is > 1 second...
            if not player.isInvincible:
                # Take a life
                player.lives = player.lives - 1
                player.isInvincible = True
                ticks = pygame.time.get_ticks()
                if player.lives == 0:
                    player.kill()
                    running = False
                    # Update score files
                    updateScore(scores, frame, True)
                    if frame > int(s):
                        highscore.truncate()
                        updateScore(highscore, frame, False)

        # On collision with heart
        heartkill = pygame.sprite.spritecollideany(player, hearts)
        if heartkill and player.lives < 3:
            player.lives = player.lives + 1
            heartkill.kill()

        pygame.display.flip()
        clock.tick(30)
        frame = frame + 1
    return None

def gameOver():
    """Unfinished/unused game over screen"""
    board = font.render("GAME OVER", True, (0,0,0), None)
    boardrect = board.get_rect(center=(WIDTH//2, HEIGHT//2))

    over = True
    # Game over screen loops
    while over:
        # Quits or try again
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    over = False

            elif event.type == QUIT:
                over = False

        screen.fill((0,0,0))
        screen.blit(board, boardrect)
    return None

def main():
    """main()"""
    game()
    scores.close()
    highscore.close()
    return None

if __name__ == '__main__':
    # Set up window
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('First Game')
    font = pygame.font.Font("C:\Windows\Fonts\Times.ttf", 20)

    # Get scores
    highscore = open("highscore.txt", "r+")
    scores = open("scores.txt", "a")
    s = highscore.readline()
    highscore.seek(0)
    main()