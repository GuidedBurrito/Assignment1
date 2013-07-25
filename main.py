'''
Name: Alex Valickis
Date June 20th 2013
Purpose: A side scrolling astroid dodging game
'''
import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 480))

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Ship.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.startingY = 200
        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()
            self.sndPickUp = pygame.mixer.Sound("PickUp.ogg")
            self.sndThunder = pygame.mixer.Sound("Crash.ogg")
            self.sndMusic = pygame.mixer.Sound("SpaceGameMusic.ogg")
            self.sndMusic.play(-1)
        
    def update(self):
        if self.rect.bottom >= screen.get_width():
            self.rect.center = (60, 30)
        
        if self.rect.top <= screen.get_height() - screen.get_height() - self.rect.height:
            self.rect.center = (60, 450)
            
        self.rect.center = (60, self.startingY)
                
class Perl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Perl.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 5
    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.bottom >= screen.get_width():
            self.reset()
        if self.rect.top <= screen.get_height() - screen.get_height() - self.rect.height:
            self.reset()
        if self.rect.left <= screen.get_width() - screen.get_width() - self.rect.width:
            self.reset() 
            
    def reset(self):
        self.rect.left = 640
        self.rect.centery = random.randrange(0, screen.get_height())
      
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Asteroid.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.health = 100
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.right <= 0:
            self.reset()
        if self.rect.top <= screen.get_height() - screen.get_height() - self.rect.height:
            self.reset()
        if self.rect.bottom >= screen.get_height() + self.rect.height:
            self.reset()
    
    def reset(self):
        self.rect.left = 640
        self.image = pygame.transform.scale(self.image, (random.randrange(130, 200), random.randrange(130, 200)))
        self.rect.centery = random.randrange(0, screen.get_height())
        self.dy = random.randrange(-2, 2)
        self.dx = random.randrange(-4, -2)
        self.health = 100
    
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Background.gif")
        self.rect = self.image.get_rect()
        self.dx = -5
        self.reset()
        
    def update(self):
        self.rect.left += self.dx
        if self.rect.left <= -600:
            self.reset() 
    
    def reset(self):
        self.rect.right = 1440

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 100
        self.score = 0
        self.missles = 0
        self.font = pygame.font.SysFont("None", 40)
        
    def update(self):
        self.text = "          Hull Strength: %" + "%d, Score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Laser.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.firing = False
        self.dx = 5
        self.currentY = 200
        
    def fire(self):
        self.rect.centery = self.currentY
        self.rect.centerx = 60
        self.firing = True
        self.update()
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.image = pygame.image.load("Laser.gif")
        self.rect.centerx += self.dx

    def reset(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (60, self.currentY)
    
def game():
    pygame.display.set_caption("G-ALEX-Y!")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    ship = Ship()
    perl = Perl()
    laser1 = Laser()
    laser2 = Laser()
    laser3 = Laser()
    laser4 = Laser()
    laser5 = Laser()
    laser6 = Laser()
    asteroid1 = Asteroid()
    asteroid2 = Asteroid()
    asteroid3 = Asteroid()
    background = Background()
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.OrderedUpdates(background, perl, ship)
    AsteroidSprites = pygame.sprite.Group(asteroid1, asteroid2, asteroid3)
    LaserSprites = pygame.sprite.Group(laser1, laser2, laser3, laser4, laser5, laser6)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    fireTimer = 0
    while keepGoing:
        clock.tick(30)
        fireTimer += 1
        pygame.mouse.set_visible(False)
        if fireTimer == 125 or fireTimer == 0:
            laser1.fire()
        if fireTimer == 150 or fireTimer == 25:
            laser2.fire()
        if fireTimer == 175 or fireTimer == 50:
            laser3.fire()
        if fireTimer == 200 or fireTimer == 75:
            laser4.fire()
        if fireTimer == 225 or fireTimer == 100:
            laser5.fire()
        elif fireTimer == 250:
            laser6.fire()
            fireTimer = -25
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            if ship.rect.center == (60, 30):
                ship.startingY = 30
                laser1.currentY = 30
                laser2.currentY = 30
                laser3.currentY = 30
                laser4.currentY = 30
                laser5.currentY = 30
                laser6.currentY = 30
            else:
                ship.startingY -= 5
                laser1.currentY -= 5
                laser2.currentY -= 5
                laser3.currentY -= 5
                laser4.currentY -= 5
                laser5.currentY -= 5
                laser6.currentY -= 5
                ship.rect.center = (60, ship.startingY)
            
        if keys[pygame.K_DOWN]:
            if ship.rect.center == (60, 450):
                laser1.currentY = 450
                laser2.currentY = 450
                laser3.currentY = 450
                laser4.currentY = 450
                laser5.currentY = 450
                laser6.currentY = 450
                ship.startingY = 450
            else:
                ship.startingY += 5
                laser1.currentY += 5
                laser2.currentY += 5
                laser3.currentY += 5
                laser4.currentY += 5
                laser5.currentY += 5
                laser6.currentY += 5
                ship.rect.center = (60, ship.startingY)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        #check collisions
        
        if ship.rect.colliderect(perl.rect):
            ship.sndPickUp.play()
            perl.reset()
            scoreboard.score += 100

        hitAsteroids = pygame.sprite.spritecollide(ship, AsteroidSprites, False)
        if hitAsteroids:
            ship.sndThunder.play()
            scoreboard.lives -= 20
            if scoreboard.lives <= 0:
                keepGoing = False
                ship.sndMusic.stop()    
                GameOver(scoreboard.score)
            for theAsteroid in hitAsteroids:
                theAsteroid.reset()
        
        blastAsteroid1 = pygame.sprite.spritecollide(asteroid1, LaserSprites, False)
        if blastAsteroid1:
            asteroid1.health -= 20
            ship.sndThunder.play()
            for theLaser in blastAsteroid1:
                theLaser.reset()
            if asteroid1.health < 1:
                asteroid1.reset()
                
        blastAsteroid2 = pygame.sprite.spritecollide(asteroid2, LaserSprites, False)
        if blastAsteroid2:
            asteroid2.health -= 20
            ship.sndThunder.play()
            for theLaser in blastAsteroid2:
                theLaser.reset()
            if asteroid2.health < 1:
                asteroid2.reset()
        
        blastAsteroid3 = pygame.sprite.spritecollide(asteroid3, LaserSprites, False)
        if blastAsteroid3:
            asteroid3.health -= 20
            ship.sndThunder.play()
            for theLaser in blastAsteroid3:
                theLaser.reset()
            if asteroid3.health < 1:
                asteroid3.reset()
        
        LaserSprites.update()
        friendSprites.update()
        AsteroidSprites.update()
        scoreSprite.update()
        
        friendSprites.draw(screen)
        AsteroidSprites.draw(screen)
        scoreSprite.draw(screen)
        LaserSprites.draw(screen)
        pygame.display.flip()
    
    ship.sndMusic.stop()
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score

def titleScreen(): 
    pygame.display.set_caption("G-ALEX-Y!")

    ship = Ship()
    background = Background()
    
    allSprites = pygame.sprite.Group(background)
    insFont = pygame.font.Font("Fipps-Regular.otf", 32)
    insLabels = []
    Message = (
    "        G-ALEX-Y" ,
    "",
    "",
    "",
    "",
    "     Click - Start",
    "",
    "Space - Instructions",
    "",
    "     Escape - Quit"
    )
    
    for line in Message:
        tempLabel = insFont.render(line, 1, (255, 255, 250))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
                elif event.key == pygame.K_SPACE:
                    keepGoing = False
                    donePlaying = False
                    ship.sndMusic.stop()
                    instructions() 
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    ship.sndMusic.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying

def GameOver(score):
    pygame.display.set_caption("G-ALEX-Y!")

    ship = Ship()
    background = Background()
    
    allSprites = pygame.sprite.Group(background, ship)
    insFont = pygame.font.Font("Fipps-Regular.otf", 25)
    insLabels = []
    GameOverMessage = (
    "",
    "",
    "",
    "            GAME OVER",
    "",
    "",
    "       Your Score: %d" % score ,
    "",
    "",
    "",
    "      Play Again? (Y/N)"
    )
    
    for line in GameOverMessage:
        tempLabel = insFont.render(line, 1, (255, 255, 255))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    Scoreboard.score = 0
                    keepGoing = False
                    donePlaying = True
                    ship.sndMusic.stop()    
                    Scoreboard.score = game()
                elif  event.key == pygame.K_n:
                    keepGoing = False
                    donePlaying = True
                    
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    ship.sndMusic.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying
    
def instructions():
    pygame.display.set_caption("G-ALEX-Y!")

    ship = Ship()
    background = Background()
    
    allSprites = pygame.sprite.Group(background, ship)
    insFont = pygame.font.Font("Fipps-Regular.otf", 16)
    insLabels = []
    instructions = (
    "                         G-ALEX-Y" ,
    "",
    "                       Instructions",  
    '',
    "     You are a space exploration ship",
    "     traveling to undescovered planets.",
    "",
    "     Fly into artifacts to collect points,",
    "     but be careful not to fly too close",    
    "     to the asteroids. Your ship will ",
    "     explode if it is hit by them too",
    "     many times! Steer with your",
    "     mouse to controll the ship.",
    "",
    "     click to start, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 250))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    ship.sndMusic.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying
        
def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = titleScreen()
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()