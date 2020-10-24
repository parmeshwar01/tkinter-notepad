from tkinter import *
import tkinter.messagebox as tmsg
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

root = Tk()
root.title("Untitled - Notepad")
root.wm_iconbitmap("notpad.ico")
root.geometry("644x788")

TextArea = Text(root, font="lucida 13")
TextArea.insert(INSERT,"")
TextArea.tag_configure("start", background="yellow",foreground='black')
file = None
TextArea.pack(expand=True, fill=BOTH)



def find(): 
      
    #remove tag 'found' from index 1 to END 
    TextArea.tag_remove('found', '1.0', END)  
      
    #returns to widget currently in focus 
    s = edit.get()  
    if s: 
        idx = '1.0'
        while 1: 
            #searches for desried string from index 1 
            idx = TextArea.search(s, idx, nocase=1,  
                              stopindex=END)  
            if not idx: break
              
            #last index sum of current index and 
            #length of text 
            lastidx = '%s+%dc' % (idx, len(s))  
              
            #overwrite 'Found' at idx 
            TextArea.tag_add('found', idx, lastidx)  
            idx = lastidx 
          
        #mark located string as red 
        TextArea.tag_config('found', foreground='red')  
    edit.focus_set() 


f1 = Frame(root,bg="white",borderwidth="1")
f1.pack(fill= X,side = BOTTOM,pady =1)

edit = Entry(f1)  
edit.pack(side=LEFT, fill=X,expand=1)  
#setting focus 
edit.focus_set()

Button(f1,text="search",command=find).pack(anchor="e")


def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)


def openFile():
    global file
    file = askopenfilename(defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                     ("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - Notepad")
        TextArea.delete(1.0, END)
        f = open(file, "r")
        TextArea.insert(1.0, f.read())
        f.close()


def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                     ("Text Documents", "*.txt")])
        if file =="":
            file = None

        else:
            #Save as a new file
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()

            root.title(os.path.basename(file) + " - Notepad")
            print("File Saved")
    else:
        # Save the file
        f = open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()


def cut():
    TextArea.event_generate(("<<Cut>>"))

def copy():
    TextArea.event_generate(("<<Copy>>"))

def paste():
    TextArea.event_generate(("<<Paste>>"))

def highlight():
    TextArea.tag_add("start", "sel.first", "sel.last")    

def about():
    tmsg.showinfo("Notepad", "Notepad using Tkinter")



MenuBar = Menu(root)


FileMenu = Menu(MenuBar, tearoff=0)

FileMenu.add_command(label="New", command=newFile)
FileMenu.add_command(label="Open", command = openFile)
FileMenu.add_command(label = "Save", command = saveFile)
FileMenu.add_separator()
FileMenu.add_command(label = "Exit", command = root.destroy)
MenuBar.add_cascade(label = "File", menu=FileMenu)


EditMenu = Menu(MenuBar, tearoff=0)

EditMenu.add_command(label = "Cut", command=cut)
EditMenu.add_command(label = "Copy", command=copy)
EditMenu.add_command(label = "Paste", command=paste)
EditMenu.add_separator()
EditMenu.add_command(label ="Highlight",command=highlight)
MenuBar.add_cascade(label="Edit", menu = EditMenu)


HelpMenu = Menu(MenuBar, tearoff=0)

HelpMenu.add_command(label = "About", command=about)
MenuBar.add_cascade(label="Help", menu=HelpMenu)


root.config(menu=MenuBar)

#RightClick Menu
m = Menu(root, tearoff = 0) 
m.add_command(label ="Cut",command=cut) 
m.add_command(label ="Copy",command=copy)
m.add_command(label ="Paste",command=paste)
m.add_separator()
m.add_command(label ="Highlight",command=highlight)

def do_popup(event): 
    try: 
        m.tk_popup(event.x_root, event.y_root) 
    finally: 
        MenuBar.grab_release() 
TextArea.bind("<Button-3>", do_popup) 
#RightClick Menu Ends

Scroll = Scrollbar(TextArea)
Scroll.pack(side=RIGHT,  fill=Y)
Scroll.config(command=TextArea.yview)
TextArea.config(yscrollcommand=Scroll.set)

root.mainloop()