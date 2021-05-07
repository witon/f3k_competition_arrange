import sys
import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat
import time
import getopt
from azure.cognitiveservices.speech.audio import AudioOutputConfig, AudioStreamFormat
from common import get_competitors_from_input

speech_key, service_region = "78eb48c98a864027a94b44e25e0ba9d7", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm)
input_file_path = ""
output_dir = ""

def print_help():
    print(sys.argv[0] + ' -i <inputfile> -o <outputdir>')

def parse_argv(argv):
    global input_file_path
    global output_dir
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "odir="])
    except getopt.GetoptError:
        print_help()
        return False
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            return False
        elif opt in ("-i", "--ifile"):
            input_file_path = arg
        elif opt in ("-o", "--odir"):
            output_dir = arg
    if (input_file_path == '' and sys.stdin.isatty()) or output_dir == '':
        print_help()
        return False
    return True


def speech(text, filename):
    format = AudioStreamFormat(samples_per_second=32000)
    audio_config = AudioOutputConfig(filename=filename)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    ssml = '<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="zh-cn"><voice name="zh-cn-YunyangNeural"><prosody rate="-10%" pitch="0%">'
    ssml = ssml + text + '</prosody></voice></speak>'
    result = speech_synthesizer.speak_ssml(ssml)
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")
        return False
    return True

def try_speech(text, filename, dir):
    i = 0
    while i < 10:
        i = i + 1
        if speech(text, dir + "\\" + filename) :
            break
        time.sleep(i)

def speech_competitors(competitors):
    global output_dir
    for competitor in competitors:
        try_speech(competitor, competitor + ".wav", output_dir)

def main(argv):

    global input_file_path
    if not parse_argv(argv):
        return
    competitors = get_competitors_from_input(input_file_path)

    global output_dir
    if not os.path.exists(output_dir):
        print("output dir " + output_dir + " isn't exist.")
        exit(0)
    speech_competitors(competitors)
 

if __name__ == '__main__':
    main(sys.argv[1:])