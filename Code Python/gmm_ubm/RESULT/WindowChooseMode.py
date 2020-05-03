from tkinter import Frame, BooleanVar, LabelFrame, Radiobutton


class WindowChooseMode(Frame):
    def __init__(self, parent, messages):
        Frame.__init__(self, parent)
        self.messages = messages
        self.choose = BooleanVar()
        self.parent = parent
        self.initUI()
        self.pack(padx=5,
                  pady=5)

    def initUI(self):
        frame = LabelFrame(master=self,
                           text='Выберите режим работы')
        self.choose.set(0)
        manually_mode = Radiobutton(master=frame,
                                    text='Ручной режим',
                                    variable=self.choose,
                                    value=0)
        manually_mode.grid(column=1,
                           row=5)
        semiautomatic_mode = Radiobutton(master=frame,
                                         text='Полуавтоматический режим',
                                         variable=self.choose,
                                         value=1)
        semiautomatic_mode.grid(column=1,
                                row=7)
        frame.pack(padx=5,
                   pady=5)
