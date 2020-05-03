from tkinter import Frame, messagebox, END, LabelFrame, Label, Entry, Button, X, Listbox


class windowInputManually(Frame):
    intervals_not_presenter = []

    def __init__(self, parent, intervals_voices, messages):
        Frame.__init__(self, parent)
        self.parent = parent
        self.intervals_voices = intervals_voices
        self.messages = messages

    def createWindow(self):
        self.initUI()
        self.pack(padx=5,
                  pady=5)

    def deleteInterval(self, list_intervals):
        if list_intervals.curselection() != ():
            list_intervals.delete(list_intervals.curselection())
        else:
            messagebox.showwarning(message='Выберите удаляемый интервал!!!')

    def deleteAllIntervals(self, list_intervals):
        list_intervals.delete(0, END)

    def isSubInterval(self, interval, intervals):
        for interval1 in intervals:
            if interval[0] >= interval1[0] and interval[1] <= interval1[1]:
                return True
        return False

    def addInterval(self, list_intervals, edit_start_time, edit_end_time):
        start_time = str(edit_start_time.get())
        end_time = str(edit_end_time.get())
        if (start_time.isdigit() or end_time.isdigit()) and int(end_time) > int(start_time):
            if self.isSubInterval(interval=[int(start_time), int(end_time)],
                                  intervals=self.intervals_voices):
                list_intervals.insert(END, str(str(start_time) + ' - ' + str(end_time)))
                edit_start_time.delete(0, END)
                edit_end_time.delete(0, END)
            else:
                messagebox.showwarning(message='Ваш интервал попадает не лежит в рамках интервалов голосов!!!')
        else:
            messagebox.showwarning(message='Введите интервал корректно!!!')

    def saveIntervals(self, list_intervals):
        intervals = list_intervals.get(0, END)
        intervals = [[int(str(interval).split(' - ')[0]), int(str(interval).split(' - ')[1])]
                     for interval in intervals]
        self.intervals_not_presenter = intervals
        messagebox.showinfo(message='Интервалы успешно сохранены!\nЗакройте окно руччного ввода и нажмите "Далее"!')
        self.parent.destroy()

    def addAllIntervals(self, list_intervals, list_intervals_voices):
        for interval in list_intervals_voices.get(0, END):
            interval = str(interval).split(' - ')
            list_intervals.insert(END, str(interval[0] + ' - ' + str(interval[1])))

    def getSelectedInterval(self, event):
        widget = event.widget
        selection = widget.curselection()
        picked = widget.get(selection)
        interval = str(picked).split(' - ')
        self.edit_start_time.delete(0, END)
        self.edit_start_time.insert(0, interval[0])
        self.edit_end_time.delete(0, END)
        self.edit_end_time.insert(END, interval[1])

    def initUI(self):
        frame1 = LabelFrame(master=self,
                            text='Интервал')
        start_time = Label(master=frame1,
                           text=" От(в мс) ")
        start_time.grid(column=0,
                        row=0)
        self.edit_start_time = Entry(master=frame1,
                                     width=10)
        self.edit_start_time.grid(column=1,
                                  row=0)
        end_time = Label(master=frame1,
                         text=" До(в мс) ")
        end_time.grid(column=2,
                      row=0)
        self.edit_end_time = Entry(master=frame1,
                                   width=10)
        self.edit_end_time.grid(column=3,
                                row=0)
        self.add_button = Button(master=frame1,
                                 text='Добавить',
                                 command=lambda: self.addInterval(list_intervals=self.list_intervals,
                                                                  edit_start_time=self.edit_start_time,
                                                                  edit_end_time=self.edit_end_time))
        self.add_button.grid(column=4,
                             row=0,
                             padx=5)
        frame1.pack(fill=X,
                    padx=5,
                    pady=5)

        frame2 = Frame(master=self)
        self.frame2_1 = LabelFrame(master=frame2,
                                   text='Ваши интервалы голосов НЕ ведущего')
        self.list_intervals = Listbox(master=self.frame2_1,
                                      width=30,
                                      height=10)
        self.list_intervals.pack()
        self.frame2_1.grid(column=0,
                           row=0,
                           columnspan=2,
                           padx=5,
                           pady=5)
        delete_button = Button(master=frame2,
                               text='Удалить',
                               command=lambda: self.deleteInterval(self.list_intervals))
        delete_button.grid(column=0,
                           row=2,
                           padx=5)
        delete_all_button = Button(master=frame2,
                                   text='Очистить всё',
                                   command=lambda: self.deleteAllIntervals(self.list_intervals))
        delete_all_button.grid(column=1,
                               row=2,
                               padx=5)
        save_button = Button(master=frame2,
                             text='Сохранить',
                             command=lambda: self.saveIntervals(self.list_intervals))
        save_button.grid(column=2,
                         row=2,
                         padx=10)
        self.frame2_2 = LabelFrame(master=frame2,
                                   text='Выделенные интервалы голосов')
        self.list_intervals_voices = Listbox(master=self.frame2_2,
                                             width=30,
                                             height=10)
        self.list_intervals_voices.bind('<<ListboxSelect>>', self.getSelectedInterval)
        self.list_intervals_voices.pack()
        self.frame2_2.grid(column=2,
                           row=0,
                           columnspan=2,
                           padx=5,
                           pady=5)
        self.add_all_button = Button(master=frame2,
                                     text='Добавить все',
                                     command=lambda: self.addAllIntervals(list_intervals=self.list_intervals,
                                                                          list_intervals_voices=self.list_intervals_voices))
        self.add_all_button.grid(column=3,
                                 row=2,
                                 padx=10)
        frame2.pack(fill=X,
                    padx=5,
                    pady=5)
        for interval in self.intervals_voices:
            self.list_intervals_voices.insert(END, str(interval[0]) + ' - ' + str(interval[1]) + '\n')
