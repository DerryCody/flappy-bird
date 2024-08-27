import pygame, random, time
pygame.init()

WIDTH=864
HEIGHT=768
TITLE="FLAPPY BIRD"

go=False
flying=False
running=True
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
groundx=0
bv=0
space=150
jumping=False
wt=3000
last_time=pygame.time.get_ticks()-wt
score=0
font=pygame.font.SysFont("TimesNewRoman",50)
passing=False

bg1=pygame.image.load("FB BG.png")
bg2=pygame.image.load("FB DOWN.png")
bg3=pygame.image.load("FB GROUND.png")
bg4=pygame.image.load("FB UP.png")
bg5=pygame.image.load("PIPE.png")
bg6=pygame.image.load("BIRD.png")
bg7=pygame.image.load("RESTART.png")


class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.images=[bg6,bg4,bg2]
        self.index=0
        self.counter=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vel=bv
        self.clicked=False
    def update(self):
        global flying
        if flying==True:
            self.vel=self.vel+0.25
            if self.vel>5:
                self.vel=5
            self.rect.y=self.rect.y+self.vel
        if self.clicked==True:
            self.vel=-5

bird=Bird(100,384)
birds=pygame.sprite.Group()
birds.add(bird)

class Pipes(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        super().__init__()
        self.image=bg5
        self.rect=self.image.get_rect()
        if pos==1:
            self.image=pygame.transform.flip(bg5,False,True)
            self.rect.bottomleft=x,y-space/2
        else:
            self.rect.topleft=x,y+space/2
    def update(self):
        self.rect.x=self.rect.x-2
        if self.rect.right<0:
            self.kill()
pipes=pygame.sprite.Group()

while running==True: 
  for event in pygame.event.get(): 
    if event.type==pygame.QUIT:
      running=False
    if event.type==pygame.MOUSEBUTTONDOWN and go==False:
        bird.image=bird.images[1]
        bird.clicked=True
    if event.type==pygame.MOUSEBUTTONUP and go==False:
        bird.image=bird.images[2]
        bird.clicked=False
        if flying==False and go==False:
            flying=True     
  
  if running==True and flying==True:
    time_now=pygame.time.get_ticks()
    groundx=groundx-1
    if groundx<=-36:
      groundx=0
    pipes.update()
    if time_now-last_time>wt:
        distance=random.randint(-100,100)
        pipe1=Pipes(864,384+distance,+1)
        pipe2=Pipes(864,384+distance,+0)
        pipes.add(pipe1)
        pipes.add(pipe2) 
        last_time=time_now
  if bird.rect.bottom>650:
    flying=False
    go=True
  if bird.rect.top<0:
    bird.clicked=False
    go=True 
  if len(pipes)>0:
      if pygame.sprite.groupcollide(pipes,birds,False,False):
          go=True
      if bird.rect.bottom>=650:
          flying=False
      if pipes.sprites()[0].rect.left<bird.rect.right and pipes.sprites()[1].rect.right>bird.rect.left and passing==False:
          passing=True
      if passing==True:
         if pipes.sprites()[0].rect.right<bird.rect.left:
           score=score+1
           passing=False
    
  screen.blit(bg1,(0,0))
  score_message=font.render("Score is "+str(score),True,"black")
  screen.blit(score_message,(30,40))
  pipes.draw(screen)
  screen.blit(bg3,(groundx,650))
  birds.draw(screen)  
  bird.update()
  pygame.display.update()    