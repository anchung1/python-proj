import urllib2
import re
import pygame


class Flickr(object):
    def __init__(self, api_key, secretKey): 
        self.flickr_api_key = "&api_key=" + api_key
        self.flickr_secret_key = secretKey

        self.flickr_url = "https://api.flickr.com/services/rest/"

        self.flickr_method_echo = "?method=flickr.test.echo&name=value"
        self.flickr_method_getRecent = "?method=flickr.photos.getRecent"

        self.flickr_format_json = "&format=json"

#https://api.flickr.com/services/rest/?method=flickr.test.echo&name=value&api_key=76cceea6d278cbd158a726e6860951e7&format=json
        self.data_file = "json-data"
        self.dict = {}



    def get_echo(self):
        req_str = self.flickr_url + self.flickr_method_echo + self.flickr_api_key + self.flickr_format_json
        print req_str
        req = urllib2.Request(req_str)
        response = urllib2.urlopen(req)
        resPage = response.read()
        print resPage

    def get_recent_photos(self):
        req_str = self.flickr_url + self.flickr_method_getRecent + self.flickr_api_key + self.flickr_format_json

        #print req_str

        req = urllib2.Request(req_str)
        response = urllib2.urlopen(req)
        resPage = response.read()

        with open(self.data_file, "w") as f:
            f.write(resPage)
        f.close()        

class PhotoURL(object):

    def __init__(self, data_file):

        self.data_file = data_file
        self.data_buffer = ""
        self.getData()
        self.header = ""
        self.current_buffer = ""
        self.getHeader()
        self.photoURL = ""
        self.hasNext = True

        #save this in case we need to debug
        with open("debug-tmp", "w") as f:
            f.write(self.current_buffer)

    def getData(self):

        with open(self.data_file, "r") as f:
            self.data_buffer = f.read()

    

    def numPhotos(self):

        m = re.search("total:(.+),", self.data_buffer)
        return m.group(0)

    def getHeader(self):

        matchObj = re.match('jsonFlickrApi(.+):\[(.+)\]\},(.+)', self.data_buffer)
        self.header = matchObj.group(1)
        self.current_buffer = matchObj.group(2)

        #add this so that all entries consistently end with },
        self.current_buffer += ","

        

    def getTotalPhotos(self):

        matchObj = re.match('(.+)total":(.+),', self.header)
        return int(matchObj.group(2))

    def getNextEntry(self):

        if (self.hasNext == False) :
            return False

        matchObj = re.match('\{(.*?)\},(.+)?', self.current_buffer)
        #matchObj = re.match('\{(.*?)\}(,(.+))?', self.current_buffer)
        if matchObj == None:
            print self.current_buffer

        if matchObj.lastindex == 1 :
            self.hasNext = False

        else :    
            self.current_buffer = matchObj.group(2)

        thisEntry = matchObj.group(1)

        #make dictionary
        #print thisEntry
        #title field is problematic since it can contain
        #all sorts of characters

        matchObj = re.match('(.*?)"title":"(.*?)",("ispublic"(.+))', thisEntry)
        if matchObj == None : 
            print thisEntry

        #this pulls out title 
        strTitle = matchObj.group(2)

        #this stitches string without title
        thisEntry = matchObj.group(1) + matchObj.group(3)
        fieldList = re.split(',', thisEntry)
        self.dict = {}
        for i in fieldList:
            (key1, val1) = re.split(":", i)
            key1 = re.sub('\"', '', key1)
            val1 = re.sub('\"', '', val1)
            self.dict[key1] = val1

        #add title back
        self.dict["title"] = strTitle
        return True

        

    def getNextPhotoURL(self):

        newEntry = self.getNextEntry()
        if newEntry == False: 
            return None

        self.photoURL = "https://farm" + self.dict['farm'] + ".staticflickr.com/" + \
            self.dict['server'] + "/" + self.dict['id'] + "_" + \
            self.dict['secret'] + ".jpg"

        return self.photoURL 


class DisplayPhoto(object):

    def __init__(self, photoList):

        self.WHITE = (255,255,255)
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.photoList = photoList
        self.photoListIndex = 0
        self.lastShownIndex = -1
        self.picFileName = "pic.jpg"
        self.saveFile = "pic-save.txt"

        pygame.init()
        size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Photos from Flickr")



    def doDisplayLoop(self):

        done = False
        clock = pygame.time.Clock()

        #photo = pygame.image.load("/Users/anchung/Documents/workspace/python1/test/pic.jpg")

        while not done:

            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop

                #print "done"
                if event.type == pygame.KEYDOWN and event.key== pygame.K_RIGHT:
                    self.photoListIndex += 1
                    if self.photoListIndex >= len(self.photoList) :
                        self.photoListIndex = len(self.photoList) - 1
                    

                if event.type == pygame.KEYDOWN and event.key==pygame.K_LEFT:
                    self.photoListIndex -= 1
                    if self.photoListIndex < 0 :
                        self.photoListIndex = 0

                if event.type==pygame.KEYDOWN and event.key==pygame.K_s:
                    with open(self.saveFile, "a") as f:
                        url = self.photoList[self.photoListIndex] + "\n"
                        f.write(url)

            self.fetchPhoto()
            self.screen.fill(self.WHITE)
            self.screen.blit(self.photo, self.photoSize)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)

        pygame.quit()

    

    def fetchPhoto(self):

        if self.lastShownIndex == self.photoListIndex :
            return

        url = self.photoList[self.photoListIndex]
        self.lastShownIndex = self.photoListIndex

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        resPage = response.read()

        print "displaying: " + url 
        print self.photoListIndex

        with open(self.picFileName, "wb") as f:
            f.write(resPage)

        f.close()

        self.photo = pygame.image.load(self.picFileName)
        self.photoSize = self.photo.get_rect()

#need pairs from: farm, server, id, secret

#constructed URL: https://farm{farm_id}.staticflickr.com/{server}/{id}_{secret}.jpg



def main():

    flickr_api_key = ""
    flickr_secret_key = ""

    flickr = Flickr(flickr_api_key, flickr_secret_key)
    ##flickr.get_echo()

    #comment this line out to reuse old buffer for debugging
    flickr.get_recent_photos()

    photoURL = PhotoURL(flickr.data_file)
    total = photoURL.getTotalPhotos()

    urlList = []
    counter = photoURL.getTotalPhotos()

    for i in range(counter):
        url = photoURL.getNextPhotoURL()
        if url == None:
            break

        urlList.append(url)

#    for url in urlList:

#        print url    

    pyDisp = DisplayPhoto(urlList)
    pyDisp.doDisplayLoop()

if __name__ == "__main__":
    main()

