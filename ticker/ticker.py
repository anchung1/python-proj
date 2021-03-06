import urllib2
import re



#http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20%20%28%22GM%22%2C%22ANET%22%2C%22MA%22%2C%22YHOO%22%2C%22FB%22%2C%22AMZN%22%2C%22CSCO%22%29&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env

class Ticker(object):
    def __init__(self):
        self.results = ""
        self.quotes = ""
        self.current_buffer = ""
        self.quote_list = []
        self.ticker_dict_list = []
    
    def get_raw_quote(self):
        req_str = """http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20%20%28%22GM%22%2C%22ANET%22%2C%22MA%22%2C%22YHOO%22%2C%22FB%22%2C%22AMZN%22%2C%22CSCO%22%29&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env"""
        
        req = urllib2.Request(req_str)
        try:
            response = urllib2.urlopen(req)
        except:
            return ""
            
        resPage = response.read()
        return resPage
        
    def get_results_tag(self):
        raw_quote = self.get_raw_quote()
        if len(raw_quote) == 0 :
            return False
        
        
        matchObj = re.match('(.*?)\n(.+)', raw_quote)
        if matchObj == None:
            print "cannot find <results>"
            print raw_quote
            return
        
        
        raw_quote = matchObj.group(2)
        
        matchObj = re.match('.+<results>(.+)</results>', raw_quote)
        self.quotes = matchObj.group(1)
        self.current_buffer = self.quotes
        
        return True
        
    def get_quote_tag(self):
        
        if self.get_results_tag() == False :
            return False
        
        while True:
            matchObj = re.match('(<quote (.*?)</quote>)(.+)?', self.current_buffer)
            if matchObj == None:
                print "no match bail"
                print self.current_buffer
                break
            if matchObj.lastindex < 3:
                #print "last elem"
                break
            self.current_buffer = matchObj.group(3)
            self.quote_list.append(matchObj.group(1))
        
        return True
        
    def get_field(self, fieldName, quote):
        
        expression = ".*?<" + fieldName + ">(.*)</" + fieldName + ">(.+)"
        matchObj = re.match(expression, quote)
        #return matchObj.group(1), matchObj.group(2)
        return matchObj.group(1)
            
    def parse_quote(self, quote):
        dict = {}
        
        matchObj = re.match("<quote symbol=.*?>(.+)", quote)
        quote = matchObj.group(1)
        #symbol = matchObj.group(1)
        #symbol = re.sub('"', '', symbol)
        #dict["symbol"] = symbol
    
        extract = "DaysLow"    
        val = self.get_field(extract, quote)
        dict[extract] = val
        
        extract = "DaysHigh"    
        val = self.get_field(extract, quote)
        dict[extract] = val

        extract = "YearLow"    
        val = self.get_field(extract, quote)
        dict[extract] = val

        extract = "YearHigh"    
        val = self.get_field(extract, quote)
        dict[extract] = val
        
        extract = "LastTradePriceOnly"    
        val = self.get_field(extract, quote)
        dict[extract] = val
    
        extract = "Name"    
        val = self.get_field(extract, quote)
        dict[extract] = val
    
        extract = "Open"    
        val = self.get_field(extract, quote)
        dict[extract] = val
    
        extract = "ChangeinPercent"    
        val = self.get_field(extract, quote)
        dict[extract] = val    
    
        extract = "Symbol"    
        val = self.get_field(extract, quote)
        dict[extract] = val
        
        extract = "DaysRange"
        val = self.get_field(extract, quote)
        dict[extract] = val

        extract = "YearRange"
        val = self.get_field(extract, quote)
        dict[extract] = val
        
        
        
        #print dict
        self.ticker_dict_list.append(dict)
        
    def update_quote(self):
        #print "update_quote"
        if self.get_quote_tag() == False :
            print "unable to get quote"
            return False
        
        for elem in self.quote_list :
            self.parse_quote(elem)
        #for elem in self.ticker_dict_list :
            #print elem["Symbol"] + " " + elem["LastTradePriceOnly"]
        
        return True

