import tkinter
from tkinter import ttk


root = tkinter.Tk()
root.title("Trans")
root.geometry("600x400")

frame_top = tkinter.Frame(root)
frame_top.propagate(0)
frame_top.pack(side=tkinter.TOP)

btn_trans = tkinter.Button(frame_top, text="翻訳", width=15)
btn_trans.grid(row=0, column=0, sticky=tkinter.W)

btn_clr = tkinter.Button(frame_top, text="取消", width=15)
btn_clr.grid(row=0, column=1, sticky=tkinter.E)



#root.resizable(False, False)    #ウィンドウサイズ固定
root.mainloop()
