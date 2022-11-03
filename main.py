import pygame
from pygame.locals import *
import time
import random


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
        self.direction = 'UP'
        self.parent_surface = parent_surface
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
        for i in range(self.length):
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
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((WIDTH,HEIGHT))
        # self.surface.fill(BACKGROUND_COLOR)
        self.render_background()
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    # check collission
    def is_collission(self,x1,y1,x2,y2):
        if (x1>=x2 and x1<x2+SIZE):
            if (y1>=y2 and y1<y2+SIZE):
                return True
        return False



    def score(self):
        font = pygame.font.SysFont("arial", 20)
        score = font.render(f"Score : {self.snake.length-1}", True, (255,255,255))
        self.surface.blit(score, (WIDTH-100,10))
    
    def render_background(self):
        bg = pygame.image.load('resources/background.jpg')
        self.surface.blit(bg, (0,0))

    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f'resources/{sound}.mp3')
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    # show on gameover 
    def game_gameover(self):
        self.play_sound('crash')
        # self.surface.fill(BACKGROUND_COLOR)
        self.render_background()

        font = pygame.font.SysFont("arial", 40)
        
        line1 = font.render(f"Game Over, Your Score is : {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (int(WIDTH/2)-300,int(HEIGHT/2)))

        line2 = font.render(f"Press Enter to restart the game.", True, (200,150,50))
        self.surface.blit(line2, (int(WIDTH/2)-300,int(HEIGHT/2)+40))

        pygame.display.flip()
        pygame.mixer.music.pause()

    # reset the game
    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)


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
                raise "Game over"
        
        # checking collision at boundaries
        if (self.snake.x[0]<0 or self.snake.x[0]>WIDTH or self.snake.y[0]<0 or self.snake.y[0]>HEIGHT ):
             raise "Game over"

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
                        pygame.mixer.music.unpause()
                        pause = False
                        # game = Game()
                        # game.run()
                    
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
            except Exception as e:
                self.game_gameover()
                pause = True
                # reset
                self.reset()
            time.sleep(0.2)
   


if __name__=="__main__":
    game = Game()
    game.run()
