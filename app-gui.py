from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
from PIL import ImageTk, Image
# from gender_prediction import emotion,ageAndgender
names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Latha', size=25, weight="bold")
        #self.configure(bg='#9A31D9')
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("1024x760" )
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        # container.configure(bg='#69F7FF')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='face.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4 )
            label = tk.Label(self, text="        Home Page        ", font="Stencil 20",fg="#BC1100")
            label.grid(row=0, sticky="ew")
            button1 = tk.Button(self, text="   New User  ",height="2",width="8", fg="#ffffff", bg="#000D62",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Existing User  ",height="2",width="12", fg="#ffffff", bg="#000D62",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Quit", height="2",width="6",fg="#000000", bg="#FFB057", command=self.on_closing)
            button1.grid(row=1, column=0, ipady=5, ipadx=7)
            button2.grid(row=2, column=0, ipady=5, ipadx=2)
            button3.grid(row=3, column=0, ipady=5, ipadx=32)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#6C00A2", font='Stencil 40').grid(row=1, column=2,ipadx=20, ipady=10, pady=20,sticky='w')
        self.user_name = tk.Entry(self, borderwidth=5, bg="lightgrey", font='Gisha 30')
        self.user_name.grid(row=2, column=2, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=3, column=2,ipadx=5, ipady=4, pady=15)
        self.buttonext.grid(row=4, column=2,ipadx=10, ipady=10,  pady=20)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select user", fg="#263942", font='Stencil 35 ').grid(row=0, column=0, padx=10, pady=10,ipadx=20, ipady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="pink")
        self.dropdown["menu"].config(bg="#CED3FF")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=25, padx=10, pady=10,)
        self.buttoncanc.grid(row=1, ipadx=15, ipady=10, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=10, ipady=10, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Stencil 35', fg="#5A0032")
        self.numimglabel.grid(row=0, column=1, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#1D6E20",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=1, ipadx=20, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=2, column=1, ipadx=20, ipady=5, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 200 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 200:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 200 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Stencil 35',fg="#003080", )
        label.grid(row=2,column=2, sticky="w",ipadx=30, ipady=10, padx=10, pady=10)
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#00A60C")
        # button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        # button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#B0C3E3", fg="#263942")
        button1.grid(row=3,column=2, sticky="ew", ipadx=15, ipady=10, padx=10, pady=10)
        # button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        # button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=5,column=2, sticky="ew", ipadx=15, ipady=10, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)



app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()

