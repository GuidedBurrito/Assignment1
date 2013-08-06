'''
Name: Alex Valickis
Date August 5th 2013
Purpose: A side scrolling space battle game
'''

'importsneeded utilities'
import pygame, random
pygame.init()

'sets up the screen'
screen = pygame.display.set_mode((640, 480))

'sets uo the ship sprite'
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
            'sets up the music and sounds'
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

'Sets up the perl sprite'
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
      
'Sets up the asteroid sprite'
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Asteroid.png")
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
        self.image = pygame.image.load("Asteroid.png")
        self.image = pygame.transform.scale(self.image, (random.randrange(130, 200), random.randrange(130, 200)))
        self.rect.centery = random.randrange(0, screen.get_height())
        self.dy = random.randrange(-2, 2)
        self.dx = random.randrange(-4, -2)
        self.health = 100
        
    def remove(self):
        self.kill()
        
'Sets up the alien sprite'
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Alien.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.health = 100
        self.moveDown = 1
        self.dy = 200
        self.reset()
        
    def update(self):
        if self.rect.center == (580,30):
            self.moveDown = 1
        if self.rect.center == (580,450):
            self.moveDown = 2
        if self.moveDown == 1:
            self.dy += 5
        if self.moveDown == 2:
            self.dy -= 5
        self.rect.center = (580, self.dy)
               
    def reset(self):
        self.rect.left = 580
        self.rect.centery = random.randrange(30, screen.get_height())
        self.health = 100
        
    def remove(self):
        self.kill()

'Sets up the moving background'
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

'Sets up the scorebord'
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 100
        self.score = 0
        self.missles = 0
        self.booms = 0
        self.font = pygame.font.SysFont("None", 40)
        
    def update(self):
        self.text = "          Hull Strength: %" + "%d, Score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()

'Sets up the laser sprites'
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

