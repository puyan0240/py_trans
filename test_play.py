from gtts import gTTS
from playsound import playsound
import os


FILE_NAME="test.mp3"

myText = "こんばんは"
myLang = 'ja'

#音声合成してファイル化
try:
    output = gTTS(myText, lang=myLang, slow=False)
    output.save(FILE_NAME)
except Exception as e:
    print("save err:"+str(e))

#再生
try:
    playsound(FILE_NAME)
except Exception as e:
    print("play err:"+str(e))

#ファイルを削除
try:
    os.remove(FILE_NAME)
except Exception as e:
    print("remove err:"+str(e))
