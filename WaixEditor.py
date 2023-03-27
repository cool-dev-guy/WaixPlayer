# legacy variant
# player_waix_widget
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import ttk,messagebox,filedialog
#3840×2160
config=[900,600]
ratio = config[0]/config[1]
print(ratio)
global onWinDistroy
class PlayerWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.PlayerWidget = PlayerWidget(self,height=800,width=600,bg="#111")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.PlayerWidget.grid(column=0,row=0,sticky=tk.NSEW)

        self.option_add('*highlightThickness', 0)
        self.option_add('*highlightBackground', '#111')

        self.geometry("950x650")
        self.title('Waix')

        self.protocol("WM_DELETE_WINDOW", self.distroyAppWindow)
        self.onWinDistroy = False
    def distroyAppWindow(self):
        print("Going to close")
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.onWinDistroy = True
            self.destroy()
    def triggerNewProjectDialog(self):
        pass
    def triggerOpenDialog(self,type):
        self.path = filedialog.askopenfilename(
            defaultextension=".mp4",
            filetypes=[("Videos", "*.mp4"), ("All Files", "*.*")],
            # initialdir="~/Documents",
            # initialfile="my_file.txt",
            title=f"Open {type}"
        )
        return self.path
class Player(tk.Canvas):
    def __init__(self,parent,*args,**kwargs):
        tk.Canvas.__init__(self, parent)
        print('Player initialized')
        self.config(*args,**kwargs)
        self.bind("<Configure>", self.configResize)
        print(*args)
        self.height = 200
        self.width = 300
        self.parrent = parent
    def configResize(self,e):
        self.height = self.parrent.winfo_height()-20
        self.width = ((self.parrent.winfo_height()-20)*ratio)
        self.config(width=int(self.width),height=int(self.height))
        #print(self.winfo_height(),self.winfo_width(),self.height,self.width)
    def player_playVID(self,file):
        self.player_loadedVID = cv2.VideoCapture(file)
        while True:
            if self.master.master.master.onWinDistroy:break
            ret, frame = self.player_loadedVID.read()
            if not ret:
                break
            self.player_currentIMG_INSTANCE = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)).resize((int(self.width),int(self.height)), Image.LANCZOS))
            self.create_image(0, 0, image=self.player_currentIMG_INSTANCE, anchor=tk.NW)
            self.update()
        self.player_loadedVID.release()
class Controls(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self, parent)
        print('Controls initialized')
        self.config(*args,**kwargs)
class ControlsButtons(tk.Button):
    def __init__(self,parent,*args,**kwargs):
        tk.Button.__init__(self, parent)
        print('ControlsButtons initialized')
        self.config(*args,**kwargs)
class PlayerContainer(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self, parent)
        print('PlayerContainer initialized')
        self.config(*args,**kwargs)
        self.player = Player(self,bg='#111',height=200,width=300)
        
    def configPlayer(self,r):
        self.player.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
class PlayerWidget(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self, parent)
        print('PlayerWidget initialized')
        # remoove unwanted lines
        self.option_add('*highlightThickness', 0)
        self.option_add('*highlightBackground', 'white')
        # config
        self.config(**kwargs)
        self.player_loadedVID = ""
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=0)
        # create player instance
        self.player_container = PlayerContainer(self,bg='#333',height=200,width=300)
        self.player_container.grid(column=0,row=0,sticky=tk.NSEW,padx=10,pady=10)
        #self.player.pack(padx=10,pady=10,fill="both", expand=True)
        # create controls
        self.controls = Controls(self)
        self.button= ControlsButtons(self.controls,text='->')
        self.button2= ControlsButtons(self.controls,text='<-',command=lambda:self.player_container.configPlayer(ratio))
        self.button3= ControlsButtons(self.controls,text='==',command=lambda:self.player_container.player.player_playVID("video.mp4"))

        self.button.grid(column=0,row=0)
        self.button2.grid(column=1,row=0)
        self.button3.grid(column=2,row=0)
        self.controls.grid(column=0,row=1,sticky=tk.NSEW,padx=10,pady=10)





if __name__ == "__main__":
    win = PlayerWindow()

    win.mainloop()
