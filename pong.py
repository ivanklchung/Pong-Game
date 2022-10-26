# This game will be a 2 player game called Pong.
# There will be a left player and a right player each
# with a paddle. The ball will keep bouncing off each player's
# paddle until the ball hits their net. If it hits a player's net,
# the opponent scores a point. First player to score 11 points wins the match.
# Left player uses q and a key to move paddle up and down respectively.
# Right player uses p and l keys to move paddle up and down respectively.

# Version 9
# fix bugs, paddle problem, 

# Version 8
# scorebaord and scores

# Version 7
# Collision scenarios
# with paddles

# Version 6 
# Collision scenarios
# with walls

# Version 5
# make sure paddle doesn't cross the edge of window

# Version 4
# make the game play
# ball and paddle movement insert function into their classes

# Version 3
# make the screen, colors, main loop
# start Ball class and Paddle Class

# Version 2
# work on main function and basics of the game

# Version 1
# download pygame template

import pygame


# User-defined functions

def main():

    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window 
    pygame.display.set_mode((1000, 500))
    # set the title of the display window
    pygame.display.set_caption('Pong')   
    # get the display surface
    w_surface = pygame.display.get_surface()
    # print the dimensions of the window
    # window_width,window_height =  w_surface.get_width(), w_surface.get_height()    
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game:
    # An object in this class represents a complete game.
    # everything I need throughout game should be here 

    def __init__(self, surface):
        # - Initialize a Game.
        # - self = initialize the Game 
        # - surface =  display window surface object
        
        # === objects that are part of every game that we will discuss
        # sets surface 
        self.surface = surface
        # sets background to color black
        self.bg_color = pygame.Color('black')

        self.FPS = 50
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
        self.frame_counter = 0
        
        # === game specific objects
        
        # starting positions
        
        # sets left team as color
        self.leftteam_color = pygame.Color('green')
        # sets right team as color
        self.rightteam_color = pygame.Color('blue')
        
        
        # initial score for both team 
        self.left_team_score = 0
        self.right_team_score = 0


        # the initial y coordinates of both paddles
        self.paddle1 = int(self.surface.get_height()/2)-  20
        self.paddle2 = int(self.surface.get_height()/2) - 20
        
        

        # paddle initial velocity, not moving 
        self.paddle1_velocity = 0
        self.paddle2_velocity = 0

        # making the ball and paddle objects
        self.ball = Ball('red', 5, [int(self.surface.get_width()/2), int(self.surface.get_height()/2)], [5, 3], self.surface)
        self.left_paddle = Paddle('green', pygame.Rect(200, self.paddle1, 20, 50), 5, self.surface)
        self.right_paddle = Paddle('blue', pygame.Rect(self.surface.get_width() - 200, self.paddle2, 20, 50), 5, self.surface)
        
        

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # - Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
                
                
                
            if event.type == pygame.KEYDOWN:

                # left paddle pressed
                if event.key == pygame.K_q:
                    self.paddle1_velocity = 7
                elif event.key == pygame.K_a:
                    self.paddle1_velocity = -7

                # right paddle pressed
                if event.key == pygame.K_p:
                    self.paddle2_velocity= 7
                elif event.key == pygame.K_l:
                    self.paddle2_velocity= -7

            if event.type == pygame.KEYUP:
                # left paddle released
                if event.key == pygame.K_q or event.key == pygame.K_a:
                    self.paddle1_velocity = 0
                # left paddle released
                if event.key == pygame.K_p or event.key == pygame.K_l:
                    self.paddle2_velocity= 0


    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        # draws ball, right and left paddle and the scores
        self.surface.fill(self.bg_color) # clear the display surface first
        self.ball.draw()
        self.left_paddle.draw()
        self.right_paddle.draw()
        self.score('right_team')
        self.score('left_team')
        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        # Update the paddle position and velocity
        # Update score board
        # - self is the Game to update

        # paddle position 
        
        # hits the top of screen
        if self.paddle1 - self.paddle1_velocity < 0:
            self.paddle1 = 0
        
        # hits the bottom of screen
        elif self.paddle1 + 50 - self.paddle1_velocity > self.surface.get_height():
            self.paddle1 = self.surface.get_height() - 50
            
        else: 
        # subtract 0, keep the paddle the way it is 
            self.paddle1 -= self.paddle1_velocity
            
        # same theory for paddle 2

        if self.paddle2 - self.paddle2_velocity< 0:
            self.paddle2 = 0
        elif self.paddle2 + 50 - self.paddle2_velocity> self.surface.get_height():
            self.paddle2 = self.surface.get_height() - 50
        else: 
            self.paddle2 -= self.paddle2_velocity

        # paddle 1 and 2 are updated, because they will be drawn
        self.left_paddle = Paddle('green', pygame.Rect(100, self.paddle1, 20, 50), 5, self.surface)
        self.right_paddle = Paddle('blue', pygame.Rect(self.surface.get_width() - 100, self.paddle2, 20, 50), 5, self.surface)
        
        
        
        scored = self.ball.move(self.left_paddle, self.right_paddle)
        
        # if the variable scored is updated to 'right goal'
        # LEFT team scores, it hit RIGHT wall
        if scored == 'right_goal':
            self.left_team_score = self.left_team_score + 1
            
        # if the variable scored is updated to 'left goal'
        # RIGHT team scores, it hit LEFT wall        
        elif scored == 'left_goal':
            self.right_team_score += 1

        # frame counter keeps going up 1, after each update
        self.frame_counter = self.frame_counter + 1

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        
        # seeing if the game is over, cap limit is 11
        if self.right_team_score == 11 or self.left_team_score == 11:
            self.continue_game = False

    def score(self, scoreboard):
        # sets text score
        # - self is Game
        # - side is which side the text is displayed

        # use default system font 
        font = pygame.font.SysFont('', 100)
        coor_x = 10
        coor_y = 0
        if scoreboard == 'left_team':
            # if left side, render text at (50,0)
            coordinate = (coor_x, coor_y)
            text_box = font.render(str(self.left_team_score), True, self.leftteam_color, self.bg_color)
        if scoreboard == 'right_team':
            

            # if right side, render text on the right side
            text_box = font.render(str(self.right_team_score), True, self.rightteam_color, self.bg_color)
            text_rect = text_box.get_rect() # get rect from textbox
            text_rect.right = self.surface.get_width()
            coordinate = [text_rect[0] - coor_x, text_rect[1]]
            
            
        # prints to surface
        self.surface.blit(text_box, coordinate)


