import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from tkinter import ttk  
from PIL import Image, ImageTk
import Gui_Builder_Home as HomePageObject

FONT= ("Verdana", 10)

class ExternalUserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load = Image.open("GUIImages/EpsilonUserPage.png")
        render = ImageTk.PhotoImage(load)
        label1 = tk.Label(self, image=render)
        label1.image= render
        label1.pack()
        
        top_frame = tk.Frame(self)
        top_frame.pack(fill = tk.BOTH,)
        top_frame.columnconfigure(3, weight=1)
        top_frame.columnconfigure(5, pad=7)
        top_frame.rowconfigure(3, weight=1)
        top_frame.rowconfigure(5, pad=7)
        title = tk.Label(top_frame, text="Welcome, please enter the EMV tag and the respective value.", font=FONT)
        title.grid(sticky=tk.W, pady=5, padx=5)
        tag=''
        value=''
        tag_value=[]
        t1 = tk.StringVar()
        t2 = tk.StringVar()
        def submit():
            self.tag=''
            self.value=''
            self.tag_value=[]
            self.tag = textbox1.get()
            self.value = textbox2.get()
            t1.set("")
            t2.set("")
            area.delete("1.0","end")
            self.tag_value=[(self.tag,self.value)]
            import EMVDecoder
            result = EMVDecoder.decodeTags(self.tag_value)
            for keys,values in result.items():
                if(len(values)==3):
                    if(type(values[2]) != type([])):
                        area.insert(tk.END,"Tag - "+keys+"\nValue - "+ values[0] + "\nTag Name -" +  values[1] + "\n Description - " + values[2]+"\n\n")
                    else:
                        
                        area.insert(tk.END,"Tag - "+keys+"\nValue - "+ values[0] + "\nTag Name -" +  values[1]+"\n\n")
                        for i in values[2]:
                            area.insert(tk.END, i+'\n')
                else:
                    area.insert(tk.END,"Tag - "+keys+"\nValue - "+ values[0] + "\nTag Name -" +  values[1]+"\n\n")
            area.insert(tk.END,"\n")
        def clearExternalUserScreen(event=None):
            area.delete("1.0","end")

            #Here,call the decode function by passing tag and value
            
        taglabel = tk.Label(top_frame, text="Tag:")
        taglabel.grid(row=1,column=0)
        
        textbox1 = tk.Entry(top_frame,textvariable = t1)
        textbox1.grid(row=1,column=1)
        valuelabel = tk.Label(top_frame, text="Tag Value:")
        valuelabel.grid(row=2,column=0)

        
        textbox2 = tk.Entry(top_frame,textvariable = t2)
        textbox2.grid(row=2,column=1)
        
        submit_button = tk.Button(top_frame, text = "Submit",relief=tk.RAISED, command = lambda : submit())
        submit_button.grid(row=3,column=1, pady=5)

        middle_frame = tk.Frame(self)
        middle_frame.pack()

        area = tk.Text(middle_frame,width= 70,height = 15)
        area.grid(pady=5)
        
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.BOTH, side = "bottom")
        
        load = Image.open("GUIImages/ncr-logo-2017.jpeg")
        render = ImageTk.PhotoImage(load)
        label1 = tk.Label(bottom_frame, image=render)
        label1.image= render
        label1.pack(side="left")

        button2 = tk.Button(bottom_frame, text="Back to Home Page",relief=tk.RAISED,
                           command=lambda: ( clearExternalUserScreen(self), controller.show_frame(HomePageObject.HomePage)))
        button2.pack(side = tk.RIGHT, padx = 12 )
