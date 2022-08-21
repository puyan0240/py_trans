import tkinter
from tkinter import ttk


#言語テーブル
LANG_TBL_NAME=0
LANG_TBL_PARAME=1
lang_tbl = [
    ["日本語", "ja"],
    ["English(英語)", "en"],
    ["German(ドイツ語)", "de"],
    ["French(フランス語)", "fr"],
    ["Spanish(スペイン語)", "es"],
    ["Portuguese(ポルトガル語)", "pt"],
    ["Russian(ロシア語)", "ru"],
    ["Korean(韓国語)", "ko"],
    ["chinese(中国語)", "zh-cn"]
]


root = tkinter.Tk()
root.title("Trans")
root.geometry("1000x600")

frame_top = tkinter.Frame(root)
frame_top.propagate(0)
frame_top.pack(side=tkinter.TOP)

btn_trans = tkinter.Button(frame_top, text="翻訳", width=15)
btn_trans.grid(row=0, column=0, sticky=tkinter.W)

#btn_clr = tkinter.Button(frame_top, text="取消", width=15)
#btn_clr.grid(row=0, column=1, sticky=tkinter.E)

frame_trans = tkinter.Frame(root)
frame_trans.propagate(0)
frame_trans.pack()

combobox_menu = [] #メニューリスト
for val in lang_tbl:
    combobox_menu.append(val[LANG_TBL_NAME])
v = tkinter.StringVar()



#root.resizable(False, False)    #ウィンドウサイズ固定
root.mainloop()
