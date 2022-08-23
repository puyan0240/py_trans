import tkinter
from tkinter import ttk
import googletrans
from googletrans import Translator


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


############################################################
#翻訳ボタンが押されました
############################################################
def btn_trans_clicked():

    #-------------------------------------------------------
    #翻訳元（入力）の文字取得
    #-------------------------------------------------------
    input_text = text_src.get('1.0', 'end')
    #print(input_text)

    lang_src = lang_dst = ""
    #-------------------------------------------------------
    #翻訳言語取得
    #-------------------------------------------------------
    #翻訳元
    if cb_src.get() != "自動":
        for lang_tbl_line in lang_tbl:
            if lang_tbl_line[LANG_TBL_NAME] == cb_src.get():
                lang_src = lang_tbl_line[LANG_TBL_PARAME]
                break
    #翻訳先
    for lang_tbl_line in lang_tbl:
        if lang_tbl_line[LANG_TBL_NAME] == cb_dst.get():
            lang_dst = lang_tbl_line[LANG_TBL_PARAME]
            break

    #print(lang_src)
    #print(lang_dst)


    #-------------------------------------------------------
    #翻訳実行
    #-------------------------------------------------------
    trans = Translator()
    try:
        if lang_src == "":  #翻訳元=自動
            result = trans.translate(input_text, dest=lang_dst)
        else:   #翻訳元=指定あり
            result = trans.translate(input_text, src=lang_src, dest=lang_dst)
        print(result.text)
    except Exception as e:
        print(e)
    return




root = tkinter.Tk()
root.title("Trans")
root.geometry("1000x600")

frame_top = tkinter.Frame(root)
frame_top.pack()

frame_trans = tkinter.Frame(root)
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
#翻訳ボタン
#-----------------------------------------------------------
btn_trans = tkinter.Button(frame_trans, text="翻訳", width=15, command=btn_trans_clicked)
btn_trans.grid(row=0, column=1, rowspan=3)


#-----------------------------------------------------------
#翻訳先の言語メニュー
#-----------------------------------------------------------
#ラベル
label_dst = tkinter.Label(frame_trans, text="翻訳先")
label_dst.grid(row=0, column=2)


#Combobox
cb_dst_menu = [] #メニューリスト
for val in lang_tbl:
    cb_dst_menu.append(val[LANG_TBL_NAME])
v_dst = tkinter.StringVar()
cb_dst = ttk.Combobox(frame_trans, textvariable=v_dst, values=cb_dst_menu, state="readonly", width=20)
cb_dst.current(0)
cb_dst.grid(row=1, column=2)

#Text
text_dst = tkinter.Text(frame_trans, width=40)
text_dst.grid(row=2, column=2)



#root.resizable(False, False)    #ウィンドウサイズ固定
root.mainloop()
