from Tkinter import *
from ticker import Ticker
import time, threading
        
class DisplayTk(object):
    
    def __init__(self):
        
        self.ticker = Ticker()
        self.ticker.update_quote()
        
        self.rootWin = Tk()
        self.rootWin.protocol("WM_DELETE_WINDOW", self.tk_delete)
        
        self.quit = False
        self.displayDict = {}
        self.entry_count = 0
        self.timer_interval = 10000 #in ms
        

        rowVal = 0
        for elem in self.ticker.ticker_dict_list :

            labelStr = elem["Symbol"] + ": " + elem["LastTradePriceOnly"] 
            price = StringVar()
            Label(self.rootWin, textvariable=price).grid(row=rowVal, column=0)
            price.set(labelStr)
            
            labelStr = elem["ChangeinPercent"]
            percentChange = StringVar()
            Label(self.rootWin, textvariable=percentChange).grid(row=rowVal, column=1)
            percentChange.set(labelStr)
            rowVal += 1
            
            labelStr = "day: " + elem["DaysRange"]
            daysRange = StringVar()
            Label(self.rootWin, textvariable=daysRange).grid(row=rowVal)
            daysRange.set(labelStr)
            rowVal += 1
            
            labelStr = "52week: " + elem["YearRange"]
            yearRange = StringVar()
            Label(self.rootWin, textvariable=yearRange).grid(row=rowVal)
            yearRange.set(labelStr)
            rowVal += 1
            
            Label(self.rootWin, text="").grid(row=rowVal)
            rowVal += 1
            
            
            self.displayDict[elem["Symbol"]] = (price, percentChange, daysRange, yearRange)
            

        #threading.Timer(self.timer_interval, self.timer_callback).start()
        
            
    def tk_delete(self):
        print "deletion"
        self.quit = True
        self.rootWin.quit()
        
        
        
    def timer_callback(self):
        
        self.ticker.update_quote()
        
        if self.quit == True :
            print "quit"
            return

        
        for elem in self.ticker.ticker_dict_list :
            entry = elem["Symbol"]
            (price, percentChange, daysRange, yearRange) = self.displayDict[entry]
 
            labelStr = elem["Symbol"] + ": " + elem["LastTradePriceOnly"]
            price.set(labelStr)
            
            labelStr = elem["ChangeinPercent"]
            percentChange.set(labelStr)
            
            labelStr = "day: " + elem["DaysRange"]
            daysRange.set(labelStr)
            
            labelStr = "52week: " + elem["YearRange"]
            yearRange.set(labelStr)
          
            
            
        print "timer callback"
        #threading.Timer(self.timer_interval, self.timer_callback).start()                          
        self.rootWin.after(self.timer_interval, self.timer_callback)
        
    def display_loop(self):
        #print self.timer_interval
        self.rootWin.after(self.timer_interval, self.timer_callback)
        mainloop()    
        
def main():
    display = DisplayTk()
    display.display_loop()
    
    
if __name__ == "__main__":
    main()