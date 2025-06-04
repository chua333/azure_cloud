from dotenv import load_dotenv
from datetime import datetime
from playsound import playsound
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk


def main():
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
        print("ready to use speech service in: ", speech_config.region)

        # Get spoken input
        # command = TranscribeCommand()
        command = "what time is it?"
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''

    # Configure speech recognition
    audio_config = speech_sdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print("Listening for command...")

    # # configure speech recognition using playback audio
    # current_dir = os.getcwd()
    # audioFile = current_dir + '\\time.wav'
    # playsound(audioFile)
    # audio_config = speech_sdk.AudioConfig(filename=audioFile)
    # speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print("Recognized command: ", command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultREason.Canceled:
            cancellation = speech.cancellation_details
            print("Speech Recognition canceled: ", cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command


def TellTime():
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)


    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

    # # Synthesize spoken output
    # speak = speech_synthesizer.speak_text_async(response_text).get()
    # if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
    #     print(speak.reason)

    # Synthesize spoken output
    responseSsml = " \
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
            <voice name='en-GB-LibbyNeural'> \
                {} \
                <break strength='weak'/> \
                Time to end this lab! \
            </voice> \
        </speak>".format(response_text)
    speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()
