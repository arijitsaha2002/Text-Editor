import tkinter as tk
import tkinter.filedialog as tkf
import os



# all constants
Window_W = 1500
Window_H = 800
TOPBAR_H = 40
TEXT_COLOR = 'black'
BACKGROUD_COLOR = 'white'
IS_AUTO_SAVE = False
BUILD_SYSTEM = None
FONT_SIZE = 16

# initial
root = tk.Tk()
root.title("Text Editor")
editor = tk.Text(root, font=FONT_SIZE)
scroll = tk.Scrollbar(editor)
root.geometry(str(Window_W)+'x'+str(Window_H))
text = None
path = None

# basics
def remove_editor():
    scroll.destroy()
    editor.destroy()

def file_name(p):
    temp = p[::-1]
    n = temp.index("/")
    temp = temp[:n]
    return temp[::-1]

def change_title():
    if path is None:
        root.title("Untitled")
    else:
        root.title(file_name(path))

def open_new_editor():
    global editor, scroll , TEXT_COLOR , BACKGROUD_COLOR
    remove_editor()
    editor = tk.Text(root, font=FONT_SIZE,foreground=TEXT_COLOR,background=BACKGROUD_COLOR)
    editor.pack(side='bottom', expand=True, fill="both")
    scroll = tk.Scrollbar(editor)
    scroll.config(command=editor.yview, width=20)
    editor.config(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill='y')
    change_title()




def save():
    global path
    temp = path
    if path == None:
        path = tkf.asksaveasfilename()
    if not path:
        path = temp
        return False
    file = open(path, "w+")
    file.write(editor.get('1.0', 'end-1c'))
    file.close()
    change_title()
    return True

# file menus


def new():
    if IS_AUTO_SAVE:
        global path
        temp = path
        path = tkf.asksaveasfilename()
        if  path:
            open_new_editor()
            save()
        else:
            path = temp
    else:
        open_new_editor()


def open_text():
    global root, editor , path , TEXT_COLOR , BACKGROUD_COLOR
    path = tkf.askopenfilename(
        filetypes=[["All Files", "*.*"]],
    )
    if not path:
        return
    open_new_editor()
    file = open(path, "r+")
    text = file.read()    
    editor.insert(1.0, text)
    file.close()
    change_title()


def saveas():
    global path
    path = tkf.asksaveasfilename()
    if not path:
        return
    file = open(path, "w+")
    file.write(editor.get('1.0', 'end-1c'))
    file.close()
    change_title()

def refresh_file():
    global path
    if path != None:
        open_new_editor()
        file = open(path, "r+")
        text = file.read()    
        editor.insert(1.0, text)
        file.close()

# Edit functions 

def select_all():
    # editor.event_generate(("<<selectall>>"))
    pass


def cut_text():
    editor.event_generate(("<<Cut>>"))


def copy_text():
    editor.event_generate(("<<Copy>>"))


def paste_text():
    editor.event_generate(("<<Paste>>"))

def find_text():
    pass

def replace_text():
    pass

# setting menus

def auto_save():
    global IS_AUTO_SAVE
    IS_AUTO_SAVE = not IS_AUTO_SAVE
    if IS_AUTO_SAVE:
        save()
    change_title()


# run


def interpreter_run(interpreter):
    save()
    if path == None:
        return
    temp = path.replace(" ","\ ")
    c = f"gnome-terminal -- bash -c \"{interpreter} {temp} && echo ; echo PRESS ENTER ; read;\""
    os.system(c)

def c_run(compiler):
    save()
    if path == None:
        return
    temp = path.replace(" ","\ ")
    n = temp[::-1].index(".")+1
    c = f"gnome-terminal -- bash -c \"{compiler} {temp} -o {temp[:-n]} && {temp[:-n]} && echo ; echo PRESS ENTER ; read;\""
    os.system(c)

