import tkinter
from tkinter import ttk,messagebox
import googletrans
from googletrans import Translator  #google翻訳
import re
from gtts import gTTS   #文字->音声ファイル化
from playsound import playsound #音声ファイルを再生
import os
import threading    #スレッド


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
    ["Italian (イタリア語)", "it"],
    ["Spanish (スペイン語)", "es"],
    ["Portuguese (ポルトガル語)", "pt"],
    ["Russian (ロシア語)", "ru"],
    ["Korean (韓国語)", "ko"],
    ["chinese (中国語)", "zh-cn"],
    ["Vietnamese (ベトナム語)", "vi"]
]
lang_auto_puls_tbl = [
    ["Auto", ""]
]
lang_auto_puls_tbl += lang_tbl
split_tbl = [".", "。", "?", "？"]

TMP_PLAY_FILENAME = "tmp_play.mp3"


############################################################
#一括ボタン押下禁止
############################################################
def btn_all_inhibit(mode):
    if mode == True:    #押下禁止
        btn_trans_dir.config(state=tkinter.DISABLED)
        btn_trans_dir.update()

        btn_trans.config(state=tkinter.DISABLED)
        btn_trans.update()

        btn_play.config(state=tkinter.DISABLED)
        btn_play.update()

        btn_reset.config(state=tkinter.DISABLED)
        btn_reset.update()

        cb_left.config(state=tkinter.DISABLED)
        cb_left.update()

        cb_right.config(state=tkinter.DISABLED)
        cb_left.update()

    else: #解除
        btn_trans_dir.config(state=tkinter.NORMAL)
        btn_trans_dir.update()

        btn_trans.config(state=tkinter.NORMAL)
        btn_trans.update()

        btn_play.config(state=tkinter.NORMAL)
        btn_play.update()

        btn_reset.config(state=tkinter.NORMAL)
        btn_reset.update()

        cb_left.config(state=tkinter.NORMAL)
        cb_left.update()

        cb_right.config(state=tkinter.NORMAL)
        cb_left.update()



############################################################
#翻訳方向ボタンが押されました
############################################################
def btn_trans_dir_clicked():
    global trans_dir,trans_dir_text_tbl

    if trans_dir == TRANS_DIR_RIGHT:
        trans_dir = TRANS_DIR_LEFT      #翻訳は右から左へ
        #Label
        label_src = label_right
        label_dst = label_left
        #Text
        text_src = text_right
        text_dst = text_left
        #Combobox
        cb_dst = cb_left
    else:
        trans_dir = TRANS_DIR_RIGHT     #翻訳は左から右へ
        #Label
        label_src = label_left
        label_dst = label_right
        #Text
        text_src = text_left
        text_dst = text_right
        #Combobox
        cb_dst = cb_right

    #Label表示変更
    label_src['text'] = "翻訳元"
    label_dst['text'] = "翻訳先"

    #Text入力規制表示変更
    text_src.config(state=tkinter.NORMAL,bg='white',bd=1)
    text_dst.config(state=tkinter.DISABLED,bg='gray97',bd=0)

    #ボタンの表示を変更
    btn_trans_dir['text'] = trans_dir_text_tbl[trans_dir]

    #Comboxメニュー変更
    #翻訳方向の切り替えにより翻訳先がAutoとなる場合は通常メニューに切り替える
    if cb_dst.get() == "Auto":
        cb_menu = [] #メニューリスト
        for val in lang_tbl:
            cb_menu.append(val[LANG_TBL_NAME])
        cb_dst.config(values=cb_menu)
        cb_dst.current(0)
        
    return


############################################################
#翻訳実行ボタンが押されました
############################################################
def btn_trans_clicked():

    #一括ボタン押下禁止(2重押下回避のため)
    btn_all_inhibit(True)

    #翻訳方向
    if trans_dir == TRANS_DIR_RIGHT:   #翻訳は左から右
        #Label
        label_src = label_left
        #Text
        text_src = text_left
        text_dst = text_right
        #Combobox
        cb_src   = cb_left
        cb_dst   = cb_right
    else:
        #Label
        label_src = label_right
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
    if cb_src.get() != "Auto":
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
        #一括ボタン押下禁止解除
        btn_all_inhibit(False)
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

    lang_auto_src = ""
    for str_src_line in str_src_list:
        if len(str_src_line) != 0:  #１文字以上ある場合
            try:
                if lang_src == "":  #翻訳元=auto
                    result = trans.translate(str_src_line, dest=lang_dst)
                else:   #翻訳元=指定あり
                    result = trans.translate(str_src_line, src=lang_src, dest=lang_dst)

                #翻訳先に出力
                text_dst.config(state=tkinter.NORMAL)   #入力許可
                text_dst.insert(tkinter.END, result.text+"\n")  #改行付きで
                text_dst.config(state=tkinter.DISABLED) #入力規制
                text_dst.update()
                lang_auto_src = result.src  #翻訳元の言語

            except Exception as e:
                print(e)
        else:
            pass

    #翻訳元の言語がautoの場合は解析結果の言語をLabelに表示する
    label_src['text'] = "翻訳元"
    if lang_src == "":  #翻訳元=auto
        for key in googletrans.LANGCODES:
            if googletrans.LANGCODES[key] == lang_auto_src:
                text = " ("+ key +")"
                label_src['text'] += text
                break
    
    #一括ボタン押下禁止解除
    btn_all_inhibit(False)

    return