class Ball:
    # An object in this class represents objects in the game

    def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
        # Initialize a Ball.
        # - self = Ball to initialize
        # - ball_color = pygame.Color of the ball
        # - ball_radius =  the radius of the ball
        # - ball_center = list of x and y coordinates
        # - ball_velocity = list of x and y coordinates
        # - surface = surface object, the window's pygame
        
      
        self.color = pygame.Color(ball_color)
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.surface = surface

    def move(self, left_paddle, right_paddle):
        # Change the location of the Ball by adding the corresponding 
        # speed values to the x and y coordinate of its center
        # - self is the Ball
        # - paddle1 is the top position of left paddle
        # - paddle2 is the top position of right paddle

        # default score is pass
        scored = 'done'

        
        for i in range(0,2):
            # horizontal motion
            if i == 0:
                # seeing which wall
                # if right wall OR left wall
                if self.surface.get_width() < self.center[i]  + self.velocity[i] or 0 > self.center[i]  + self.velocity[i]:
                    # hits either, will change direction velocity
                    self.velocity[i] = -self.velocity[i]
                    # see which net/wall, it hits, the opposite side will get scored
                    if self.velocity[i] > 0:
                        scored = 'left_goal'  # bounce off right wall
                    else:
                        scored = 'right_goal'  # bounce off left wall

        
            # vertical motion       
            # bounching off top and bottom wall
            if i == 1:
                if self.surface.get_height() < self.center[i] + self.velocity[1] + self.velocity[i] or 0 > self.center[i] - self.velocity[1] + self.velocity[i]:
                    self.velocity[i] = -self.velocity[i]
            self.center[i] = (self.center[i] + self.velocity[i])  
        

        # paddle 
        if left_paddle.get_center().collidepoint([ self.center[0] - self.radius ,self.center[1]] ) and self.velocity [0] < 0:
            self.velocity[0] = - self.velocity[0]        
        
        if right_paddle.get_center().collidepoint( [self.center[0] - self.radius ,self.center[1]] ) and self.velocity [0] > 0:
            self.velocity[0] = - self.velocity[0]        

        # return which side scored
        return scored

    def draw(self):
        # Draw the ball on the surface
        # - self is the Ball
        
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)


class Paddle:
    # An object in this class represents objects in the game
    
    def __init__(self, paddle_color, paddle_object, paddle_velocity, surface):
        # - Initialize the Paddles.
        # - self = Paddle to initialize
        # - paddle_color = pygame.Color of the paddle
        # - paddle_object= make an object of paddle as a Rect
        # - paddle_velocity = list of x and y coordinates
        # - surface = surface object, the window's pygame
        

        self.color = pygame.Color(paddle_color)
        self.center = paddle_object
        self.velocity = paddle_velocity
        self.surface = surface
    
    def draw(self):
        # Draw the paddle on the surface
        # - self is the Paddle

        pygame.draw.rect(self.surface, self.color, self.center)
    
    def get_center(self):
        return self.center # used self.center
        
    

# main function call
main()