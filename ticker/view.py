import pygame
from ticker import Ticker

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
class Display(object):
    
    def __init__(self):
        
        self.ticker = Ticker()
        self.ticker.update_quote()
        
        pygame.init()
         
        # Set the width and height of the screen [width, height]
        self.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
         
        pygame.display.set_caption("Ticker LLC")
        self.setup_font()
         
        # Loop until the user clicks the close button.
        self.done = False
         
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        self.time_elapsed = pygame.time.get_ticks()

        self.displayList = []
        
    def setup_font(self): 
        if pygame.font:
            
            self.fontBigSize = 34
            self.fontSmallSize = 24
            self.fontBig = pygame.font.Font(None, self.fontBigSize)
            self.fontSmall = pygame.font.Font(None, self.fontSmallSize)
            
 
            #self.bigText = fontBig.render("big font", 1, (10,10,10))
            #self.smallText = fontSmall.render("small font", 1, (10,10,10))
            
            
    def elapsed(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_elapsed > 10000 :
            print "10sec elapsed"
            self.time_elapsed = current_time
            self.ticker.update_quote()
            
            self.displayList = []
            for elem in self.ticker.ticker_dict_list :
                name = elem["Name"]
                symbol = elem["Symbol"]
                price = elem["LastTradePriceOnly"]
                self.displayList.append((elem["Name"], elem["Symbol"], elem["LastTradePriceOnly"]))
                print symbol + ": " + price
                


                           
    def text_render(self):
        initX = 50
        initY = 50
        offsetX = 0
        offsetY = 0

        ticker_list = self.ticker.ticker_dict_list        
        for (name, symbol, price) in self.displayList:
 
            bigText = self.fontBig.render(name, 1, (10,10,10))
            self.screen.blit(bigText, (initX+offsetX, initY+offsetY))
            
            offsetX += 0
            offsetY += self.fontBigSize

            smallStr = symbol + "        " + price
            smallText = self.fontSmall.render(smallStr, 1, (10,10,10))
            self.screen.blit(smallText, (initX+offsetX, initY+offsetY))
            
            
            
            offsetX += 0
            offsetY += self.fontSmallSize + self.fontBigSize
                    

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
            self.text_render()         
            self.elapsed()
         
            
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
         
            # --- Limit to 60 frames per second
            self.clock.tick(60)
         
        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.quit()
        
def main():

        
    display = Display()
    display.display_loop()
    
    
if __name__ == "__main__":
    main()
    

