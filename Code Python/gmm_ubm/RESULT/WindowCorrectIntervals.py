from threading import Thread
from tkinter import LabelFrame, Label, Entry, Button, X, END
from RESULT.WindowInputManually import windowInputManually


class CorrectIntervals(windowInputManually):
    def __init__(self, parent, intervals_voices, main_processing, messages):
        windowInputManually.__init__(self, parent, intervals_voices, messages)
        self.parent = parent
        self.intervals_voices = intervals_voices
        self.main_processing = main_processing
        self.messages = messages

        self.initUI2()
        self.frame2_1['text'] = 'Полученные интервалы голосов НЕ ведущего'
        self.add_button['text'] = 'Изменить'
        self.add_button['command'] = self.changeInterval
        self.pack(padx=5,
                  pady=5)

    def changeInterval(self):
        current_index = self.list_intervals.curselection()[0]
        self.list_intervals.delete(current_index)
        self.list_intervals.insert(current_index,
                                   str(self.edit_start_time.get()) + ' - ' + str(self.edit_end_time.get()))

    def getSelectedInterval(self, event):
        widget = event.widget
        selection = widget.curselection()
        picked = widget.get(selection)
        interval = str(picked).split(' - ')
        self.edit_start_time.delete(0, END)
        self.edit_start_time.insert(0, interval[0])
        self.edit_end_time.delete(0, END)
        self.edit_end_time.insert(END, interval[1])

    def getIntervals(self, start, end):
        interval_ms = [int(start), int(end)]

        self.messages.insert(END, 'Идет тренировка классификатора...\n')
        self.main_processing.GetIntervalsPresenter(interval_ms=interval_ms)
        self.messages.insert(END, 'Тренировка классификатора завершена\n')

        self.messages.insert(END, 'Идет разделение голосов на голос ведущего и остальных...\n')
        indexes_intervals_not_presenter = self.main_processing.classificator_presenter.Classification()
        self.intervals_not_presenter = [interval for i, interval in enumerate(self.intervals_voices)
                                        if i in indexes_intervals_not_presenter]
        self.messages.insert(END, 'Разделение голосов на голос ведущего и остальных завершено\n')
        for interval in self.intervals_not_presenter:
            self.list_intervals.insert(END, str(interval[0]) + ' - ' + str(interval[1]) + '\n')
        self.list_intervals.bind('<<ListboxSelect>>', self.getSelectedInterval)

    def initUI2(self):
        self.messages.insert(END, 'Введите любой интервал, в котором только голос ведущего(больше 2 секунд)\n')
        frame0 = LabelFrame(master=self,
                            text='Интервал голоса ведущего')
        start_time = Label(master=frame0,
                           text=" От(в мс) ")
        start_time.grid(column=0,
                        row=0)
        edit_start_time = Entry(master=frame0,
                                width=10)
        edit_start_time.grid(column=1,
                             row=0)
        end_time = Label(master=frame0,
                         text=" До(в мс) ")
        end_time.grid(column=2,
                      row=0)
        edit_end_time = Entry(master=frame0,
                              width=10)
        edit_end_time.grid(column=3,
                           row=0)
        train_button = Button(master=frame0,
                              text='Тренировать',
                              command=lambda: Thread(
                                  target=lambda: self.getIntervals(edit_start_time.get(), edit_end_time.get())
                              ).start())
        train_button.grid(column=4,
                          row=0,
                          padx=5)
        frame0.pack(fill=X,
                    padx=5,
                    pady=5)
        self.createWindow()
