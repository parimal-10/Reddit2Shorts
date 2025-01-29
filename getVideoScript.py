import getVoiceOver
from moviepy import AudioFileClip # type: ignore

MAX_WORDS_PER_COMMENT = 50
MIN_COMMENTS_FOR_FINISH = 1
MIN_DURATION = 15
MAX_DURATION = 58

class VideoScript:
    title = ""
    text = ""
    id = ""
    url = ""
    titleSCFile = ""
    textSCFile = ""
    totalDuration = 0
    frames = []

    def __init__(self, title, text, id, url):
        self.id = f"{id}"
        self.title = title
        self.url = url
        self.text = text
        self.titleAudioClip = self.__create_voice_over(f"{id}-title", title)
        if(not(self.text == "" or self.text == None)):
            self.textAudioClip = self.__create_voice_over(f'{id}-text', text)

    def can_be_finished(self) -> bool:
        return ((len(self.frames) >= MIN_COMMENTS_FOR_FINISH) and (self.totalDuration > MIN_DURATION))

    def addScene(self, id, text):
        wordCount = len(text.split())
        if(wordCount > MAX_WORDS_PER_COMMENT):
            return True
        frame = ScreenshotScene(id, text)
        frame.audioClip = self.__create_voice_over(id, text)
        if(frame.audioClip == None):
            return True
        self.frames.append(frame)

    def get_script_id(self):
        return self.id

    def get_duration(self):
        return self.totalDuration

    def __create_voice_over(self, id, text):
        filepath = getVoiceOver.create_voice_over(id, text)
        audioClip = AudioFileClip(filepath)
        if(self.totalDuration + audioClip.duration > MAX_DURATION):
            return None
        self.totalDuration += audioClip.duration
        return audioClip


class ScreenshotScene:
    text = ""
    screenshotFile = ""
    id = ""

    def __init__(self, id, text):
        self.commentId = id
        self.text = text
