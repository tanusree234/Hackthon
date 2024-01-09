import speech_recognition as sr

# Create a recognizer instance
r = sr.Recognizer()

# Braille conversion dictionary
braille_dict = {
    'a': '100000', 'b': '110000', 'c': '100100', 'd': '100110', 'e': '100010',
    'f': '110100', 'g': '110110', 'h': '110010', 'i': '010100', 'j': '010110',
    'k': '101000', 'l': '111000', 'm': '101100', 'n': '101110', 'o': '101010',
    'p': '111100', 'q': '111110', 'r': '111010', 's': '011100', 't': '011110',
    'u': '101001', 'v': '111001', 'w': '010111', 'x': '101101', 'y': '101111',
    'z': '101011', '#': '001111', '1': '100000', '2': '110000', '3': '100100',
    '4': '100110', '5': '100010', '6': '110100', '7': '110110', '8': '110010',
    '9': '010100', '0': '010110', ' ': '000000'
}


def text_to_braille(message):
    # Convert the text to lowercase
    message = message.lower()

    # Convert each character to Braille
    braille = [braille_dict.get(char, '000000') for char in message]

    # Join the Braille characters into a string
    return ' '.join(braille)


# Example usage
# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Listening...")
    # Read the audio data from the default microphone
    audio_data = r.record(source, duration=10)
    print("Recognizing...")
    # Convert speech to text
    text = r.recognize_google(audio_data)

    print(text)
print(text_to_braille(text))
