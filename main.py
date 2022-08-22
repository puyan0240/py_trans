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
#frame_top.propagate(0)
frame_top.pack()

btn_trans = tkinter.Button(frame_top, text="翻訳", width=15)
btn_trans.grid(row=0, column=0, sticky=tkinter.W)

#btn_clr = tkinter.Button(frame_top, text="取消", width=15)
#btn_clr.grid(row=0, column=1, sticky=tkinter.E)

frame_trans = tkinter.Frame(root)
#frame_trans.propagate(0)
frame_trans.pack()

#-----------------------------------------------------------
#翻訳元の言語メニュー
#-----------------------------------------------------------
#ラベル
label_src = tkinter.Label(frame_trans, text="翻訳元")
label_src.grid(row=0, column=0)

#Combobox
cb_src_menu = [] #メニューリスト
cb_src_menu.append("自動")
for val in lang_tbl:
    cb_src_menu.append(val[LANG_TBL_NAME])
v_src = tkinter.StringVar()
cb_src = ttk.Combobox(frame_trans, textvariable=v_src, values=cb_src_menu, state="readonly", width=20)
cb_src.current(0)
cb_src.grid(row=1, column=0)

#Text
text_src = tkinter.Text(frame_trans, width=40)
text_src.grid(row=2, column=0)




#-----------------------------------------------------------
#翻訳先の言語メニュー
#-----------------------------------------------------------
#ラベル
label_dst = tkinter.Label(frame_trans, text="翻訳先")
label_dst.grid(row=0, column=1)


#Combobox
cb_dst_menu = [] #メニューリスト
for val in lang_tbl:
    cb_dst_menu.append(val[LANG_TBL_NAME])
v_dst = tkinter.StringVar()
cb_dst = ttk.Combobox(frame_trans, textvariable=v_dst, values=cb_dst_menu, state="readonly", width=20)
cb_dst.current(0)
cb_dst.grid(row=1, column=1)

#Text
text_dst = tkinter.Text(frame_trans, width=40)
text_dst.grid(row=2, column=1)



#root.resizable(False, False)    #ウィンドウサイズ固定
root.mainloop()
