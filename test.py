import googletrans
from googletrans import Translator


trans = Translator()

print(googletrans.LANGUAGES)    #言語リスト

try:
    bf = "今日は暑いですね"
    af = trans.translate(bf, "en")
    print(bf+" -> "+af.text)

    bf = "it is hot today"
    af = trans.translate(bf, "ja")
    print(bf+" -> "+af.text)

except Exception as e:
    print(e)