def run():
    if path == None:
        return
    global BUILD_SYSTEM
    if (path.endswith(".cpp") and BUILD_SYSTEM.get() == "auto") or BUILD_SYSTEM.get() == ".cpp":
        c_run("g++")
    elif (path.endswith(".c") and BUILD_SYSTEM.get() == "auto") or BUILD_SYSTEM.get() == ".c":
        c_run("gcc")
    elif (path.endswith(".pl") and BUILD_SYSTEM.get() == "auto") or BUILD_SYSTEM.get() == ".pl":
        interpreter_run("prolog")
    elif (path.endswith(".tex") and BUILD_SYSTEM.get() == "auto") or BUILD_SYSTEM.get() == ".tex":
        interpreter_run("pdflatex") 
    elif (path.endswith(".py") and BUILD_SYSTEM.get() == "auto") or BUILD_SYSTEM.get() == ".py":
        interpreter_run("python3")
    elif (path.endswith(".sh") and BUILD_SYSTEM.get() == "auto") or BUILD_SYSTEM.get() == ".sh":
        interpreter_run("sh")


# help
def keybinding():
    pass
def about_editor():
    pass



# Manu bar
# file
file_menu = tk.Menu(root)
topbar = tk.Menu(file_menu, tearoff=0)

topbar.add_command(label="New", command=new)
topbar.add_command(label="Open", command=open_text)
topbar.add_command(label="Save", command=save)
topbar.add_command(label="Save As",command=saveas)
topbar.add_command(label="Refresh",command=refresh_file)

file_menu.add_cascade(label="FILE", menu=topbar)


# Edit
file_menu.add_separator(background='black')
edit_manu = tk.Menu(file_menu, tearoff=0)

edit_manu.add_command(label="Select All", command=select_all)
edit_manu.add_command(label="Copy", command=copy_text)
edit_manu.add_command(label="Cut", command=cut_text)
edit_manu.add_command(label="Paste", command=paste_text)
edit_manu.add_command(label="Find", command=find_text)
edit_manu.add_command(label="Replace", command=replace_text)

file_menu.add_cascade(label="Edit", menu=edit_manu)

# settings
BUILD_SYSTEM = tk.StringVar()
BUILD_SYSTEM.set("auto")

file_menu.add_separator(background='black')
setting_manu = tk.Menu(file_menu, tearoff=0)

setting_manu.add_checkbutton(label="Auto Save",command=auto_save)
build_manu = tk.Menu(setting_manu,tearoff=0)

# build and run

build_manu.add_radiobutton(label="Auto",variable=BUILD_SYSTEM,value="auto")
build_manu.add_radiobutton(label="gcc",variable=BUILD_SYSTEM,value=".c")
build_manu.add_radiobutton(label="g++",variable=BUILD_SYSTEM,value=".cpp")
build_manu.add_radiobutton(label="pdflatex",variable=BUILD_SYSTEM,value=".tex")
build_manu.add_radiobutton(label="prolog",variable=BUILD_SYSTEM,value=".pl")
build_manu.add_radiobutton(label="python",variable=BUILD_SYSTEM,value=".py")
build_manu.add_radiobutton(label="shell",variable=BUILD_SYSTEM,value=".sh")
setting_manu.add_cascade(label="Build System", menu=build_manu)

file_menu.add_cascade(label="Setting",menu=setting_manu)
# run

file_menu.add_separator(background='black')
file_menu.add_command(label="Run",command=run)

# help

file_menu.add_separator(background='black')
help_manu = tk.Menu(file_menu,tearoff=0)

help_manu.add_command(label="Keybinding",command=keybinding)
help_manu.add_command(label="About",command=about_editor)

file_menu.add_cascade(label="Help",menu=help_manu)

# keybindings

# root.bind('<F5>', build_run)
# root.bind('<F8>', run)



def closing():
    if IS_AUTO_SAVE and (path != None):
        save()
    root.destroy()


root.config(menu=file_menu)
root.protocol("WM_DELETE_WINDOW", closing)
root.mainloop()

