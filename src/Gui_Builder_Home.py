import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from tkinter import ttk  
from PIL import Image, ImageTk

FONT= ("Verdana", 10)

class EMVTagTool(tk.Tk):

    def __init__(self, *args, **kwargs):
        

        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.master.title("EMV Tags Decoder")
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (HomePage, EpsilonUserPage, ExternalUserPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.BOTH, side = "bottom")

        load = Image.open("GUIImages/ncr-logo-2017.jpeg")
        render = ImageTk.PhotoImage(load)
        image1 = tk.Label(bottom_frame, image=render)
        image1.image= render
        image1.pack()

        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.BOTH, side = "top")

        load = Image.open("GUIImages/HackTagPic.png")
        render = ImageTk.PhotoImage(load)
        label1 = tk.Label(top_frame, image=render)
        label1.image= render
        label1.pack()

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(fill=tk.BOTH)

        label2 = tk.Label(sub_frame1, text="Welcome to NCR's HackTag Application.\n"+
                                     "This application is designed to help you have a glance at the list of tags with their values at once.\n"+
                                     "You can also get bit by bit explanation for the given tag value.\n\n"+
                                     "Please select the relevant option.", font=("Times", 15), )
        label2.pack(padx=20, pady=20)

        button = tk.Button(self, text="Epsilon User",relief=tk.RAISED,
                            command=lambda: controller.show_frame(EpsilonUserPage))
        button.pack(pady=10)

        button2 = tk.Button(self, text="External User",relief=tk.RAISED,
                            command=lambda: controller.show_frame(ExternalUserPage))
        button2.pack(pady=10)
    
class EpsilonUserPage(tk.Frame):
    def __init__(self, parent, controller):
        transaction_id = []
        tags = []
        tags_values = []
        current=0
        filename = ""
        def UploadAction(event=None):
            area.delete("1.0","end")
            trannum.set("")
            tag.set("")
            filename = filedialog.askopenfilename()
            textBoxFilePath.delete('1.0', tk.END)
            textBoxFilePath.insert(tk.INSERT, filename)
            # Preprocessing of the file data
            self.filename = filename
            import parseCacheLogForEMVTransactionNumbers as u
            transaction_id = u.search_multiple_strings_in_file(filename)
            tags = []
            tags_values =[]
            #transactionIdCombobox()
            self.transaction_id=transaction_id
            self.tags=tags
            self.tags_values=tags_values
        def transactionIdCombobox():
            trannum['values'] = self.transaction_id
        def transactionIdSelection(event=None):
            area.delete("1.0","end")
            self.current = trannum.current()
            self.tags_values = []
            import getAssociatedEMVTags as a
            self.tags_values = a.getAssociatedEMVTags(self.filename,self.transaction_id[trannum.current()])
            
            self.tags = []
            for i in self.tags_values:
                self.tags.append(i[0])
            tagCombobox()
        def tagCombobox():
            tag['values'] = self.tags
        def tagSelection(event=None):
            # API result for selected tag
            area.delete("1.0","end")
            self.current = tag.current()
            import EMVDecoder
            singletaginfo = [self.tags_values[self.current]]
            d = EMVDecoder.decodeTags(singletaginfo)
            for keys,values in d.items():
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
        def exportAction(event=None):
            import filecreation
            import EMVDecoder
            result = EMVDecoder.decodeTags(self.tags_values)
            filecreation.export_excel(result)
            import os
            cwd=os.getcwd()
            area.delete("1.0","end")
            area.insert(tk.END, "Tag details have been exported to 'TagDetails.xlsx at path " + cwd)
        def clearEpsilonScreen(event=None):
            area.delete("1.0","end")
            textBoxFilePath.delete("1.0","end")
            self.transaction_id=[]
            self.tags=[]
            trannum.set("")
            tag.set("")

            
        tk.Frame.__init__(self,parent)
        load = Image.open("GUIImages/EpsilonUserPage.png")
        render = ImageTk.PhotoImage(load)
        label1 = tk.Label(self, image=render)
        label1.image= render
        label1.pack()
        top_frame = tk.Frame(self)
        top_frame.pack(fill = tk.BOTH,)
        top_frame.columnconfigure(3, weight=1)
        top_frame.columnconfigure(5, pad=7)
        top_frame.rowconfigure(4, weight=1)
        top_frame.rowconfigure(6, pad=7)
        label1=Label(top_frame, text='Click below to browse the CacheManager log', font=("Times", 13))
        label1.grid(sticky=tk.W,column=1)
        textBoxFilePath = tk.Text(top_frame, height=1, width=40)
        textBoxFilePath.grid(sticky=tk.W,row=1, column=1)
        # Preprocessing file
        upload_button = tk.Button(top_frame, text='Upload',relief=tk.RAISED, command = lambda: UploadAction(self))
        upload_button.grid(sticky=tk.E,row=1, column=0, padx=5)
        
        label2=Label(top_frame, text='Transaction IDs', font=("Times", 12))
        label2.grid(sticky=tk.E,row=2,column=0)
        # Selecting tansaction id
        trannum = ttk.Combobox(top_frame,values="",postcommand= lambda: transactionIdCombobox())
        trannum.bind("<<ComboboxSelected>>", transactionIdSelection)
        trannum.grid(sticky = tk.W,row=2, column=1)
        
        label2=Label(top_frame, text='Tags', font=("Times", 12))
        label2.grid(sticky=tk.E,row=3,column=0)
        # Selecting tags
        tag = ttk.Combobox(top_frame,values="",postcommand= lambda: [tagCombobox()])
        tag.bind("<<ComboboxSelected>>", tagSelection)
        tag.grid(sticky=tk.W,row=3,column=1)

        or_label = Label(top_frame, text="(or)")
        or_label.grid(row=3, column =1)

        export_button = tk.Button(top_frame, text = "Export", relief=tk.RAISED,command = lambda: exportAction(self))
        export_button.grid(sticky=tk.E,row=3, column=1)

        area = tk.Text(top_frame,width= 70,height = 15)
        area.grid(row=4,column=1)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, side = "bottom")
        load = Image.open("GUIImages/ncr-logo-2017.jpeg")
        render = ImageTk.PhotoImage(load)
        label1 = tk.Label(frame2, image=render)
        label1.image= render
        label1.pack(side="left")
        
        button2 = tk.Button(frame2, text="Back to Home Page",relief=tk.RAISED,
                            command=lambda: (clearEpsilonScreen(self),controller.show_frame(HomePage)))
        button2.pack(side = tk.RIGHT, padx=20)
        """controller.show_frame(HomePage)"""
            

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
                           command=lambda: ( clearExternalUserScreen(self), controller.show_frame(HomePage)))
        button2.pack(side = tk.RIGHT, padx = 12 )
app = EMVTagTool()
app.geometry("900x750+300+300")
app.resizable(width=False, height=False)
app.mainloop()

