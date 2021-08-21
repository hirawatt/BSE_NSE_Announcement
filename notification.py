import time
import notify2
import os

# path to notification window icon
ICON_PATH = os.getcwd() + "/icon.jpeg"

# fetch news items
#newsitems = topStories()
newsitems = {'description': 'Months after it was first reported, the feud between Dwayne Johnson and Vin Diesel continues to rage on, with a new report saying that the two ar being kept apart during the promotions of The Fate of the Furious.',
            'link': 'http://www.hindustantimes.com/hollywood/vin-diesel-dwayne-johnson-feud-rageson-they-re-being-kept-apart-for-fast-8-tour/story-Bwl2Nx8gja9T15aMvcrcvL.html',
            'media': 'http://www.hindustantimes.com/rf/image_size_630x354/HT/p2/2017/04/01/Pictures/_fbcbdc10-1697-11e7-9d7a-cd3db232b835.jpg',
            'pubDate': b'Sat, 01 Apr 2017 05:22:51 GMT ',
            'title': "Vin Diesel, Dwayne Johnson feud rages on; they're being deliberately kept apart"}

# initialise the d-bus connection
notify2.init("News Notifier")

# create Notification object
n = notify2.Notification(None, icon = ICON_PATH)

# set urgency level
#n.set_urgency(notify2.URGENCY_NORMAL)
n.set_urgency(notify2.URGENCY_CRITICAL)

# set timeout for a notification
n.set_timeout(10000)

for newsitem in newsitems:

    # update notification data for Notification object
    n.update(newsitem[2], newsitem[3])

    # show notification on screen
    n.show()

    # short delay between notifications
    #time.sleep(15)
