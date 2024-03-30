from multiprocessing import Process
import pyttsx3 

# the TTS engine is not thread-safe, so can only run it in a separate process.
def launch_speak(txt, path):
    p=Process(target=speak_to_file, args=(txt, path))
    p.start()
    p.join()

def speak_to_file(txt, path):
    eng=pyttsx3.init()
    eng.setProperty("rate", 140)
    eng.save_to_file(txt, path)
    eng.runAndWait()
