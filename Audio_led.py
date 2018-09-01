#this class communicates with the audio and gives us back volume
#and pitch so we could set the color on the led strip

#import libs
import random



def get_pitch():
    return (random.randint(0,256),random.randint(0,256),random.randint(0,256))

def get_volume():
    return 255