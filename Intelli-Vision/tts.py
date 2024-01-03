import gtts
# from playsound import playsound

# make a request to google to get synthesis
t1 = gtts.gTTS(
    """The image depicts a man wearing headphones and glasses, sitting down while drinking from a bottle. He appears to be enjoying his beverage, possibly listening to music or watching a show. 

The scene is set in a room with a dining table in the background, and a couch is situated nearby. Another person can be seen in the room, but their presence is not the main focus of the image. The dining table occupies most of the background, while the couch is situated towards the left side of the room."""
)
# save the audio file
t1.save("audio/welcome.mp3")