import pygame


# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
class Display(object):
    
    def __init__(self):
        pygame.init()
         
        # Set the width and height of the screen [width, height]
        self.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
         
        pygame.display.set_caption("Ticker LLC")
         
        # Loop until the user clicks the close button.
        self.done = False
         
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def display_loop(self):
        
        # -------- Main Program Loop -----------
        while not self.done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                    #print "done"
                       
                             
            # --- Game logic should go here
         
            # --- Drawing code should go here
         
            # First, clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            self.screen.fill(WHITE)
         
            
         
            
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
         
            # --- Limit to 60 frames per second
            self.clock.tick(60)
         
        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.quit()