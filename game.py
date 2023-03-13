import pygame
from pygame import mixer
import random
import math
from PIL import Image

class CarryMinatiChapriCleanerGame():
    def __init__(self): 
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Carryminati : Chapri Cleaner Game")
        self.icon = pygame.image.load('Carryminati.png')
        pygame.display.set_icon(self.icon)
        self.background = pygame.image.load("background.jpg")

        self.playerImg = pygame.image.load('Carryminati.png')
        self.playerX = 370
        self.playerY = 480
        self.playerX_change = 0

        self.enemyImg = []
        self.enemyX = []
        self.enemyY = []
        self.enemyX_change = []
        self.enemyY_change = []

        self.bulletImg = pygame.image.load('bullet.png')
        self.bullet_X = 0
        self.bullet_Y = 480
        self.bullet_X_change = 0
        self.bullet_Y_change = 1
        self.bullet_state = "ready"

        self.score = 0
        self.font = pygame.font.Font('Black Mustang.ttf', 32)

        self.textX = 10
        self.textY =  10

        self.over_font = pygame.font.Font('Black Mustang.ttf', 100)
        self.running = True
        self.restart_game = False
        self.num_of_enemies = 6

    def show_score(self, x, y):
        sc = self.font.render(f"Score : {str(self.score)}", True, (255, 255, 255))
        self.screen.blit(sc, (x, y))

    def game_over_text(self):
        over_text = self.over_font.render("GAME OVER!", True, (255, 255, 255))
        self.screen.blit(over_text, (200, 250))

    # Genarating Random Enemies

    def genarate_random_enemies(self):
        for i in range(self.num_of_enemies):
            e = random.choice(["Dhinchak", "Payal", "Joginder"])
            if e == "Dhinchak":
                self.enemyImg.append(pygame.image.load("Dhichak Pooja.png"))
            if e == "Payal":
                self.enemyImg.append(pygame.image.load("Payal Zone.png"))
            if e == "Joginder":
                self.enemyImg.append(pygame.image.load("Thara Bhai Joginder.png"))
            
            self.enemyX.append(random.randint(0, 800))
            self.enemyY.append(random.randint(50, 150))
            self.enemyX_change.append(2)
            self.enemyY_change.append(30)

    def player(self):
        self.screen.blit(self.playerImg, (self.playerX, self.playerY))

    def enemy(self, x, y, i):
        self.screen.blit(self.enemyImg[i], (x, y))

    def fire_bullet(self, x, y):
        self.bullet_state
        self.bullet_state = "fire"
        self.screen.blit(self.bulletImg, (x + 20, y + 17))

    def isColission(self, enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False


    def run_game(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.K_BACKSPACE or event.type == pygame.K_ESCAPE:
                    self.restart_game = True

                if self.restart_game:
                    self.running = False
                    self.run_game()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.playerX_change = -0.8
                    
                    if event.key == pygame.K_RIGHT:
                        self.playerX_change = 0.8

                    if event.key == pygame.K_SPACE:
                        if self.bullet_state == "ready":
                            self.bullet_X = self.playerX
                            self.fire_bullet(self.bullet_X, self.bullet_Y)
                            bullet_sound = mixer.Sound('laser.wav')
                            bullet_sound.play()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        self.playerX_change = 0
            
            self.genarate_random_enemies()
            self.playerX += self.playerX_change
            if self.playerX <= 0:
                self.playerX = 0

            elif self.playerX >= 736:
                self.playerX = 736
            
            for i in range(self.num_of_enemies):
                self.enemyX[i] += self.enemyX_change[i]
                if self.enemyY[i] > 380:
                    for j in range(self.num_of_enemies):
                        self.enemyY[j] = 2000
                    self.game_over_text()
                    game_over_sound = mixer.Sound('game_over.wav')
                    game_over_sound.play()

                    break
                if self.enemyX[i] <= 0:
                    self.enemyX_change[i] = 0.5
                    self.enemyY[i] += self.enemyY_change[i]
                elif self.enemyX[i] >= 736:
                    self.enemyX_change[i] = -0.5
                    self.enemyY[i] += self.enemyY_change[i]
                
                collison = self.isColission(self.enemyX[i], self.enemyY[i], self.bullet_X, self.bullet_Y)
                if collison:
                    self.bullet_Y = 480
                    self.bullet_state = "ready"
                    self.score += 1
                    explosionSound = mixer.Sound('explosion.wav')
                    explosionSound.play() 
                    self.enemyX[i] = random.randint(0, 736)
                    self.enemyY[i] = random.randint(50, 150)
                
                self.enemy(self.enemyX[i], self.enemyY[i], i)

            if self.bullet_Y <=0:
                self.bullet_Y = 480
                self.bullet_state = "ready"

            if self.bullet_state == "fire":
                self.fire_bullet(self.bullet_X, self.bullet_Y)
                self.bullet_Y -= self.bullet_Y_change

            self.player()
            self.show_score(self.textX, self.textY)
            pygame.display.update()

if __name__ == "__main__":
    game = CarryMinatiChapriCleanerGame()
    game.run_game()