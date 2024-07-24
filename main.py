import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 256, 196
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.SCALED)
Icon = pygame.image.load('colonthree.png')
pygame.display.set_icon(Icon)

pygame.mixer.set_num_channels(1)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (255,174,201)
BLUE = (153,217,234)
r = 0
g = 0
b = 0

cursor = pygame.image.load('cursor.png').convert_alpha()
explosion = [pygame.image.load('explosion/1.gif'),pygame.image.load('explosion/2.gif'),pygame.image.load('explosion/3.gif'),pygame.image.load('explosion/4.gif'),pygame.image.load('explosion/5.gif'),pygame.image.load('explosion/6.gif'),pygame.image.load('explosion/7.gif'),pygame.image.load('explosion/8.gif'),pygame.image.load('explosion/9.gif'),pygame.image.load('explosion/10.gif'),pygame.image.load('explosion/11.gif'),pygame.image.load('explosion/12.gif'),pygame.image.load('explosion/13.gif'),pygame.image.load('explosion/14.gif'),pygame.image.load('explosion/15.gif'),pygame.image.load('explosion/16.gif'),pygame.image.load('explosion/17.gif')]

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = 0
        self.sizevariance=random.randint(-50,0)
        self.image = explosion[self.frame+1]
        self.rect = self.image.get_rect()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x+50-self.sizevariance+random.randint(-10,10), mouse_y+75-self.sizevariance+random.randint(-10,10))
        pygame.mixer.stop()
        pygame.mixer.Sound.play(pygame.mixer.Sound("explosion.mp3"))

    def update(self):
        if self.frame < len(explosion)-2:
            self.frame += 0.25
            self.image = pygame.transform.scale(explosion[int(self.frame)+1],(100+self.sizevariance,100+self.sizevariance))
        else:
            self.kill()

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cursor
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self):
        # Get the current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Set the player's center to the mouse position
        self.rect.center = (mouse_x+self.rect.width/2, mouse_y+self.rect.height/2)
        # Keep player within the screen boundaries
        self.rect.x = max(0, min(WIDTH, self.rect.x))
        self.rect.y = max(0, min(HEIGHT, self.rect.y))

# Define bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((1, 10))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5


    def update(self):
        self.rect.y += self.speed*-1
        # Remove bullet if it goes off the screen
        if self.rect.bottom < 0:
            self.kill()

# Load enemy image
enemy_image = pygame.image.load('Gu.png').convert_alpha()  # Replace 'enemy.png' with the actual filename of your enemy image

# Define enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.transform.scale(enemy_image.convert_alpha(),(20*random.randint(1,3),20*random.randint(1,3)))  # Load image with transparency
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 4)
        self.angle = 0
        self.rotate_speed = random.randint(-5, 5)  # Random initial rotation speed

    def update(self):
        # Rotate the image
        self.angle += self.rotate_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Adjust the position to keep the center unchanged
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 4)
            self.rotate_speed = random.randint(-5, 5)  # Randomize rotation speed again



# Create sprite groups
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
for _ in range(16):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)


# Create player
player = Player()
all_sprites.add(player)
players.add(player)

pygame.mouse.set_visible(False)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Shoot bullet when spacebar is pressed
                bullet = Bullet(player.rect.left, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check for mouse click
            if event.button == 1:  # Left mouse button
                # Check for collision with enemies
                clicked_enemies = pygame.sprite.groupcollide(enemies, players, True, False)
                # Remove clicked enemies
                for enemy in clicked_enemies:
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)
                    all_sprites.add(Explosion())
                    if r < 180:
                        r += 60
                        g += 30


 

    # Update
    all_sprites.update()
    if r > 0 and g > 0:
        r -= 10
        g -= 5

    # Collision detection
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)# or pygame.sprite.groupcollide(enemies, players, True, False)
    for hit in hits:
        # Spawn a new enemy when one is destroyed
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw
    screen.fill((r,g,b))
    all_sprites.draw(screen)
    players.draw(screen)
    pygame.display.flip()

    fps = int(clock.get_fps())
    pygame.display.set_caption(f"Gu | {fps}")

    # Control the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
