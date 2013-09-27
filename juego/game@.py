import pygame, sys
import math
from pygame import *

Size = (1200, 600)
FLAGS = 0
Resolution = 32
v=3
def game():
    pygame.init()
    screen = display.set_mode(Size, FLAGS, Resolution)
    display.set_caption("Vidas: "+str(v))
    timer = time.Clock()

    up = down = left = right = False
    bg=Surface((1200,600))
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    arthur = Arthur(20,20)
    platforms = []

    x = y = 0
    level = [
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                                     P",
    "P        pppp                                                P",
    "P        pppE                 p                              P",
    "P                          p     p     p                     P",
    "P                    ppp            p    p                    P",
    "P                                                      L     P",
    "PPPPPPPPPPPPPPPPPPPPPPPDDDDDDDDDDDDDDDDPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            ]

    #builds the level
    for row in level:
        for col in row:
            if col =="p":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "L":
                L = LevelBlock(x, y)
                platforms.append(L)
                entities.add(L)
            if col == "D":
                Death = DangerBlock(x, y)
                platforms.append(Death)
                entities.add(Death)
            if col == "P":
                P = Border(x, y)
                platforms.append(P)
                entities.add(P)
            x += 18
        y += 18
        x = 0
    entities.add(arthur)

    while 1:
        timer.tick(20)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
                #raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                #raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True


            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        #draw bg
        for y in range(20):
            for x in range(25):
                screen.blit(bg, (x * 32, y * 32))

        #update player, draw everything else
        arthur.update(up, down, left, right, platforms)
        entities.draw(screen)
        screen.blit(arthur.image, arthur.rect)
        pygame.display.flip()

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Arthur(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.sheet = pygame.image.load('Arthur/arthur2.png')
        self.sheet.set_clip(pygame.Rect((252,4), (32,41 )))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = ( x, y)
        self.frame = 0
        res = self.reset(50, 300)
        
        self.left_states = { 0: (252, 3, 28, 41),
                             1: (225, 5, 27, 41),
                             2: (192, 5, 32, 41),
                             3: (164, 4, 32, 41),
                             3: (141, 5, 24, 41),
                             4: (107, 5, 31, 41),
                             5: (79, 5, 27, 41) }
        self.right_states = { 0: (284, 5, 29, 43),
                              1: (313, 5, 27, 43),
                              2: (338, 5, 32, 41),
                              3: (399, 5, 24, 41),
                              4: (425, 5, 31, 41),
                              5: (457, 5, 28, 41) }
        self.up_states = { 0: (284, 81, 29, 43),
                           1: (312, 81, 29, 43),
                           2: (225, 81, 29, 43) }
        self.down_states = { 0: (252, 81, 29, 43),
                             1: (225, 81, 29, 43),
                             2: (312, 81, 29, 43) }
        self.jump_states = { 0:(282, 48, 29, 37)}
        self.jump_right_states = { 0: (206, 47, 29, 43)}
        self.jump_left_states = { 0: (315 ,48, 34, 43)}
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
    def reset(self,x,y):
        self.x = x
        self.y = y

        self.rect.center = (self.x, self.y)

    def update(self, up, down, left, right, platforms):
        if up:
            #only jump if on the ground
            if self.onGround:
                animation = self.clip(self.jump_states)
                self.yvel = -16
        if down:
            animation = self.clip(self.down_states)
            pass
        if left:
            animation = self.clip(self.left_states)
            self.xvel = -5
        if right:
            animation = self.clip(self.right_states)
            self.xvel = 5
        if not self.onGround:
            #only accelerate wit gravity if in the air
            self.yvel +=3
            #max falling sapeed
            if self.yvel > 30:
                self.yvel = 30
        if not (left or right):
            animation = self.clip(self.right_states[0])
            self.xvel = 0

        # increment in x direction
        self.rect.left+= self.xvel
        # x-axis collisions
        self.collide(self.xvel, 0 , platforms)
        # increment in y direction
        self.rect.top +=self.yvel
        # assuming we're in the air
        self.onGround = False;
        # y-axis collisions
        self.collide(0, self.yvel, platforms)
        self.image = self.sheet.subsurface(self.sheet.get_clip())
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    event.post(event.Event(QUIT))
                elif isinstance(p, DangerBlock):
                    display.set_caption("Vidas: "+str(v-1))
                    self.rect.x=50
                    self.rect.y=300
                elif isinstance(p, LevelBlock):
                    display.set_caption("Pasaste de nivel!!")
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                        self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                   # Player.rect.top =  Player.rect.top


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((18,18))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 18, 18)

        def update(self):
            pass

class Border(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((18,18))
        self.image.convert()
        self.image.fill((0,0,0))
        self.rect = Rect(x, y, 18,18)

        def update(self):
            pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))
class DangerBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color('red'))
class LevelBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("green"))



game()
