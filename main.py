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
    ">>> 翻訳方向 >>>", #TRANS_DIR_RIGHT
    "<<< 翻訳方向 <<<", #TRANS_DIR_LEFT
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


############################################################
#翻訳方向ボタンが押されました
############################################################
def btn_trans_dir_clicked():
    global trans_dir

    if trans_dir == TRANS_DIR_RIGHT:
        trans_dir = TRANS_DIR_LEFT      #翻訳は右から左へ
        #ラベル表示を変更
        label_left['text'] = "翻訳先"        
        label_right['text'] = "翻訳元"

    else:
        trans_dir = TRANS_DIR_RIGHT     #翻訳は左から右へ
        #ラベル表示を変更
        label_left['text'] = "翻訳元"
        label_right['text'] = "翻訳先"

    #ボタンの表示を変更
    trans_dir_text = trans_dir_text_tbl[trans_dir]
    btn_trans_dir['text'] = trans_dir_text
    return


############################################################
#翻訳実行ボタンが押されました
############################################################
def btn_trans_clicked():

    if trans_dir == TRANS_DIR_RIGHT:   #翻訳は左から右
        text_src = text_left
        text_dst = text_right
        cb_src   = cb_left
        cb_dst   = cb_right
    else:
        text_src = text_right
        text_dst = text_left
        cb_src   = cb_left
        cb_dst   = cb_right


    #翻訳先の文字を消す
    text_dst.delete('1.0', tkinter.END)

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
    #翻訳元（入力）の文字取得
    #-------------------------------------------------------
    str_src = text_src.get('1.0', tkinter.END+'-1c')
    if len(str_src) == 0:
        return  #入力文字数なし
    str_src_list = re.split(r'[.。?？]', str_src, 0) #.か。で分離
    print(str_src)
    print(str_src_list)


    #-------------------------------------------------------
    #翻訳実行
    #-------------------------------------------------------
    trans = Translator()

    for str_src_line in str_src_list:
        try:
            if lang_src == "":  #翻訳元=自動
                result = trans.translate(str_src_line, dest=lang_dst)
            else:   #翻訳元=指定あり
                result = trans.translate(str_src_line, src=lang_src, dest=lang_dst)
            #print(result.text)
            #翻訳先に出力
            text_dst.insert(tkinter.END, result.text)
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
text_left = tkinter.Text(frame_trans, width=40)
text_left.grid(row=2, column=0)


#-----------------------------------------------------------
#ボタン
#-----------------------------------------------------------
#翻訳方向ボタン
trans_dir_text = trans_dir_text_tbl[trans_dir]
btn_trans_dir = tkinter.Button(frame_trans, text=trans_dir_text, width=15, command=btn_trans_dir_clicked)
btn_trans_dir.grid(row=0, column=1, rowspan=2)

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
text_right = tkinter.Text(frame_trans, width=40)
text_right.grid(row=2, column=2)


#root.resizable(False, False)    #ウィンドウサイズ固定
root.mainloop()