'sets up the bosses laser'
class BLaser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("BLaser.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.firing = False
        self.dx = 5
        self.currentY = 200
        
    def fire(self):
        self.rect.centery = self.currentY
        self.rect.centerx = 500
        self.firing = True
        self.update()
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.image = pygame.image.load("BLaser.png")
        self.rect.centerx -= self.dx        

    def reset(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (500, self.currentY)        

'sets up the boss'
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Boss.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.health = 100
        self.dy = 200
        self.moveDown = 1

    def update(self):
        if self.rect.center == (500,150):
            self.moveDown = 1
        if self.rect.center == (500,325):
            self.moveDown = 2
        if self.moveDown == 1:
            self.dy += 5
        if self.moveDown == 2:
            self.dy -= 5
        self.rect.center = (500, self.dy)
    
    def reset(self):
        self.rect.left = 500
        self.rect.centery = random.randrange(0, screen.get_height())
        self.dy = random.randrange(-2, 2)
        self.health = 100
        
    def remove(self):
        self.kill()

'Main game function'
def game():
    
    'labels the game window'
    pygame.display.set_caption("G-ALEX-Y!")
    
    'creates sprites from their set ups'
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
    alien1 = Alien()
    alien2 = Alien()
    alien3 = Alien()
    asteroid1 = Asteroid()
    asteroid2 = Asteroid()
    boss = Boss()
    bossLaser1 = BLaser()
    bossLaser2 = BLaser()
    bossLaser3 = BLaser()
    bossLaser4 = BLaser()
    asteroid3 = Asteroid()
    background = Background()
    scoreboard = Scoreboard()

    'Groups sprites'
    friendSprites = pygame.sprite.OrderedUpdates(background, perl, ship)
    AsteroidSprites = pygame.sprite.Group(asteroid1, asteroid2, asteroid3)
    AlienSprites = pygame.sprite.Group(alien1, alien2, alien3)
    BossSprite = pygame.sprite.Group(boss)
    BLaserSprites = pygame.sprite.Group(bossLaser1, bossLaser2, bossLaser3, bossLaser4)
    LaserSprites = pygame.sprite.Group(laser1, laser2, laser3, laser4, laser5, laser6)
    scoreSprite = pygame.sprite.Group(scoreboard)

    'Creates a clock'
    clock = pygame.time.Clock()
   
    'Variables are initialized'
    keepGoing = True
    doneLevel1 = False
    doneLevel2 = False
    asteroidsDestroyed = 0
    aliensDestroyed = 0
    fireTimer = 0
   
    'Level 1'
    while keepGoing:
         'Clock is set up'
         clock.tick(30)
         
         fireTimer += 1
         
         'Sets up the auto fire'
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
          
         'Listens for key presses'
         keys = pygame.key.get_pressed()
          
         'when the up arrow is pressed'
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
              
         'when the down arrow is pressed'
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
          
         'if the user closes the window' 
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 keepGoing = False
         
         'if the ship collects a perl' 
         if ship.rect.colliderect(perl.rect):
             ship.sndPickUp.play()
             perl.reset()
             scoreboard.score += 100
  
         'if the ship hits an asteroid'
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
        
         'if the ship shoots an asteroid'
         blastAsteroid1 = pygame.sprite.spritecollide(asteroid1, LaserSprites, False)
         if blastAsteroid1:
             asteroid1.health -= 20
             ship.sndThunder.play()
             for theLaser in blastAsteroid1:
                 theLaser.reset()
             if asteroid1.health < 1:
                 asteroidsDestroyed += 1
                 if asteroidsDestroyed == 15:
                     asteroid1.remove()
                     asteroid2.remove()
                     asteroid3.remove()
                     keepGoing = False
                     doneLevel1 = True
                 else:
                     asteroid1.reset()
                     scoreboard.booms += 1
         
         'if the ship shoots an asteroid'         
         blastAsteroid2 = pygame.sprite.spritecollide(asteroid2, LaserSprites, False)
         if blastAsteroid2:
             asteroid2.health -= 20
             ship.sndThunder.play()
             for theLaser in blastAsteroid2:
                 theLaser.reset()
             if asteroid2.health < 1:
                 asteroidsDestroyed += 1
                 if asteroidsDestroyed == 15:
                     asteroid1.remove()
                     asteroid2.remove()
                     asteroid3.remove()
                     keepGoing = False
                     doneLevel1 = True
                 else:
                     asteroid2.reset()
                     scoreboard.booms += 1
           
         'if the ship shoots an asteroid'             
         blastAsteroid3 = pygame.sprite.spritecollide(asteroid3, LaserSprites, False)
         if blastAsteroid3:
             asteroid3.health -= 20
             ship.sndThunder.play()
             for theLaser in blastAsteroid3:
                 theLaser.reset()
             if asteroid3.health < 1:
                 asteroidsDestroyed += 1
                 if asteroidsDestroyed == 15:
                     asteroid1.remove()
                     asteroid2.remove()
                     asteroid3.remove()
                     keepGoing = False
                     doneLevel1 = True
                 else:
                     asteroid3.reset()
                     scoreboard.booms += 1
         
         'updates the sprites'
         LaserSprites.update()
         friendSprites.update()
         AsteroidSprites.update()
         scoreSprite.update()
          
         'draws the sprites to the screen'
         friendSprites.draw(screen)
         AsteroidSprites.draw(screen)
         scoreSprite.draw(screen)
         LaserSprites.draw(screen)
         pygame.display.flip()
     
    'Level 2'         
    while doneLevel1 == True:
         
         'labels the game window'
         pygame.display.set_caption("G-ALEX-Y!")
         
         'sets up the clock'
         clock.tick(30)
         fireTimer += 1
         
         'hides mouse'
         pygame.mouse.set_visible(False)
         
         'sets up auto fire'
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
  
         'listens for key presses'
         keys = pygame.key.get_pressed()
          
         'if the up key is pressed' 
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
         'If the down key is pressed'
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
                  
         
         'if the ship collects a perl' 
         if ship.rect.colliderect(perl.rect):
             ship.sndPickUp.play()
             perl.reset()
             scoreboard.score += 100
         
         'When the ship shoots an alien'
         blastAlien1 = pygame.sprite.spritecollide(alien1, LaserSprites, False)
         if blastAlien1:
             alien1.health -= 20
             ship.sndThunder.play()
             for theLaser in blastAlien1:
                 theLaser.reset()
             if alien1.health < 1:
                 aliensDestroyed += 1
                 if aliensDestroyed == 15:
                     alien1.remove()
                     alien2.remove()
                     alien3.remove()
                     doneLevel1 = False
                     doneLevel2 = True
                 else:
                     alien1.reset()
                     scoreboard.booms += 1
         
         'When the ship shoots an alien'         
         blastAlien2 = pygame.sprite.spritecollide(alien2, LaserSprites, False)
         if blastAlien2:
             alien2.health -= 20
             ship.sndThunder.play()
             for theLaser in blastAlien2:
                 theLaser.reset()
             if alien2.health < 1:
                 aliensDestroyed += 1
                 if aliensDestroyed == 15:
                     alien1.remove()
                     alien2.remove()
                     alien3.remove()
                     doneLevel1 = False
                     doneLevel2 = True
                 else:
                     alien2.reset()
                     scoreboard.booms += 1
                      
         'When the ship shoots an alien'
         blastAlien3 = pygame.sprite.spritecollide(alien3, LaserSprites, False)
         if blastAlien3:
             alien3.health -= 20
             ship.sndThunder.play()
             for theLaser in blastAlien3:
                 theLaser.reset()
             if alien3.health < 1:
                 aliensDestroyed += 1
                 if aliensDestroyed == 15:
                     alien1.remove()
                     alien2.remove()
                     alien3.remove()
                     doneLevel1 = False
                     doneLevel2 = True
                 else:
                     alien3.reset()
                     scoreboard.booms += 1
        
         'If the user closes the window'
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 doneLevel1 = False
  
         'Updates the sprites'
         LaserSprites.update()
         friendSprites.update()
         AlienSprites.update()
         scoreSprite.update()
          
         'Draws the sprites to the screen'
         friendSprites.draw(screen)
         AlienSprites.draw(screen)
         scoreSprite.draw(screen)
         LaserSprites.draw(screen)
         pygame.display.flip()
    
    'Level 3'   
    while doneLevel2 == True:
         
         'labels the game window'
         pygame.display.set_caption("G-ALEX-Y!")
         
         'sets the clock up'
         clock.tick(30)
         fireTimer += 1
         
         'hides the mouse'
         pygame.mouse.set_visible(False)
         
         'sets up the fire timer'
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
            
            
         if fireTimer == 125 or fireTimer == 0:
            bossLaser1.fire()
         if fireTimer == 150 or fireTimer == 25:
            bossLaser2.fire()
         if fireTimer == 175 or fireTimer == 50:
            bossLaser3.fire()
         if fireTimer == 200 or fireTimer == 75:
            bossLaser4.fire()
    
         'listens for key presses'
         keys = pygame.key.get_pressed()
            
         'if the up key is pressed'
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
        
         'if the down key is pressed'
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
                     
         'if the boss hiyts the player'
         BossDamage = pygame.sprite.spritecollide(ship, BLaserSprites, False)
         if BossDamage:
            ship.sndThunder.play()
            scoreboard.lives -= 20
            if scoreboard.lives <= 0:
               keepGoing = False
               ship.sndMusic.stop()    
               GameOver(scoreboard.score)
            for theBLaser in BossDamage:
                theBLaser.reset()
         
         'if the ship collects a perl' 
         if ship.rect.colliderect(perl.rect):
             ship.sndPickUp.play()
             perl.reset()
             scoreboard.score += 100
         
         'if the user trys to close the window'
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                doneLevel2 = False
     
         'Updates the sprites'
         LaserSprites.update()
         BLaserSprites.update()
         friendSprites.update()
         BossSprite.update()
         scoreSprite.update()
             
         'Draws the sprites to the screen'
         friendSprites.draw(screen)
         BossSprite.draw(screen)
         BLaserSprites.draw(screen)
         scoreSprite.draw(screen)
         LaserSprites.draw(screen)
         pygame.display.flip()

    'stops the music'
    ship.sndMusic.stop()
    
    'shows the mouse'
    pygame.mouse.set_visible(True) 
    return scoreboard.score

'Main menu'
def titleScreen(): 
    
    'labels trhe game window'
    pygame.display.set_caption("G-ALEX-Y!")
    
    'sets up the ship and background sprites'
    ship = Ship()
    background = Background()
    
    'message for the  main menu'
    allSprites = pygame.sprite.Group(background)
    insFont = pygame.font.Font("Fipps-Regular.otf", 32)
    insLabels = []
    Message = (
    "        G-ALEX-Y" ,
    "",
    "",
    "",
    "",
    "     Enter - Start",
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
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
    doneLevel1 = False
    score = 0
    while not donePlaying:
        donePlaying = titleScreen()
        if not donePlaying:
            score = game()
            if doneLevel1 == True:
                score += level2()


if __name__ == "__main__":
    main()