from gtts import gTTS
from playsound import playsound
import os


myText = "こんばんは"
myLang = 'ja'

#音声合成してファイル化
try:
    output = gTTS(myText, lang=myLang, slow=False)
    output.save("test.mp3")
except Exception as e:
    print("save err:"+str(e))

#再生
try:
    playsound("test.mp3")
except Exception as e:
    print("play err:"+str(e))

#ファイルを削除
try:
    os.remove("test.mp3")
except Exception as e:
    print("remove err:"+str(e))