############################################################
#再生ボタンが押されました
############################################################
def btn_play_clicked():
    global trans_dir

    #先に翻訳する
    btn_trans_clicked()

    #一括ボタン押下禁止(2重押下回避のため)
    btn_all_inhibit(True)

    #再生は専用のタスクで実施する
    task_id = threading.Thread(target=play_task)
    task_id.start()
    #task_id.join()
    return


############################################################
#再生タスク
############################################################
def play_task():
    global trans_dir
    #print("play_task start")


    #翻訳方向
    if trans_dir == TRANS_DIR_RIGHT:   #翻訳は左から右
        #Text
        text_dst = text_right
        #Combobox
        cb_dst = cb_right
    else:
        #Text
        text_dst = text_left
        #Combobox
        cb_dst = cb_left

    #翻訳先の言語
    lang_dst = ""
    tmp = cb_dst.get()
    for val in lang_tbl:
        if val[LANG_TBL_NAME] == cb_dst.get():
            lang_dst = val[LANG_TBL_PARAME]
            break
    #print(lang_dst)

    #翻訳先の言語を改行毎にリスト化する
    str_dst = text_dst.get('1.0', tkinter.END)
    str_dst_list = str_dst.split("\n")
    #print(str_dst_list)

    #１行毎に読み上げる(PLAY)
    play_err = False
    for str_dst_line in str_dst_list:
        if len(str_dst_line) != 0:
            #音声ファイル化
            try:
                output = gTTS(str_dst_line, lang=lang_dst, slow=False)
                output.save(TMP_PLAY_FILENAME)
            except Exception as e:
                print("save err: "+str(e))
                play_err = True
                break

            #音声ファイルを再生
            #
            try:
                playsound(TMP_PLAY_FILENAME)
            except Exception as e:
                print("play err: "+str(e))
                play_err = True
                break
            
            #音声ファイルを削除
            try:
                os.remove(TMP_PLAY_FILENAME)
            except Exception as e:
                print("remove err: "+str(e))
                play_err = True
                break
    
    #再生失敗時はエラーポップアップを表示する
    if play_err == True:
        messagebox.showerror("エラー", "再生に失敗しました")

    #print("play_task end !!")
    #一括ボタン押下禁止解除
    btn_all_inhibit(False)


############################################################
#リセットボタンが押されました
############################################################
def btn_reset_clicked():
    global trans_dir

    trans_dir = TRANS_DIR_RIGHT

    #Label
    label_left['text'] = "翻訳元"
    label_right['text'] = "翻訳先"
    #Text
    text_left.config(state=tkinter.NORMAL)
    text_left.delete('1.0', tkinter.END)
    text_left.config(bg='white', bd=1)
    text_right.config(state=tkinter.NORMAL)
    text_right.delete('1.0', tkinter.END)
    text_right.config(bg='gray97', bd=0)
    text_right.config(state=tkinter.DISABLED)
    #Combobox
    cb_menu = [] #メニューリスト
    for val in lang_auto_puls_tbl:
        cb_menu.append(val[LANG_TBL_NAME])
    cb_left.config(values=cb_menu)
    cb_left.current(0)
    cb_right.current(0)

    #翻訳ボタン
    btn_trans_dir['text'] = trans_dir_text_tbl[trans_dir]
    return


root = tkinter.Tk()
root.title("翻訳くん")
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
for val in lang_auto_puls_tbl:
    cb_menu.append(val[LANG_TBL_NAME])
v_left = tkinter.StringVar()
cb_left = ttk.Combobox(frame_trans, textvariable=v_left, values=cb_menu, state="readonly", width=25)
cb_left.current(0)
cb_left.grid(row=1, column=0)

#Text
text_left = tkinter.Text(frame_trans,  relief=tkinter.SOLID, width=60,height=40, padx=10)
text_left.config(state=tkinter.NORMAL)   #入力許可
text_left.config(bg="white", bd=1)    #入力許可時のText表示
text_left.grid(row=2, rowspan=3, column=0, padx=10, pady=10)


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
btn_trans.grid(row=2, column=1,sticky=tkinter.S, padx=5, pady=5)

#読み上げボタン
btn_play = tkinter.Button(frame_trans, text="翻訳+PLAY", width=15, command=btn_play_clicked)
btn_play.grid(row=3, column=1,sticky=tkinter.N, padx=5, pady=5)


#リセットボタン
btn_reset = tkinter.Button(frame_trans, text="リセット", width=10, command=btn_reset_clicked)
btn_reset.grid(row=4, column=1, sticky=tkinter.N,padx=5, pady=5)


#-----------------------------------------------------------
#右側の言語メニュー
#-----------------------------------------------------------
#ラベル
label_right = tkinter.Label(frame_trans, text="翻訳先")
label_right.grid(row=0, column=2)


#Combobox
cb_menu = [] #メニューリスト
for val in lang_tbl:
    cb_menu.append(val[LANG_TBL_NAME])
v_right = tkinter.StringVar()
cb_right = ttk.Combobox(frame_trans, textvariable=v_right, values=cb_menu, state="readonly", width=25)
cb_right.current(0)
cb_right.grid(row=1, column=2)

#Text
text_right = tkinter.Text(frame_trans, relief=tkinter.SOLID, width=60, height=40,padx=10)
text_right.config(state=tkinter.DISABLED)   #入力規制
text_right.config(bg="gray97", bd=0)    #入力規制時のText表示
text_right.grid(row=2, rowspan=3, column=2, padx=10, pady=10)


#root.resizable(False, False)    #ウィンドウサイズ固定
root.mainloop()
