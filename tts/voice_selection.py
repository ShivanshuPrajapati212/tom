from AppKit import NSSpeechSynthesizer
from Foundation import NSRunLoop, NSDate

speech = NSSpeechSynthesizer.alloc().init()

speech.startSpeakingString_("")

# Keep the run loop alive while speaking
while speech.isSpeaking():
    NSRunLoop.currentRunLoop().runUntilDate_(
        NSDate.dateWithTimeIntervalSinceNow_(0.1)
)
