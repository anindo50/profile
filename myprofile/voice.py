# from gtts import gTTS
# import os

# text = "আপনি কেমন আছেন? আ! আ! আ! আ! আ! "  # Example text in Bangla (Bengali)
# language = 'bn'  # Language code for Bangla

# tts = gTTS(text=text, lang=language)
# tts.save("output.mp3")
# os.system("start output.mp3")  # For Windows, adjust for other OS


# import pyttsx3



# with open('C:/Users/User/Desktop/test_ai/dataexp/book2.txt', 'r', encoding='utf-8', errors='ignore') as file:
#     content = file.read()
    

# # Print the content


# # Initialize the TTS engine
# engine = pyttsx3.init()

# # Set the text you want to convert to speech
# text = "Hello, this is a text-to-speech conversion."
# engine.say(text)

# # Save the audio to a file
# engine.save_to_file(content, 'outputss.mp3')

# # Run the engine to process the speech request
# engine.runAndWait()



# import pyttsx3

# def customize_tts(text):
#     # Initialize the TTS engine
#     engine = pyttsx3.init()

#     # Set default speech properties
#     engine.setProperty('rate', 150)  # Speed of speech
#     engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

#     # Split the text into words
#     words = text.split()

#     for word in words:
#         # Determine pitch based on word length
#         if len(word) <= 3:
#             pitch = '0st'   # Normal pitch for short words
#         elif len(word) <= 6:
#             pitch = '-2st'  # Slightly lower pitch for medium-length words
#         else:
#             pitch = '-4st'  # Lower pitch for long words

#         # Use SSML to set the pitch dynamically
#         ssml_text = f"<speak><prosody pitch='{pitch}'>{word}</prosody></speak>"

#         # Speak the word
#         engine.say(ssml_text)

#     # Wait until all speech is finished
#     engine.runAndWait()

# # Example usage
# text_input = "This is a simple demonstration of Text to Speech customization."
# customize_tts(text_input)



# import pyttsx3

# def customize_tts(text,output_file):
#     # Initialize the TTS engine
#     engine = pyttsx3.init()

#     # Set default volume
#     engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

#     # Determine speech rate based on total text length
#     if len(text.split()) <= 10:
#         rate = 290  # Faster rate for shorter texts
#     elif len(text.split()) <= 20:
#         rate = 190  # Normal-fast rate for medium-length texts
#     else:
#         rate = 89  # Slower rate for longer texts

#     # Set the speech rate
#     engine.setProperty('rate', rate)

#     # Speak the entire text at once
#     # engine.say(text)
#     engine.save_to_file(text, output_file)

#     # Wait until all speech is finished
#     engine.runAndWait()


import pyttsx3

def list_available_voices():
    """Lists all available voices with their index and details."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}:")
        print(f" - ID: {voice.id}")
        print(f" - Name: {voice.name}")
        print(f" - Language: {voice.languages}\n")
    engine.stop()

def customize_tts(text, output_file, voice_index=1):
    """
    Converts text to speech and saves it to an audio file.
    
    Parameters:
    - text (str): The text to be spoken.
    - output_file (str): The output file where the audio will be saved.
    - voice_index (int): Index of the desired voice to use (default is 0).
    """
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Get the list of voices and select one by index
    voices = engine.getProperty('voices')
    if voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    else:
        print(f"Voice index {voice_index} out of range, using default voice.")
    
    # Set default volume
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    # Determine speech rate based on total text length
    if len(text.split()) <= 3:
        rate = 400

    if len(text.split()) <= 10:
        rate = 300  # Faster rate for shorter texts
    elif len(text.split()) <= 15:
        rate = 250 
    elif len(text.split()) <= 20:
        rate = 200  # Normal-fast rate for medium-length texts
    else:
        rate = 100  # Slower rate for longer texts

    # Set the speech rate
    engine.setProperty('rate', rate)

    # Save the speech to the output file
    engine.save_to_file(text, output_file)

    # Wait until all speech is finished
    engine.runAndWait()

# Example usage
# text_input = "This is a simple demonstration of Text to Speech customization that should sound faster and more fluid."
# output_file = "output_speech.wav"
# customize_tts(text_input,output_file)