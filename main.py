import pygame
from pygame.locals import *
import time
import random
from database import getLevel

# size of snzke
SIZE = 40
WIDTH = 1000
HEIGHT = 600
BACKGROUND_COLOR = (158, 27, 245)


# Ball
class Apple:
    def __init__(self,parent_surface):
        self.parent_surface = parent_surface
        self.x = random.randint(1, int(WIDTH/SIZE)-1)* SIZE
        self.y= random.randint(1, int(HEIGHT/SIZE)-1)* SIZE
        self.apple = pygame.image.load('resources/apple.jpg').convert()

    def draw(self):
        self.parent_surface.blit(self.apple,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, int(WIDTH/SIZE)-1)* SIZE
        self.y = random.randint(1, int(HEIGHT/SIZE)-1)* SIZE
        pygame.display.flip()

# Snake 
class Snake:

    # Initializing snake 
    def __init__(self,parent_surface,length):
        self.length = length
        self.x = [SIZE]*self.length
        self.y= [SIZE]*self.length
        self.increment= 40
        self.direction = 'DOWN'
        self.parent_surface = parent_surface
        self.snake_head = pygame.image.load('resources/head.png').convert()
        self.block = pygame.image.load('resources/block.jpg').convert()

    # increase snake length on collision with apple
    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)


    # Draw snake  
    def draw(self):
        # self.parent_surface.fill(BACKGROUND_COLOR)
        # self.render_background()
        self.parent_surface.blit(self.snake_head,(self.x[0],self.y[0]))
        for i in range(1,self.length):
            self.parent_surface.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
       

    def move_right(self):
        self.direction = 'RIGHT'
        # self.draw()

    def move_left(self):
        self.direction = 'LEFT'
        # self.draw()

    def move_up(self):
        self.direction = 'UP'
        # self.draw()

    def move_down(self):
        self.direction = 'DOWN'
        # self.draw()

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction=='UP':
            # print('moving up')
            self.y[0] -= self.increment
            
        if self.direction=='DOWN':
            # print('moving down')
            self.y[0] += self.increment
            
        if self.direction=='LEFT':
            # print('moving left')
            self.x[0] -= self.increment
            
        if self.direction=='RIGHT':
            # print('moving right')
            self.x[0] += self.increment
            
        self.draw()

# Game
class Game:

    def __init__(self):
        pygame.init()
        self.setLevel(1)
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((WIDTH,HEIGHT))
        # self.surface.fill(BACKGROUND_COLOR)
        self.render_background()
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        # self.level = None
        # self.title = None
        # self.target = None
        # self.background = None
        # self.speed = None
        self.level_completed = False
    
    # set level
    def setLevel(self,level):
        level = getLevel(level)
        self.level = level[0]
        self.title = level[1]
        self.target = level[2]
        self.background = level[3]
        self.speed = level[4]
        self.music = level[5]
        print(self.music)


    # check collission
    def is_collission(self,x1,y1,x2,y2):
        if (x1>=x2 and x1<x2+SIZE):
            if (y1>=y2 and y1<y2+SIZE):
                return True
        return False

    def score(self):
        font = pygame.font.SysFont("arial", 20)
        score = font.render(f"Score : {self.snake.length-1}/{self.target}", True, (255,255,255))
        self.surface.blit(score, (WIDTH-150,10))
    
    def render_background(self):
        bg = pygame.image.load(f'resources/background/{self.background}')
        self.surface.blit(bg, (0,0))

    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f'resources/{sound}.mp3')
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        pygame.mixer.music.load(f'resources/music/{self.music}.mp3')
        pygame.mixer.music.play()

    # show on gameover 
    def game_gameover(self):
        self.play_sound('crash')
        self.render_background()

        font = pygame.font.SysFont("arial", 40)

        title = font.render(f"{self.title}", True, (255,255,255))
        self.surface.blit(title, (100,100))
        
        line1 = font.render(f"Game Over, Your Score is : {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (100,150))

        line2 = font.render(f"Press Enter to restart the game.", True, (200,150,50))
        self.surface.blit(line2, (100,200))

        pygame.mixer.music.stop()
        pygame.display.flip()
    
     # show on gameover 
    def level_complete(self):
        # self.play_sound('success')
        font = pygame.font.SysFont("arial", 40)

        title = font.render(f"{self.title}", True, (255,255,255))
        self.surface.blit(title, (100,100))
        
        line1 = font.render(f"Hurrey! Level Complete, {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (100,150))

        line2 = font.render(f"Press Enter to play the next level.", True, (200,150,50))
        self.surface.blit(line2, (100,200))

        pygame.mixer.music.stop()
        pygame.display.flip()

    # reset the game
    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)
        # self.play_background_music()
        self.render_background()

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()

        # snake eating apple
        if self.is_collission(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            # print("Collisiion")
            self.play_sound('ding')

            self.snake.increase_length()
            self.apple.move()
        # snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collission(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.level_completed = False
                raise "Game over"
        
        # checking collision at boundaries
        if (self.snake.x[0]<0 or self.snake.x[0]>WIDTH or self.snake.y[0]<0 or self.snake.y[0]>HEIGHT ):
            self.level_completed = False
            raise "Game over"

        if (self.target == self.snake.length+1):
            self.level_completed = True
            raise "Level Complete"


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                # print("running")
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        # pygame.mixer.music.unpause()
                        self.play_background_music()
                        pause = False
                        self.level_completed = False
                    
                    # When game is not paused
                    if not pause:
                        if event.key == K_RIGHT:
                            # print("Direction changed to :",self.snake.direction)
                            self.snake.move_right()
                            
                        if event.key == K_LEFT:
                            # print("Direction changed to :",self.snake.direction)
                            self.snake.move_left()
                        
                        if event.key == K_UP:
                            # print("Direction changed to :",self.snake.direction)
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            # print("Direction changed to :",self.snake.direction)
                            self.snake.move_down()
                    
                if event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception :
                pause = True
                if self.level_completed:
                    print("+++++")
                    self.level_complete()
                    self.reset()
                    try:
                        self.setLevel(self.level+1)
                    except:
                        self.setLevel(1)
                else:
                    print("------")
                    self.game_gameover()
                    # pause = True
                    # reset
                    self.reset()
            time.sleep(self.speed)

if __name__=="__main__":
    game = Game()
    game.run()
