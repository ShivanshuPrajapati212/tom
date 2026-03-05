from AppKit import NSSpeechSynthesizer
from Foundation import NSRunLoop, NSDate

def speakText(text):
    speech = NSSpeechSynthesizer.alloc().init()

    speech.startSpeakingString_(text)

    while speech.isSpeaking():
        NSRunLoop.currentRunLoop().runUntilDate_(
            NSDate.dateWithTimeIntervalSinceNow_(0.1)
    )


if __name__ == "__main__":
    speakText("Hello World")
