from Tkinter import *
from ticker import Ticker
import time, threading


        
class DisplayTk(object):
    
    def __init__(self):
        
        self.ticker = Ticker()
        self.ticker.update_quote()
        self.master = Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.tk_delete)
        
        self.quit = False
        self.displayDict = {}
        self.entry_count = 0
        
        for elem in self.ticker.ticker_dict_list :
            Label(self.master, text=elem["Name"]).pack()
            labelStr = elem["Symbol"] + ": " + elem["LastTradePriceOnly"] + "\n"
            
            textVar = StringVar()
            Label(self.master, textvariable=textVar).pack()
            textVar.set(labelStr)
            
            self.displayDict[elem["Symbol"]] = textVar

        threading.Timer(1, self.timer_callback).start()
            
    def tk_delete(self):
        print "deletion"
        self.quit = True
        self.master.quit()
        
        
        
    def timer_callback(self):
        if self.quit == True :
            return

        self.entry_count += 1
        self.ticker.update_quote()
        for elem in self.ticker.ticker_dict_list :
            entry = elem["Symbol"]
            textVar = self.displayDict[entry]
            
            labelStr = ""
            if elem["Symbol"] != "AMZN" :
                labelStr = elem["Symbol"] + ": " + elem["LastTradePriceOnly"] + "\n"
            else :
                if self.entry_count % 2 == 0 :
                    labelStr = elem["Symbol"] + ": " + elem["LastTradePriceOnly"] + "\n"
                else :    
                    labelStr = elem["Symbol"] + ": " + "1"
            textVar.set(labelStr)
            
        print "timer callback"
        threading.Timer(1, self.timer_callback).start()                          
        
    def display_loop(self):
        mainloop()    
        
def main():
    display = DisplayTk()
    display.display_loop()
    
    
if __name__ == "__main__":
    main()