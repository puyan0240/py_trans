import tkinter
from tkinter import ttk
import googletrans
from googletrans import Translator
import re


#翻訳方向
TRANS_DIR_RIGHT = 0 #左から右へ
TRANS_DIR_LEFT = 1  #右から左へ
TRANS_DIR_TBL_VAL = 0
TRANS_DIR_TBL_TEXT = 1
trans_dir_text_tbl = [
    "---->", #TRANS_DIR_RIGHT
    "<----", #TRANS_DIR_LEFT
]
trans_dir = TRANS_DIR_RIGHT


#言語テーブル
LANG_TBL_NAME=0
LANG_TBL_PARAME=1
lang_tbl = [
    ["Japanese (日本語)", "ja"],
    ["English (英語)", "en"],
    ["German (ドイツ語)", "de"],
    ["French (フランス語)", "fr"],
    ["Spanish (スペイン語)", "es"],
    ["Portuguese (ポルトガル語)", "pt"],
    ["Russian (ロシア語)", "ru"],
    ["Korean (韓国語)", "ko"],
    ["chinese (中国語)", "zh-cn"]
]
split_tbl = [".", "。", "?", "？"]



############################################################
#翻訳方向ボタンが押されました
############################################################
def btn_trans_dir_clicked():
    global trans_dir,trans_dir_text_tbl

    if trans_dir == TRANS_DIR_RIGHT:
        trans_dir = TRANS_DIR_LEFT      #翻訳は右から左へ
        #ラベル表示を変更
        label_left['text'] = "翻訳先"        
        label_right['text'] = "翻訳元"
        #Text
        text_src = text_right
        text_dst = text_left
    else:
        trans_dir = TRANS_DIR_RIGHT     #翻訳は左から右へ
        #ラベル表示を変更
        label_left['text'] = "翻訳元"
        label_right['text'] = "翻訳先"
        #Text
        text_src = text_left
        text_dst = text_right

    #ボタンの表示を変更
    btn_trans_dir['text'] = trans_dir_text_tbl[trans_dir]

    #Text入力表示変更
    text_src.config(state=tkinter.NORMAL,bg='white',bd=1)
    text_dst.config(state=tkinter.DISABLED,bg='gray97',bd=0)
    return


############################################################
#翻訳実行ボタンが押されました
############################################################
def btn_trans_clicked():

    #翻訳方向
    if trans_dir == TRANS_DIR_RIGHT:   #翻訳は左から右
        #Text
        text_src = text_left
        text_dst = text_right
        #Combobox
        cb_src   = cb_left
        cb_dst   = cb_right
    else:
        #Text
        text_src = text_right
        text_dst = text_left
        #Combobox
        cb_src   = cb_right
        cb_dst   = cb_left


    #翻訳先の文字を消す
    text_dst.config(state=tkinter.NORMAL)   #入力許可
    text_dst.delete('1.0', tkinter.END)
    text_dst.config(state=tkinter.DISABLED) #入力規制


    #-------------------------------------------------------
    #翻訳言語取得
    #-------------------------------------------------------
    lang_src = lang_dst = ""
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
    #翻訳元（入力）の文字取得
    #-------------------------------------------------------
    #テキスト取得
    str_src = text_src.get('1.0', tkinter.END)

    #改行を全て削除
    str_src = str_src.replace("\n", "")
    if len(str_src) == 0:
        return  #入力文字数なし

    #分割文字を分割文字+改行に置換
    for str_split in split_tbl:
        str_src = str_src.replace(str_split, str_split+"\n")

    #文章を改行で分割してリスト化する
    str_src_list = str_src.split("\n")


    #-------------------------------------------------------
    #翻訳実行
    #-------------------------------------------------------
    trans = Translator()

    for str_src_line in str_src_list:
        if len(str_src_line) != 0:  #１文字以上ある場合
            try:
                if lang_src == "":  #翻訳元=自動
                    result = trans.translate(str_src_line, dest=lang_dst)
                else:   #翻訳元=指定あり
                    result = trans.translate(str_src_line, src=lang_src, dest=lang_dst)

                #翻訳先に出力
                text_dst.config(state=tkinter.NORMAL)   #入力許可
                text_dst.insert(tkinter.END, result.text+"\n")
                text_dst.config(state=tkinter.DISABLED) #入力規制

            except Exception as e:
                print(e)
        else:
            pass
    return



root = tkinter.Tk()
root.title("Trans")
#root.geometry("1000x600")

frame_top = tkinter.Frame(root)
frame_top.pack()

frame_trans = tkinter.Frame(root)
frame_trans.pack()

#-----------------------------------------------------------
#左側の言語メニュー
#-----------------------------------------------------------
#ラベル
label_left = tkinter.Label(frame_trans, text="翻訳元")
label_left.grid(row=0, column=0)

#Combobox
cb_menu = [] #メニューリスト
for val in lang_tbl:
    cb_menu.append(val[LANG_TBL_NAME])
v_left = tkinter.StringVar()
cb_left = ttk.Combobox(frame_trans, textvariable=v_left, values=cb_menu, state="readonly", width=20)
cb_left.current(0)
cb_left.grid(row=1, column=0)

#Text
text_left = tkinter.Text(frame_trans,  relief=tkinter.SOLID, width=60,padx=10)
text_left.config(state=tkinter.NORMAL)   #入力許可
text_left.config(bg="white", bd=1)    #入力許可時のText表示
text_left.grid(row=2, column=0, padx=10, pady=10)


#-----------------------------------------------------------
#ボタン
#-----------------------------------------------------------
#ラベル
label_dir = tkinter.Label(frame_trans, text="翻訳方向")
label_dir.grid(row=0, column=1)

#翻訳方向ボタン
trans_dir_text = trans_dir_text_tbl[trans_dir]
btn_trans_dir = tkinter.Button(frame_trans, text=trans_dir_text, width=15, command=btn_trans_dir_clicked)
btn_trans_dir.grid(row=1, column=1)

#翻訳実行ボタン
btn_trans = tkinter.Button(frame_trans, text="翻訳", width=15, command=btn_trans_clicked)
btn_trans.grid(row=2, column=1)


#-----------------------------------------------------------
#右側の言語メニュー
#-----------------------------------------------------------
#ラベル
label_right = tkinter.Label(frame_trans, text="翻訳先")
label_right.grid(row=0, column=2)


#Combobox
v_right = tkinter.StringVar()
cb_right = ttk.Combobox(frame_trans, textvariable=v_right, values=cb_menu, state="readonly", width=20)
cb_right.current(1)
cb_right.grid(row=1, column=2)

#Text
text_right = tkinter.Text(frame_trans, relief=tkinter.SOLID, width=60, padx=10)
text_right.config(state=tkinter.DISABLED)   #入力規制
text_right.config(bg="gray97", bd=0)    #入力規制時のText表示
text_right.grid(row=2, column=2, padx=10, pady=10)


#root.resizable(False, False)    #ウィンドウサイズ固定
root.mainloop()
