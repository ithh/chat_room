#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
import socket, threading


def on_send_msg():
    nick_name = "辉"
    chat_msg = chat_msg_box.get(1.0, "end")
    if chat_msg == "\n":
        return

    chat_data = nick_name + ":" + chat_msg
    chat_data = chat_data.encode()
    data_len = "{:<15}".format(len(chat_data)).encode()

    try:
        sock.send(data_len)
        sock.send(chat_data)
    except:
        # sock.close()
        tk.messagebox.showerror("温馨提示", "发送消息失败，请检查网络连接！")
    else:
        chat_msg_box.delete(1.0, "end")
        chat_record_box.configure(state=tk.NORMAL)
        chat_record_box.insert("end", chat_data.decode() + "\n")
        chat_record_box.configure(state=tk.DISABLED)


def recv_chat_msg():
    global sock

    while True:
        try:
            while True:
                    msg_len_data = sock.recv(15)
                    if not msg_len_data:
                        break

                    msg_len = int(msg_len_data.decode().rstrip())
                    recv_size = 0
                    msg_content_data = b""
                    while recv_size < msg_len:
                        tmp_data = sock.recv(msg_len - recv_size)
                        if not tmp_data:
                            break
                        msg_content_data += tmp_data
                        recv_size += len(tmp_data)
                    else:
                        # 显示
                        chat_record_box.configure(state=tk.NORMAL)
                        chat_record_box.insert("end", msg_content_data.decode() + "\n")
                        chat_record_box.configure(state=tk.DISABLED)
                        continue
                    break
        finally:
                sock.close()
                sock = socket.socket()
                sock.connect(("39.107.243.179", 9999))


sock = socket.socket()
sock.connect(("39.107.243.179", 9999))

mainWnd = tk.Tk()
mainWnd.title("辉的聊天室")

chat_record_box = tk.Text(mainWnd)
chat_record_box.configure(state=tk.DISABLED)
chat_record_box.pack(padx=10, pady=10)

chat_msg_box = tk.Text(mainWnd)
chat_msg_box.configure(width=65, height=5)
chat_msg_box.pack(side=tk.LEFT, padx=10, pady=10)

send_msg_btn = tk.Button(mainWnd, text="发 送", command=on_send_msg)
send_msg_btn.pack(side=tk.RIGHT, padx=10, pady=10, ipadx=15, ipady=15)

threading.Thread(target=recv_chat_msg).start()

mainWnd.mainloop()

sock.close()