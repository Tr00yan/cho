#Создай собственный Шутер!
from time import time as timer 
from pygame import *
from random import *
window= display.set_mode((700,500))
backround = transform.scale(image.load('galaxy.jpg'), (700,500))
mixer.init()
font.init()
mixer.music.load('space.ogg')
#mixer.music.play()
spacemusic = mixer.Sound('space.ogg')
mixer.music.load("fire.ogg")
fire_sound = mixer.Sound("fire.ogg")
spacemusic.play()
run = True
clock = time.Clock()
finish = False
losepoints = 0 
score = 0
num_fire = 0
rel_time = False
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial',80)
win = font1.render("YOU WIN!", True, (255,255,255))
lose = font1.render("YOU LOSE!", True, (180,0,0))
#---------------------------------------------------------------------------
class GameSprite(sprite.Sprite):
   #конструктор класса
    def __init__(self, player_image, player_x, player_y,size_x, size_y,player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#--------------------------------------------------------------------------------
class Player(GameSprite):
   # def __init__(self, player_image, player_x, player_y, player_speed):
        #super().__init__()
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top,15,20,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        global losepoints
        if self.rect.y > 500:
            self.rect.x = randint(80, 420)
            self.rect.y = 0
            losepoints = losepoints + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        if self.rect.y < 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 420)
            self.rect.y = 0
#------------------------------------------------------
shatl = Player("rocket.png", 250,250,80,100,10)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(80,620), -40, 80, 50, randint(1,5))
    monsters.add(monster)
for i in range(3):
    asteroidpon = Asteroid("asteroid.png", randint(80,620), -40, 80, 50, randint(1,5))
    asteroids.add(asteroidpon)
while run:
   # if losepoints == 3:
      #  finish = True
    clock.tick(60)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    shatl.fire()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    #if losepoints > 10:
        #finish = True
        #text_lose = font2.render("Пропущено:"+ str(losepoints), 1, (255,255,255))
    #elif score > 10:
        #text_win = font2.render("YOU WIN!"), 1, (255,255,255))
        
    if not finish:  
        text = font2.render("Cчёт"+ str(score),1,(255,255,255))
        
        text_lose = font2.render("Пропущено:"+ str(losepoints), 1, (255,255,255))
        window.blit(backround, (0,0))
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets,True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80,620), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(shatl,monsters, False) or losepoints >= 4:
            finish = True
            window.blit(lose, (200,200))
        if sprite.spritecollide(shatl,asteroids, False):
            finish = True
            window.blit(lose, (200,200))
        if score == 10:
            window.blit(win, (200,200))
            finish = True
        asteroids.update()
        asteroids.draw(window)
        shatl.reset()
        shatl.update()
        monsters.update()
        monsters.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload',1, (150,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False
        window.blit(text_lose,(10,50))
        window.blit(text,(10,20))

    
        display.update()
        
    time.delay(50)
