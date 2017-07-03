import tkinter

class GuiTK(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent

    def initialGUI(self):
        self.grid()

        self.entryVariable = tkinter.StringVar()
        self.entry = tkinter.Entry(self, textvariable = self.entryVariable)
        self.entry.grid(column = 0, row = 0, sticky = 'EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here")

        button     = tkinter.Button(self, text = u'Test',
                                    command = self.OnButtonClick)
        button.grid(column = 1, row = 0)

        self.labelVariable = tkinter.StringVar()
        label      = tkinter.Label(self, textvariable = self.labelVariable,
                                   anchor = 'w', fg = 'white', bg = 'blue')
        label.grid(column = 0, row = 1, columnspan = 2, sticky = 'EW')
        self.labelVariable.set(u"Hello !")

        self.grid_columnconfigure(0, weight = 1)
        self.resizable(True, False)

        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

        # self.update()
        # self.geometry(self.geometry())
    def OnButtonClick(self):
        self.labelVariable.set(self.entryVariable.get()+" (You clicked the button)")
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

    def OnPressEnter(self):
        self.labelVariable.set(self.entryVariable.get()+" (You entered the button)")
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

if __name__ == '__main__':
    myApp = GuiTK(None)
    myApp.title('General Tool Apps')
    myApp.initialGUI()
    myApp.mainloop()
