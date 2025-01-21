import pyttsx3

def speak_text(text, pitch=150, rate=150):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set properties for voice, pitch, and rate
    voices = engine.getProperty('voices')
    
    # Try to set the female voice (usually index 1 or 0, depending on system)
    engine.setProperty('voice', voices[1].id)  # Female voice (on most systems)
    
    # Set pitch and rate
    engine.setProperty('pitch', pitch)  # Adjust pitch (default is usually 50)
    engine.setProperty('rate', rate)    # Adjust rate (default is usually 200)
    
    # Speak the passed text
    engine.say(text)
    engine.runAndWait()

# Example usage
if __name__ == "__main__":
    text_to_speak = "Hello, I hope you are having a wonderful day!"
    speak_text(text_to_speak, pitch=120, rate=130)
