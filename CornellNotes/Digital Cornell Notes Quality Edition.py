from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pickle
import sys

class Page(Tk):

    def __init__(self):

        super().__init__()
        
        #Program set-up
        self.title("PyNotes - Unnamed.note")
        self.working_filename = "Unnamed.note"
        self.saved = False
        self.bind("<Control-s>", self.save)
        self.bind("<Control-o>", self.load)

        #Name entry
        self.Name = Entry(self)
        self.Name.insert(0,"Name")
        #Subject entry
        self.Subject = Entry(self)
        self.Subject.insert(0,"Subject")
        #Date entry
        self.Date = Entry(self)
        self.Date.insert(0,"Date")

        #Keywords text
        self.Keywords = Text(self, height=26, width=20, wrap=WORD)

        #Description text
        self.Description = Text(self, height=26,width=40, wrap=WORD)

        #Synchronized scroll setup
        def sync_scroll(*args):
            self.Keywords.yview(*args)
            self.Description.yview(*args)

        #Note scrollbar
        self.Scrollbar = Scrollbar(self, orient='vertical', command=sync_scroll)

        #Summary text
        self.Summary = Text(self, height=8, width=60, wrap=WORD)

        #File manager buttons
        self.Menu = Button(self, text="File", width=60, command=self.open_menu)


        #Page assembly
        self.Name.grid(row=0,column=0, sticky=NW); self.Date.grid(row=0, column=1, columnspan=2, sticky=NE)
        self.Subject.grid(row=1,column=0, sticky=NW)

        self.Keywords.grid(row=2,column=0, sticky=EW); self.Description.grid(row=2, column=1, sticky=EW); self.Scrollbar.grid(row=2,column=2,sticky=NS)
        
        self.Summary.grid(row=3,columnspan=3, sticky=EW)

        self.Menu.grid(row=4,columnspan=3, sticky=EW)

    def open_menu(self):
        """Function to open the file menu."""
        
        file_menu = Toplevel(self)
        self.Save = Button(file_menu, text="Save", width=20, command=self.save)
        self.Save_as = Button(file_menu, text="Save As", width=20, command=self.save_as)
        self.Load = Button(file_menu, text="Open", width=20, command=self.load)
        self.Save.pack()
        self.Save_as.pack()
        self.Load.pack()
        file_menu.mainloop()
        
    def save(self, *args):
        """General function to initiate saving process."""
        
        if not self.saved:
            self.save_as()
        else:
            self.save_filename(self.working_filename)

    def save_as(self):
        """Saving function that opens a file dialog."""
        
        filename = asksaveasfilename()
        if filename != '': #Only save if file name is chosen
            if filename[-5:] != ".note": #If filename is not properly formatted
                if '.' in filename: #Check to see if another file format has been specified
                    filename = filename.split('.')[0]+'.note' #Overwrite improper file format with .note
                else: #If a plain name has been given instead
                    filename += '.note' #Add the file format specifier onto the end
            self.save_filename(filename)
            self.update_filename(filename)#Only update filename on successful save
    
    def save_filename(self, filename):
        """Saving function that takes a file name and deposits all entered information into the file."""
        
        self.saved = True
        
        data = [self.Name.get(), self.Subject.get(), self.Date.get(), self.Keywords.get("1.0","end-1c"), self.Description.get('1.0','end-1c'),
                self.Summary.get('1.0','end-1c')]
        
        with open(filename, mode='wb') as f:

            pickle.dump(data, f)

    def load(self, *args):
        """General function to initiate loading process."""

        filename = askopenfilename()
        self.load_file(filename)
            
    def load_file(self, filename):
        
        with open(filename, mode='rb') as f:

            data = pickle.load(f)

            self.Name.delete(0,END)
            self.Subject.delete(0,END)
            self.Date.delete(0,END)
            self.Keywords.delete('1.0',END)
            self.Description.delete('1.0',END)
            self.Summary.delete('1.0',END)
            
            self.Name.insert(0,data[0])
            self.Subject.insert(0,data[1])
            self.Date.insert(0,data[2])
            self.Keywords.insert('1.0',data[3])
            self.Description.insert('1.0',data[4])
            self.Summary.insert('1.0',data[5])
            self.saved = True
        self.update_filename(filename) #Only set working filename on successful load
    
    def update_filename(self, filename):
        
        self.working_filename = filename
        self.title("PyNotes - " + filename)
    
        

main = Page()
if len(sys.argv)>1:
    main.load_file(sys.argv[1])
main.mainloop()

        
