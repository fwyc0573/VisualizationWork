import tkinter as tk
from tkinter import *
from tkinter import ttk
from urllib.request import urlopen
from PIL import Image, ImageTk
from torchvision import transforms as transforms
#import make_pic_2   在这里导入自己的py包文件
num=1
url = r"H:\re\predict_sym1.png"

def calculate(*args):
    print(addr.get(),":",port.get())
    #make_pic_2.main(int(fft.get()),int(start.get()),int(stop.get()),int(cent.get()))
#调用自己的内核函数

def change():       #更新图片操作
    global num
    num=num+1
    if num%3==0:
        url1=r"H:\re\predict_sym2.png"
        global label_img, img
        pil_image = Image.open(url1)
        original = Image.new('RGB', (300, 400))
        load = Image.open(url1)
        load = transforms.Resize((300, 400))(load)
        original = load
        img= ImageTk.PhotoImage(original)
        label_img.configure(image = img)
    # if num%3==1:
    #     url1=r"H:\re\predict_sym2.png"
    #     pil_image = Image.open(url1)
    #     pil_image = transforms.Resize((200, 180))(pil_image)
    #     img= ImageTk.PhotoImage(pil_image)
    #     label_img.configure(image = img)
    # if num%3==2:
    #     url1=r"H:\re\predict_sym1.png"
    #     pil_image = Image.open(url1)
    #     pil_image = transforms.Resize((200, 180))(pil_image)
    #     img= ImageTk.PhotoImage(pil_image)
    #     label_img.configure(image = img)
    root.update_idletasks()   #更新图片，必须update

root = Tk()
root.title("Draw GUI")
root.geometry("1280x1080")


mainframe = ttk.Frame(root, padding="5 4 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


addr = StringVar()
port = StringVar()
fft  = StringVar()
cent = StringVar()
start= StringVar()
stop = StringVar()

label1 = ttk.Label(mainframe,text="Original Picture")

ttk.Label(mainframe, text="Address:").place(x=80,y=25)
addr_entry = ttk.Entry(mainframe, width=7, textvariable=addr)
addr_entry.place(x=10,y=25)

# ttk.Label(mainframe, text="Port:").grid(column=3, row=1, sticky=W)
# port_entry = ttk.Entry(mainframe, width=7, textvariable=port)
# port_entry.grid(column=4, row=1, sticky=(W, E))
#
# ttk.Label(mainframe, text="FFt:").grid(column=1, row=2, sticky=W)
# fft_entry = ttk.Combobox(mainframe, width=7, textvariable=fft)
# fft_entry['values'] = (2048, 4096, 8192)
# fft_entry.current(1)
# fft_entry.grid(column=2, row=2, sticky=(W, E))
#
# ttk.Label(mainframe, text="CenterFR:").grid(column=3, row=2, sticky=W)
# cent_entry = ttk.Entry(mainframe, width=7, textvariable=cent)
# cent_entry.grid(column=4, row=2, sticky=(W, E))
#
# ttk.Label(mainframe, text="StartFR:").grid(column=1, row=3, sticky=W)
# start_entry = ttk.Entry(mainframe, width=7, textvariable=start)
# start_entry.grid(column=2, row=3, sticky=(W, E))
#
# ttk.Label(mainframe, text="StopFR:").grid(column=3, row=3, sticky=W)
# stop_entry = ttk.Entry(mainframe, width=7, textvariable=stop)
# stop_entry.grid(column=4, row=3, sticky=(W, E))

ttk.Button(mainframe, text="Draw!", command=calculate).place(x=600,y=25)
ttk.Button(mainframe, text="Update!", command=change).place(x=80,y=25)


load = Image.open(url)
load = transforms.Resize((300, 800))(load)
img = ImageTk.PhotoImage(load)
label_img = ttk.Label(root, image = img ,compound=CENTER)
label_img.place(x=100,y=605)

# load2 = Image.open(r"H:\re\predict_sym2.png")
# load2 = transforms.Resize((300, 300))(load2)
# img2 = ImageTk.PhotoImage(load)
# label_img2 = ttk.Label(root, image = img2 ,compound=CENTER)
# label_img2.place(x=80,y=25)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
addr_entry.focus()

root.bind('<Return>', calculate)   #主循环，除了这一行可以一直循环，其他行只执行一次

root.mainloop()