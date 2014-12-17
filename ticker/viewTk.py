from Tkinter import *
from ticker import Ticker
import time, threading
import re
        
class DisplayTk(object):
    
    def __init__(self):
        
        self.ticker = Ticker()
        if self.ticker.update_quote() == False :
            return
        
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
            symbolWidget = Label(self.rootWin, textvariable=price)
            symbolWidget.grid(row=rowVal, column=0)
            price.set(labelStr)
            
            labelStr = elem["ChangeinPercent"]
            percentChange = StringVar()
            percentWidget = Label(self.rootWin, textvariable=percentChange)
            percentWidget.grid(row=rowVal, column=1)
            percentChange.set(labelStr)
            rowVal += 1
            
            self.color_code(labelStr, symbolWidget, percentWidget)

            
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
            
            
            self.displayDict[elem["Symbol"]] = \
                (price, percentChange, daysRange, yearRange, symbolWidget, percentWidget)
            

        #threading.Timer(self.timer_interval, self.timer_callback).start()
        
            
    def tk_delete(self):
        print "deletion"
        self.quit = True
        self.rootWin.quit()
        
    def color_code(self, labelStr, symbolWidget, percentWidget):   
            if labelStr[0] == "+" :
                symbolWidget.config(fg = "blue")
                percentWidget.config(fg = "blue")
            else :
                symbolWidget.config(fg = "red")
                percentWidget.config(fg = "red")
                 
        
    def timer_callback(self):
        
        if self.ticker.update_quote() == False :
            self.rootWin.after(self.timer_interval, self.timer_callback)
            return 
        
        if self.quit == True :
            print "quit"
            return

        
        for elem in self.ticker.ticker_dict_list :
            entry = elem["Symbol"]
            (price, percentChange, daysRange, yearRange, symbolWidget, percentWidget) \
                = self.displayDict[entry]
 
            labelStr = elem["Symbol"] + ": " + elem["LastTradePriceOnly"]
            price.set(labelStr)
            
            labelStr = elem["ChangeinPercent"]
            percentChange.set(labelStr)
            self.color_code(labelStr, symbolWidget, percentWidget)
            
            labelStr = "day: " + elem["DaysRange"]
            daysRange.set(labelStr)
            
            labelStr = "52week: " + elem["YearRange"]
            yearRange.set(labelStr)
          
            
            
        #print "timer callback"
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