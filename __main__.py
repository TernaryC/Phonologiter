import tkinter as tk
import tkinter.filedialog as tkFile
import tkinter.messagebox as tkMess
from copy import deepcopy
from pyglet.font import add_file as load_font
import pyexcel_ods3 as ods
from os.path import basename as os_name
from playsound import playsound
from collections import OrderedDict
import sys.argv as arguments
from getopt import getopt
from ipa import sort_IPA,                 \
                IPA,          IPA_Other,  \
                IPA_Place,    IPA_Manner, \
                IPA_Backness, IPA_Height, \
                IPA_Type,     IPA_i       \

VERSION = "1.0.0b"
RELEASE = "11/27/20"
load_font("assets/NotoSans-Regular.ttf")



def get_name(name):
    if "/" in list(name): return os_name(name)
    else: return name


class Phono(tk.Frame):
    def __init__(self, parent=None):
        try:
            super().__init__(parent)
            self.root = parent
            self.root.iconbitmap("assets/icon.ico")
            self.root.title("Phonologiter - New Phonology")
            
            self.root.bind_all("<Control-n>", lambda _: self.FILE_new())
            self.root.bind_all("<Control-s>", lambda _: self.FILE_save())
            self.root.bind_all("<Control-o>", lambda _: self.FILE_open())
            self.root.bind_all("<Control-q>", lambda _: self.FILE_quit())
            
            self.grid()
            
            # UI Variables
            self.mode = 0
            self.page = 0
            
            self.modes = []
            self.pages = []
            #
            
            self.IPA_sel = []   # FD
            
            # Screen Storage
            self.ipaScreen = None
            
            self.ipaCon = None
            self.ipaVow = None
            self.ipaOth = None
            
            self.simCon = None
            self.simVow = None
            self.simOth = None
            
            self.testCon = None
            self.testVow = None
            self.testOth = None
            
            self.cellCon = None
            self.cellVow = None
            self.cellOth = None
            #
            
            self.opened = None
            
            self.changed = False
            self.nums = [0, 0, 0]   # FD
            
            # Create UI
            self.create_menu()
            self.create_mode()
            self.create_page()
            self.create_screen()
        except Exception as e:
            self.throw_err("#UC_INITERR", e)
    
    def throw_err(self, code, error="TOTALERROR", suberr="TOTALERROR"):
        msg = ""
        try:
            msg = "Fatal Error: " + code + "\n\n"
            debug = code[:3]
            if debug == "#UC":
                msg += "There was an unknown fatal error while initializing" + \
                       " Phonologiter:\n"
                msg += "{}".format(error)
                msg += """
                
Please contact the developer with this error log.
                       """
            if debug == "#UR":
                msg += "There was an unknown fatal error during runtime:\n"
                msg += "{}".format(error)
                msg += """
                
Please contact the developer with this error log.            
                       """
            if debug == "#IN":
                msg += "An error has occured:\n"
                msg += "{}".format(error)
                msg += "\nDuring the processing of this error, another" + \
                       " fatal error has occured:\n"
                msg += "{}".format(suberr)
                msg += """
                
Please contact the developer with this error log.            
                       """
            if debug == "#FN":
                msg += "There was an unknown fatal error creating a new" + \
                       " phonology:\n"
                msg += "{}".format(error)
                msg += """
                
Please contact the developer with this error log.
                       """
            if debug == "#FS":
                msg += "There was an unknown fatal error while saving" + \
                       " your phonology:\n"
                msg += "{}".format(error)
                msg += """
                
Please contact the developer with this error log.
                       """
            if debug == "#FO":
                msg += "There was a fatal error while loading your phonology:\n"
                if error != "TOTALERROR":
                    msg += "{}".format(error)
                msg += """
                
Your phonology file may have been corrupted or edited by an outside program.
If this error persists, please contact the developer with this error log and the file which has caused this error.
                      """
            if debug == "#FE":
                msg += "There was an unknown fatal error while exporting" + \
                       " your phonology:\n"
                msg += "{}".format(error)
                msg += """
                
Please contact the developer with this error log.
                       """
        except Exception as e:
            msg = "Fatal Error: #XX_UNKERR\n\n"
            msg += "A fatal error has occured during error resolution." + \
                   " How meta!\n"
            msg += "{}".format(e)
            msg += "\nThis error occured while trying to process the" + \
                   " following error:\n"
            msg += "{}".format(code)
            msg += """

On a serious note, please contact the developer with this error log, as clearly something has gone horribly and terribly wrong.
                   """
                   
        msg += "\nPhonologiter version: " + VERSION
        msg += "\n\nPhonologiter will now exit."
        tkMess.showerror(title="Phonologiter", message=msg)
        self.root.quit()
    
    def FILE_quit(self):
        if self.changed:
            txt = "Do you want to save the current phonology?"
            ans = tkMess.askyesnocancel(title="Phonologiter", message=txt)
            if ans is None: return
            if ans is True:
                saved = self.FILE_save()
                if not saved: return
        self.root.quit()
        quit()
    
    def create_menu(self):
        try:
            menubar = tk.Menu(self.root)
            
            filemenu = tk.Menu(menubar, tearoff=0)
            filemenu.add_command(label="New File...", command=self.FILE_new,
                                 underline=0, accelerator="Ctrl+N")
            filemenu.add_command(label="Open File...", command=self.FILE_open,
                                 underline=0, accelerator="Ctrl+O")
            filemenu.add_command(label="Save File...", command=self.FILE_save,
                                 underline=0, accelerator="Ctrl+S")
            filemenu.add_separator()
            filemenu.add_command(label="Export File...",
                                 command=self.FILE_export, underline=1)
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=self.root.quit,
                                 accelerator="Ctrl+Q")
            menubar.add_cascade(label="File", menu=filemenu, underline=0)
            
            helpmenu = tk.Menu(menubar, tearoff=0)
            #helpmenu.add_command(label="Help", underline=1)
            #helpmenu.add_separator()
            helpmenu.add_command(label="About Phonologiter", underline=0,
                                 command=self.HELP_about)
            menubar.add_cascade(label="Help", menu=helpmenu, underline=0)
            
            self.root.config(menu=menubar)
        except Exception as e:
            self.throw_err("#UC_MENUERR", e)
    
    def FILE_new(self, called=False):
        try:
            if not called and self.changed:
                txt = "Do you want to save the current phonology?"
                ans = tkMess.askyesnocancel(title="Phonologiter", message=txt)
                if ans is None: return
                if ans is True:
                    saved = self.FILE_save()
                    if not saved: return
        
            self.IPA_sel = []
            self.nums = [0, 0, 0]
            
            self.ipaScreen = None
            
            self.ipaCon = None
            self.ipaVow = None
            self.ipaOth = None
            
            self.simCon = None
            self.simVow = None
            self.simOth = None
            
            self.cellCon = None
            self.cellVow = None
            self.cellOth = None
            
            if not called: self.opened = None
            if not called: self.root.title("Phonologiter - New Phonology")
            self.changed = False
            
            self.mode = 0
            self.page = 0
            self.change_mode(0, True)
            self.change_page(0, True)
            self.create_screen()
            self.fix_screens()
        except Exception as e:
            self.throw_err("#FN_UNKERR", e)
           
    def FILE_save(self):
        try:
            op = "New Phonology.phn" if self.opened is None else self.opened
            f = tkFile.asksaveasfile(mode="w", initialfile=op, 
                                     defaultextension=".phn")
            if f is None: return False
            if f.name == "":
                txt = "You must name your Phonology before saving."
                tkMess.showwarning(title="Phonologiter", message=txt)
                return False
            self.opened = str(f.name)
            self.root.title("Phonologiter - " + self.opened)
            
            file = ""
            file += ",".join([str(n) for n in self.nums])
            file += ";"
            dc = False
            for s in self.IPA_sel:
                if dc: file += ","
                file += str(ord(s))
                dc = True
            
            f.write(file)
            f.close()
            
            self.changed = False
            return True
        except Exception as e:
            self.throw_err("#FS_UNKERR", e)
        
    def FILE_open(self):
        try:
            if self.changed:
                txt = "Do you want to save the current phonology?"
                ans = tkMess.askyesnocancel(title="Phonologiter", message=txt)
                if ans is None: return
                if ans is True:
                    saved = self.FILE_save()
                    if not saved: return
            
            f = tkFile.askopenfile(mode="r",
                                   filetypes=[("Phonologies", ".phn")])
            if f is None: return
            self.opened = str(f.name)
            self.root.title("Phonologiter - " + self.opened)
            file = f.read()
            f.close()
            
            self.FILE_new(True)
            
            data = file.split(";")
            try: self.nums = [int(s) for s in data[0].split(",")]
            except ValueError: self.throw_err("#FOL0_NUMERR")
            if len(self.nums) != 3: self.throw_err("#FOL0_LENERR")
            data = data[1].split(",")

            for i in range(0, len(data)):
                symb = data[i]
                try: self.IPA_sel.append(chr(int(symb)))
                except ValueError: self.throw_err("#FOL1_SELERR")
            
            for s in self.IPA_sel:
                if s not in IPA: self.throw_err("#FOL2_SYMBERR")
                ipa = IPA[s]
                if ipa.type == 0: search = self.cellCon
                if ipa.type == 1: search = self.cellVow
                if ipa.type == 2: search = self.cellOth
                try: search
                except NameError: self.throw_err("#FOL2_TYPERR")

                checker = search[ipa.row()][ipa.col()]
                if checker is None: self.throw_err("#FOL2_CHECKERR")
                sym = checker.winfo_children()[0]
                
                sym.config(compound=tk.TOP)
                sym.config(fg="#00F")
                sym.config(disabledforeground="#009")
            
            self.update_SIM()
        except Exception as e:
            self.throw_err("#FO_UNKERR", e)
           
    def FILE_export(self):
        try:
            if all([n == 0 for n in self.nums]):
                txt = "You cannot export an empty sheet."
                tkMess.showwarning(title="Phonologiter", message=txt)
                return
        
            try:
                op = "New Phonology.ods" if self.opened is None else self.opened
                if op[-4:] == ".phn": op = op[:-4] + ".ods"
                f = tkFile.asksaveasfile(mode="wb", initialfile=op,
                                         defaultextension=".ods")
            except PermissionError as e:
                txt = "Error saving file. That file may be open in another " +\
                      "program. Please close out of that program before trying " +\
                      "again."
                tkMess.showwarning(title="Phonologiter", message=txt)
                return
            if f is None: return
            if f.name == "":
                txt = "You must name your Phonology before exporting."
                tkMess.showwarning(title="Phonologiter", message=txt)
                return False
        
            conIpa = self.manifest_IPA_cons(self.root, True)
            vowIpa = self.manifest_IPA_vows(self.root, True)
            othIpa = self.manifest_IPA_oths(self.root, True)

            file = OrderedDict() # from collections import OrderedDict
            
            if self.nums[0] > 0: 
                file.update({"Consonants": self.EXP_compose(conIpa)})
            if self.nums[1] > 0: 
                file.update({"Vowels": self.EXP_compose(vowIpa)})
            if self.nums[2] > 0: 
                file.update({"Other Symbols": self.EXP_compose(othIpa, True)})
            
            ods.save_data(f, file)
            f.close()
        except Exception as e:
            self.throw_err("#FE_UNKERR", e)
        
    def EXP_compose(self, ipa, other=False):
        sheet = []
        
        cols = []
        if not other: cols.append("")
        for c in ipa["top"]:
            cols.append(c)
            if not other: cols.append("--")
        sheet.append(cols)
        
        for i in range(len(ipa["side"])):
            row = []
            if not other: row.append(ipa["side"][i])
            for j in range(len(ipa["cells"][i])):
                s = ipa["cells"][i][j]
                if other and j % 2 == 0: continue
                if s is None: row.append("")
                else: row.append(s)
            sheet.append(row)
        
        return sheet
           
    def HELP_about(self):
        txt = """
Phonologiter
Version {}
Released {}
               
Created by Jenni Zimmerle
Written in Python 3.8.0 using the following PyPi packages:
    playsound v.1.2.2, pyexcel_ods3 v.0.6.0, pyglet v.1.5.11, 

Sounds sourced from Wikipedia
[https://commons.wikimedia.org/wiki/General_phonetics]
Sounds provided by Peter Isotalo, user:Adamsa123, user:Denelson83, and UCLA Phonetics Lab Archive 2003, and used under various copyleft licenses.
The specific licenses for each sound can be found by clicking on the sound in the link above.
              """
        txt = txt.format(VERSION, RELEASE)
        tkMess.showinfo(title="Phonologiter", message=txt)
           
    def create_mode(self):
        try:
            modeF = tk.Frame(self.root, bd=5)
            modeF.grid(column=0, row=0, sticky=tk.NE)
            
            self.modes.append(tk.Button(modeF, text="Full IPA Chart", width=14,
                                        relief=tk.SUNKEN,
                                        command= lambda: self.change_mode(0)))
            self.modes.append(tk.Button(modeF, text="Simple Chart", width=14,
                                        command= lambda: self.change_mode(1)))
            self.modes.append(tk.Button(modeF, text="Sound Test", width=14,
                                        command= lambda: self.change_mode(2)))
            self.modes[0].grid(column=0, row=0)
            self.modes[1].grid(column=0, row=1)
            self.modes[2].grid(column=0, row=4, pady=30)
        except Exception as e:
            self.throw_err("#UC_MODERR", e)
    
    def create_screen(self):
        try:
            screenF = tk.Frame(self.root, bd=3, relief=tk.SUNKEN, padx=2,
                               pady=2, width=674, height=255)
            screenF.grid_propagate(0)
            screenF.grid(column=1, row=0, padx=5, pady=5, sticky=tk.SW)
            
            self.ipaCon = tk.Frame(screenF)
            self.create_IPA_cons(self.ipaCon)
            self.ipaVow = tk.Frame(screenF)
            self.create_IPA_vows(self.ipaVow)
            self.ipaOth = tk.Frame(screenF)
            self.create_IPA_oths(self.ipaOth)
            
            self.simCon = tk.Frame(screenF)
            self.manifest_IPA_cons(self.simCon)
            self.simVow = tk.Frame(screenF)
            self.manifest_IPA_vows(self.simVow)
            self.simOth = tk.Frame(screenF)
            self.manifest_IPA_oths(self.simOth)
            
            self.testCon = tk.Frame(screenF)
            self.test_IPA_cons(self.testCon)
            self.testVow = tk.Frame(screenF)
            self.test_IPA_vows(self.testVow)
            self.testOth = tk.Frame(screenF)
            self.test_IPA_oths(self.testOth)
            
            screenF.grid_rowconfigure(0, weight=1)
            screenF.grid_columnconfigure(0, weight=1)
            
            self.ipaScreen = screenF
            
            self.fix_screens()
        except Exception as e:
            self.throw_err("#UC_SCREENERR", e)

    def create_IPA(self, parent, top_row, side_row, label=True, fakey=False,
                   mom=-1):
        try:
            col = []
            for i in range(len(top_row)):
                if fakey: col.append(top_row[i])
                else:
                    col.append(tk.Label(parent, text=top_row[i]))
                    col[i].grid(column=(i * 2) + 1, row=0, columnspan=2)
            
            row = []
            for i in range(len(side_row)):
                t = side_row[i] if label else ""
                if fakey: row.append(t)
                else:
                    row.append(tk.Label(parent, text=t, pady=3))
                    row[i].grid(column=0, row=i + 1, sticky=tk.E)
                
            symbs = []
            for i in range(len(side_row)):
                symbs.append([])
                for j in range(len(top_row) * 2):
                    symbs[i].append(None)
            
            ret = {"col":col, "row":row, "symbs":symbs, "top":top_row,
                   "side":side_row}
            return ret
        except Exception as e:
            self.throw_err("#UR_IPA"+str(mom)+"ERR", e)

    def create_IPA_cons(self, parent):
        ipa = self.create_IPA(parent, IPA_Place.copy(), IPA_Manner.copy(),
                              mom=0)
        
        self.cellCon = self.create_full_IPA(parent, ipa["symbs"], 0, mom=0)

    def create_IPA_vows(self, parent):
        ipa = self.create_IPA(parent, IPA_Backness.copy(), IPA_Height.copy(),
                              mom=1)
        
        self.cellVow = self.create_full_IPA(parent, ipa["symbs"], 1, mom=1)

    def create_IPA_oths(self, parent):
        ipa = self.create_IPA(parent, IPA_Type.copy(), IPA_i.copy(), False,
                              mom=2)
    
        self.cellOth = self.create_full_IPA(parent, ipa["symbs"], 2, mom=2)

    def create_full_IPA(self, parent, cells, type, subtype=None, test=False,
                        mom=-1):
        try:
            if subtype is None: subtype = type
            for s in IPA.values():
                if s.type != type and s.type != subtype: continue
                f = tk.Frame(parent)
                c = ["#009", "#666"]
                if test: c = ["#00F", "#000"]
                l = tk.Label(f, text=s.symb, state=tk.DISABLED,
                             fg=c[0], disabledforeground=c[1],
                             cursor="hand2", font=("Noto Sans", 12)
                             )
                if not test:
                    l.config(compound=tk.BOTTOM)   # Store state of Symb
                    l.bind("<Button-1>", self.add_IPA)
                else:
                    l.bind("<Button-1>", self.play_IPA)
                l.bind("<Enter>", lambda e: self.change_IPA(e, True))
                l.bind("<Leave>", lambda e: self.change_IPA(e, False))
                l.grid()
                f.grid(column=s.col() + 1, row=s.row() + 1, sticky=s.anc())
                cells[s.row()][s.col()] = f
            
            return cells
        except Exception as e:
            self.throw_err("#UR_FULL" + str(mom) + "ERR", e)
        
    def create_simp_IPA(self, parent, ipa, type, symbs, fakey=False, mom=-1):
        try:
            cells = ipa["symbs"]
            top = ipa["top"]
            side = ipa["side"]
            for s in symbs.values():
                if s.type != type: continue
                if fakey:
                    cells[s.row(side)][s.col(top)] = s.symb
                else:
                    f = tk.Frame(parent)
                    l = tk.Label(f, text=s.symb,
                                 fg="#000", font=("Noto Sans", 12)
                                 )
                    l.grid()
                    f.grid(column=s.col(top) + 1, row=s.row(side) + 1, sticky=s.anc())
                    cells[s.row(side)][s.col(top)] = f
            
            return {"top":top, "side":side, "cells":cells}
        except Exception as e:
            self.throw_err("#UR_SIM" + str(mom) + "ERR", e)

    def manifest_IPA_cons(self, parent, fakey=False):
        ipa = self.manifest_IPA(parent, 0, 3, fakey, mom=0)
        sipa = self.create_simp_IPA(parent, ipa["ipa"], 0, ipa["symbs"], fakey,
                                    mom=0)
        return sipa
        
    def manifest_IPA_vows(self, parent, fakey=False):
        ipa = self.manifest_IPA(parent, 1, fakey=fakey, mom=1)
        sipa = self.create_simp_IPA(parent, ipa["ipa"], 1, ipa["symbs"], fakey,
                                    mom=1)
        return sipa
        
    def manifest_IPA_oths(self, parent, fakey=False):
        ipa = self.manifest_IPA(parent, 2, fakey=fakey, mom=2)
        sipa = self.create_simp_IPA(parent, ipa["ipa"], 2, ipa["symbs"], fakey,
                                    mom=2)
        return sipa
        
    def manifest_IPA(self, parent, type, subtype=None, fakey=False, mom=-1):
        try:
            if subtype is None: subtype = type
        
            top_row = []
            side_row = []
            symbols = {}
            
            voices = {}
            
            post_sort = []
            
            for i in self.IPA_sel:
                s = IPA[i]
                
                if s.type != type:
                    if s.type != subtype: continue
                    # Other Consonants
                    s = deepcopy(IPA_Other[i])
                    if s.c in voices and s.r in voices[s.c]:
                        if s.voice in voices[s.c][s.r]:
                            post_sort.append(s)
                            continue
                    
                if not s.c in top_row: top_row.append(s.c)
                if not s.r in side_row: side_row.append(s.r)
                symbols[s.symb] = s
                
                if not s.c in voices: voices[s.c] = {}
                if not s.r in voices: voices[s.c][s.r] = []
                voices[s.c][s.r].append(s.voice)
            
            
            top_row = sort_IPA(top_row, type, False)
            side_row = sort_IPA(side_row, type, True)
                
            for s in post_sort:
                if not s.c in top_row: top_row.append(s.c)
                if not s.r in side_row: side_row.append(s.r)
                else:
                    side_row.insert(side_row.index(s.r) + 1, s.r + "(2)")
                    s.r += "(2)"
                symbols[s.symb] = s
                
            ipa = self.create_IPA(parent, top_row, side_row,
                                  False if type == 2 else True, fakey,
                                  mom=mom+10)
                   
            ret = {"ipa":ipa, "symbs":symbols}
            return ret
        except Exception as e:
            self.throw_err("#UR_MANI"+mom+"ERR", e)

    def test_IPA_cons(self, parent):
        ipa = self.create_IPA(parent, IPA_Place.copy(), IPA_Manner.copy(),
                              mom=20)
        
        self.create_full_IPA(parent, ipa["symbs"], 0, test=True, mom=20)
    
    def test_IPA_vows(self, parent):
        ipa = self.create_IPA(parent, IPA_Backness.copy(), IPA_Height.copy(),
                              mom=21)
        
        self.create_full_IPA(parent, ipa["symbs"], 1, test=True, mom=21)
        
    def test_IPA_oths(self, parent):
        ipa = self.create_IPA(parent, IPA_Type.copy(), IPA_i.copy(), False,
                              mom=22)
        
        self.create_full_IPA(parent, ipa["symbs"], 2, test=True, mom=22)

    def change_IPA(self, event, activate):
        try:
            if activate: event.widget.config(state=tk.NORMAL)
            else: event.widget.config(state=tk.DISABLED)
        except Exception as e:
            try:
                self.throw_err("#UR_CIPA"+event.widget["text"]+"ERR", e)
            except Exception as f:
                self.throw_err("#IN_CIPAERR", e, f)

    def add_IPA(self, event):
        try:
            if not self.changed:
                self.changed = True
                self.root.title(self.root.title() + "*")
            if event.widget["compound"] == tk.BOTTOM:
                event.widget.config(compound=tk.TOP)
                event.widget.config(fg="#66F")
                event.widget.config(disabledforeground="#00F")
                self.IPA_sel.append(event.widget["text"])
                t = IPA[event.widget["text"]].type
                self.nums[t] += 1
            else:
                event.widget.config(compound=tk.BOTTOM)
                event.widget.config(fg="#009")
                event.widget.config(disabledforeground="#666")
                self.IPA_sel.remove(event.widget["text"])
                t = IPA[event.widget["text"]].type
                self.nums[t] -= 1
                if (self.nums[t] < 0): self.nums[t] = 0
        except Exception as e:
            try:
                self.throw_err("#UR_AIPA"+event.widget["text"]+"ERR", e)
            except Exception as f:
                self.throw_err("#IN_AIPAERR", e, f)

    def play_IPA(self, event):
        try:
            ipa = IPA[event.widget["text"]]
            file = "assets/" + ipa.id() + ".wav"
            
            playsound(file, False)
        except Exception as e:
            try:
                self.throw_err("#UR_PIPA" + event.widget["text"] + "ERR", e)
            except Exception as f:
                self.throw_err("#IN_PIPAERR", e, f)
        
    def create_page(self):
        try:
            pageF = tk.Frame(self.root, bd=5)
            pageF.grid(column=1, row=1, sticky=tk.NW)
            
            self.pages.append(tk.Button(pageF, text="Consonants",
                                        relief=tk.SUNKEN,
                                        command= lambda: self.change_page(0)))
            self.pages.append(tk.Button(pageF, text="Vowels",
                                        command= lambda: self.change_page(1)))
            self.pages.append(tk.Button(pageF, text="Other Symbols",
                                        command= lambda: self.change_page(2)))
            self.pages[0].grid(column=0, row=0)
            self.pages[1].grid(column=1, row=0)
            self.pages[2].grid(column=2, row=0)
        except Exception as e:
            self.throw_err("#UC_PAGERR", e)
         
    def change_mode(self, mode, fakey=False):
        try:
            self.mode = mode
            for i in range(3):
                r = tk.RAISED if i != mode else tk.SUNKEN
                self.modes[i].configure(relief=r)
                
            if not fakey: self.update_SIM()
        except Exception as e:
            self.throw_err("#UR_MODERR", e)
        
    def change_page(self, page, fakey=False):
        try:
            self.page = page
            for i in range(3):
                r = tk.RAISED if i != page else tk.SUNKEN
                self.pages[i].configure(relief=r)
                
            if not fakey: self.fix_screens()
        except Exception as e:
            self.throw_err("#UR_PAGERR", e)
            
    def fix_screens(self):
        try:
            self.ipaCon.grid_forget()
            self.ipaVow.grid_forget()
            self.ipaOth.grid_forget()
            self.simCon.grid_forget()
            self.simVow.grid_forget()
            self.simOth.grid_forget()
            self.testCon.grid_forget()
            self.testVow.grid_forget()
            self.testOth.grid_forget()
            
            stick = tk.N+tk.S+tk.E+tk.W
            
            if self.mode == 0:
                if self.page == 0: self.ipaCon.grid(sticky=stick)
                if self.page == 1: self.ipaVow.grid(sticky=stick)
                if self.page == 2: self.ipaOth.grid(sticky=stick)
                
                self.pages[0].configure(state=tk.ACTIVE)
                self.pages[1].configure(state=tk.ACTIVE)
                self.pages[2].configure(state=tk.ACTIVE)
            if self.mode == 1:
                if self.page == 0: self.simCon.grid(sticky=stick)
                if self.page == 1: self.simVow.grid(sticky=stick)
                if self.page == 2: self.simOth.grid(sticky=stick)
                
                if self.nums[0] == 0: self.pages[0].configure(state=tk.DISABLED)
                if self.nums[1] == 0: self.pages[1].configure(state=tk.DISABLED)
                if self.nums[2] == 0: self.pages[2].configure(state=tk.DISABLED)
            if self.mode == 2:
                if self.page == 0: self.testCon.grid(sticky=stick)
                if self.page == 1: self.testVow.grid(sticky=stick)
                if self.page == 2: self.testOth.grid(sticky=stick)
                
                self.pages[0].configure(state=tk.ACTIVE)
                self.pages[1].configure(state=tk.ACTIVE)
                self.pages[2].configure(state=tk.ACTIVE)
        except Exception as e:
            self.throw_err("#UR_FIXERR", e)
            
    def update_SIM(self):
        try:
            self.simCon.grid_forget()
            self.simVow.grid_forget()
            self.simOth.grid_forget()
        
            self.simCon = tk.Frame(self.ipaScreen)
            self.simVow = tk.Frame(self.ipaScreen)
            self.simOth = tk.Frame(self.ipaScreen)
            
            self.fix_screens()
            
            self.manifest_IPA_cons(self.simCon)
            self.manifest_IPA_vows(self.simVow)
            self.manifest_IPA_oths(self.simOth)
            
            self.ipaScreen.grid_rowconfigure(0, weight=1)
            self.ipaScreen.grid_columnconfigure(0, weight=1)
            
            self.check_nums()
        except Exception as e:
            self.throw_err("#UR_UPERR", e)
        
    def check_nums(self):
        try:
            tnum = [0, 0, 0]
            for s in self.IPA_sel: tnum[IPA[s].type] += 1
            if any([self.nums[x] != tnum[x] for x in range(3)]):
                self.changed = True
            self.nums = tnum
        except Exception as e:
            self.throw_err("#UR_NUMERR", e)


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    phono = Phono(parent=root)
    phono.mainloop()
