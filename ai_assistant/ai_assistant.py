import openai
import pyttsx3
import speech_recognition as sr

# Set your OpenAI key
openai.api_key = ""

# Initialize text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response["choices"][0]["text"]
    except Exception as e:
        print(f"An error occurred while generating response from OpenAI: {str(e)}")

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # Wait for the user to say "genius"
        print("Waiting for 'genius'...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "genius":
                    print("You said 'genius', recording your question...")
                    
                    # Record audio
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        # Generate response using GPT-3
                        response = generate_response(text)
                        if response:
                            print(f"GPT-3 says: {response}")

                            # Read response using text-to-speech
                            speak_text(response)
                        
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand your speech")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
