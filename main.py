import pygame, sys, random # type: ignore
from pygame.math import Vector2 # type: ignore

pygame.init()

title_font = pygame.font.Font(None, 45)
score_font = pygame.font.Font(None, 25)
 
  #<|variables|>#

BG_COLOR = (156, 200, 255)
SNAKE_COLOR = (2, 74, 191)
SNAKE_OFFSET = (2, 76, 204)

cell_size = 30
number_of_cell = 25

OFFSET = 50

#<|Clases|>#

class Food:
    def __init__(self, snake_body):
      self.position = self.generate_ramdom_pos(snake_body)

    def draw(self):
        Food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET +self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, Food_rect)
    
    def generate_random_cell(self):
      x = random.randint(0, number_of_cell - 1)
      y = random.randint(0, number_of_cell - 1)
      return Vector2(x, y)

    def generate_ramdom_pos(self, snake_body):
      
      position = self.generate_random_cell()
     
      while position in snake_body:
        position = self.generate_random_cell()

      return position

class Snake:
  def __init__(self):
    self.body = [Vector2(6, 9), Vector2(5,9), Vector2 (4,9)]
    self.direction = Vector2(1,0)
    self.next_direction = Vector2(1,0)
    self.add_segment = False
    self.eat_sound = pygame.mixer.Sound("sound/bloxy-cola.mp3")
    self.wall_sound = pygame.mixer.Sound("sound/wall.mp3")
    
  
  def draw(self):
    for segment in self.body:
      segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
      pygame.draw.rect(screen, SNAKE_COLOR, segment_rect,0, 6)
      
  def update(self):
    self.direction = self.next_direction
    self.body.insert(0, self.body[0] + self.direction)
    if self.add_segment == True:
      self.add_segment = False
    else:
      self.body.pop()

  def reset(self):
    self.body = [Vector2(6, 9), Vector2(5,9), Vector2 (4,9)]
    self.direction = Vector2(1,0)
    
class Game:
  def __init__(self):
    self.snake = Snake()
    self.food = Food(self.snake.body)
    self.state = "jugando"
    self.score = 0
    
  def draw(self):
    self.snake.draw()
    self.food.draw()
    
  def update(self):
   if self.state == "jugando":
    self.snake.update()
    self.check_colision_with_food()
    self.check_collision_with_edges()
    self.check_tail_collision()
  
  def check_colision_with_food(self):
    if self.snake.body[0] == self.food.position:
      self.food.position = self.food.generate_ramdom_pos(self.snake.body)
      self.snake.add_segment = True
      self.score += 1
      self.snake.eat_sound.play()
      
  def check_collision_with_edges(self):
    if self.snake.body[0].x == number_of_cell or self.snake.body[0].x == -1:
      self.game_over()
    if self.snake.body[0].y == number_of_cell or self.snake.body[0].y == -1:
      self.game_over()

  def game_over(self):
   self.snake.reset()
   self.food.position = self.food.generate_ramdom_pos(self.snake.body)
   self.state = "perdistes"
   self.score = 0
   self.snake.wall_sound.play()
  
  def check_tail_collision(self):
    headless_body = self.snake.body[1:]
    if self.snake.body[0] in headless_body:
      self.game_over()                 


    
screen = pygame.display.set_mode((2*OFFSET+cell_size*number_of_cell, 2*OFFSET+cell_size*number_of_cell ))

pygame.display.set_caption("retro snake")

clock = pygame.time.Clock()

game = Game()

food_surface = pygame.image.load("bloxiade.png")

SNAKE_UPDATE = pygame.USEREVENT

pygame.time.set_timer(SNAKE_UPDATE, 110)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SNAKE_UPDATE:
          game.update()
          
        if event.type == pygame.KEYDOWN:
          if game.state == "perdistes":
           game.state = "jugando"
          
          if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
           game.snake.next_direction = Vector2(0, -1)
          if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
           game.snake.next_direction = Vector2(0, 1)
          if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
           game.snake.next_direction = Vector2(-1, 0)
          if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
           game.snake.next_direction = Vector2(1, 0)
    
    screen.fill(BG_COLOR)       
    
    pygame.draw.rect(screen, SNAKE_OFFSET, (OFFSET - 5,  OFFSET - 5, cell_size*number_of_cell + 10, cell_size*number_of_cell), 5)

    game.draw()
    title_surface = title_font.render("Retro Snake",True, SNAKE_OFFSET)
    score_surface = score_font.render(str(game.score), True, SNAKE_OFFSET)

    screen.blit(title_surface, (OFFSET -15, 20))
    screen.blit(score_surface, (OFFSET + cell_size*number_of_cell + 10, OFFSET - 5))
    
    pygame.display.update()
    clock.tick(60)        



