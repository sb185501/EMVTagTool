import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from tkinter import ttk  
from PIL import Image, ImageTk
import Gui_Builder_Home as HomePageObject


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
            area.insert(tk.END, "Tag details have been exported to 'TagDetails.xlsx at path" + cwd)
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
                            command=lambda: (clearEpsilonScreen(self),controller.show_frame(HomePageObject.HomePage)))
        button2.pack(side = tk.RIGHT, padx=20)
        """controller.show_frame(HomePage)"""
