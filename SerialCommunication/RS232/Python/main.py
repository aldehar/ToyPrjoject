from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox

from comm import Comm
import comm

class Gui:
    
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("RS232 Serial Communication")

        self.isConnect = False

        self.initWidget()

        print("[COM Port List]")
        portList = comm.getComPortList()
        for port, desc in portList:
            print("{} - {} ".format(port, desc))

    def initWidget(self):
        # 1st
        pnlTop = tk.PanedWindow(self.win)
        pnlTop.pack(side="top", fill="x")
        lblPort = tk.Label(pnlTop, text="Port")
        lblPort.pack(side="left")
        self.entryPort = tk.Entry(pnlTop)
        self.entryPort.insert(0, "COM3")
        self.entryPort.pack(side="left", fill="x", expand=True)
        lblBaud = tk.Label(pnlTop, text="Baud")
        lblBaud.pack(side="left")
        self.entryBaud = tk.Entry(pnlTop)
        self.entryBaud.insert(0, "9600")
        self.entryBaud.pack(side="left", fill="x", expand=True)

        # 2nd
        pnl2nd = tk.PanedWindow(self.win)
        pnl2nd.pack(side="top", fill="x", anchor="c") 
        btnConnect = tk.Button(pnl2nd, text="Connect", command=lambda: self.onBtnClicked("START"))
        btnConnect.pack(side="left", fill="x", expand=True)
        btnDisconnect = tk.Button(pnl2nd, text="Disconnect", command=lambda: self.onBtnClicked("STOP"))
        btnDisconnect.pack(side="left", fill="x", expand=True)

        # 3rd
        pnl3rd = tk.PanedWindow(self.win)
        pnl3rd.pack(side="top", fill="x", anchor="c")
        lblTrx = tk.Label(pnl3rd, text="Receive Detail", anchor="w")
        lblTrx.pack(side="top", fill="x", expand=True)
        self.txtTrx = scrolledtext.ScrolledText(pnl3rd, height=5)
        self.txtTrx.pack(side="top", fill="x", expand=True)
        
        # 4th
        pnl4th = tk.PanedWindow(self.win)
        pnl4th.pack(side="top", fill="x", anchor="c")
        lblSend = tk.Label(pnl4th, text="Send Data", anchor="w")
        lblSend.pack(side="top", fill="x", expand=True)
        self.entrySend = tk.Entry(pnl4th)
        self.entrySend.pack(side="top", fill="x", expand=True)
        btnSend = tk.Button(pnl4th, text="Send", command=lambda: self.onBtnClicked("SEND"))
        btnSend.pack(side="left", fill="x", expand=True)

    def onBtnClicked(self, flag):
        try:
            if flag == "START":
                port = self.entryPort.get()
                baud = self.entryBaud.get()
                nBaud = int(baud)
                self.startConnect(port, nBaud)
            elif flag == "STOP":
                self.stopConnect()
            elif flag == "SEND":
                data = self.entrySend.get()
                self.entrySend.delete(0, tk.END)
                self.sendSerial(data)
        except Exception as e:
            messagebox.showinfo(title="Error", message=e.args)
            print(e)

    def startConnect(self, port, baud):
        try:
            if self.isConnect == False:
                self.cmm = Comm(port, baud, self)
                self.isConnect = True
            else:
                messagebox.showinfo(title="Warn", message="이미 연결 중입니다 !")
        except Exception as e:
            messagebox.showinfo(title="Error", message=e.args)
            print(e)

    def stopConnect(self):
        try:
            if self.isConnect:
                self.cmm.stop()
                self.isConnect = False
            else:
                messagebox.showinfo(title="Warn", message="이미 연결이 끊어졌습니다 !")
        except Exception as e:
            messagebox.showinfo(title="Error", message=e.args)
            print(e)

    def sendSerial(self, data):
        try:
            if self.isConnect:
                if len(data) > 0:
                    self.cmm.send_serial(data)
                else :
                    messagebox.showinfo(title="Warn", message="보낼 메세지가 없습니다.")
            else:
                messagebox.showinfo(title="Warn", message="연결 후, 데이터를 보내주세요 !")
        except Exception as e:
            messagebox.showinfo(title="Error", message=e.args)
            print(e)

    def displayMsg(self, data, strKind):
        now = datetime.now()
        strMsg = "[{}][{}]{}\n".format(now, strKind, data)
        self.txtTrx.insert(tk.END, strMsg)

    def start(self):
        self.win.mainloop()
    
    def __del__(self):
        pass

# 해당 파일을 직접 실행시킬때, 실행 됨 >> python main.py
if __name__ == "__main__":
    win = Gui()
    win.start()