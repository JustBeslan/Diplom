from RESULT.MainProcessing import Main_Processing
from tkinter.filedialog import *
from threading import Thread
from RESULT.WindowInputManually import windowInputManually
from RESULT.WindowCorrectIntervals import CorrectIntervals

global main_processing
global window_correct_intervals


class NewThread(Thread):
    def __init__(self, path=None, name=None, id_thread=None,
                 interval_presenter=None, is_presenter=None):
        Thread.__init__(self)
        self.id = id_thread
        if self.id == 1:
            self.path_video = path
            self.name_video = name
        if self.id == 3:
            self.interval_presenter = interval_presenter
            self.is_presenter = is_presenter

    def run(self):
        global main_processing
        if self.id == 1:
            main_processing = Main_Processing(self.path_video, self.name_video, messages)
            global intervals_silence
            intervals_silence = main_processing.audioProcessing.intervals_silence
            global intervals_voices
            intervals_voices = main_processing.audioProcessing.corrected_intervals_voices
            messages.insert(END, 'Нажмите "Далее"\n')
        if self.id == 2:
            messages.insert(END, 'Идет обработка последовательности картинок...\n')
            main_processing.videoAnalyse(intervals_not_presenter)
            global intervals_together
            intervals_together = main_processing.videoProcessing.intervals_together
            global intervals_someone
            intervals_someone = main_processing.videoProcessing.intervals_someone
            messages.insert(END, 'Обработка последовательности картинок завершена...\n')
            messages.insert(END, 'Все интервалы времени сформированы...\n')
        if self.id == 3:
            messages.insert(END, 'Идет тренировка классификатора...\n')
            main_processing.GetIntervalsPresenter(self.interval_presenter)
            messages.insert(END, 'Тренировка классификатора завершена\n')

            messages.insert(END, 'Идет разделение голосов на голос ведущего и остальных...\n')
            indexes_intervals_presenter = main_processing.classificator_presenter.Classification()
            global intervals_presenter
            intervals_presenter = [interval for i, interval in enumerate(intervals_voices)
                                   if i in indexes_intervals_presenter]
            messages.insert(END, 'Разделение голосов на голос ведущего и остальных завершено\n')
            global window_correct_intervals
            window_correct_intervals = CorrectIntervals(window[1], intervals_voices, intervals_presenter)
            intervals_presenter = window_correct_intervals.intervals_presenter
            getIntervalsNotPresenter()
            print(intervals_voices)
            print(intervals_presenter)
            print(intervals_not_presenter)


class Window1(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.pack(padx=5, pady=5)

    def get_path(self, edit):
        edit.delete(0, 100)
        edit.insert(0, askopenfilename())

    def load_video(self, editWithPathVideo, loadVideoButton):
        text = str(editWithPathVideo.get())
        name_video = text.split("/")[-1]
        path_video = text.split(name_video)[0]
        if os.path.exists(path_video):
            messages.insert(END, "Видео загружается...\n")
            NewThread(path=path_video, name=name_video, id_thread=1).start()
            loadVideoButton["state"] = "disabled"
        else:
            messages.insert(END, "Некорректный путь!!!\n")

    def initUI(self):
        frame1 = Frame(self)
        editWithPathVideo = Entry(frame1, width=50)
        editWithPathVideo.insert(0, "Укажите путь к вебинару... ")
        editWithPathVideo.pack(side=LEFT, padx=5, pady=10)
        changeDirButton = Button(frame1, text="Выбрать", command=lambda: self.get_path(editWithPathVideo))
        changeDirButton.pack(side=LEFT, padx=5, pady=10)
        frame1.pack(fill=X, padx=5, pady=5)

        frame2 = Frame(self)
        loadVideoButton = Button(frame2, text="Загрузить видео",
                                 command=lambda: self.load_video(editWithPathVideo, loadVideoButton))
        loadVideoButton.pack(padx=5, pady=5)
        frame2.pack(fill=X, padx=5, pady=5)


class Window2(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.choose = BooleanVar()
        self.parent = parent
        self.initUI()
        self.pack(padx=5, pady=5)

    def initUI(self):
        frame = LabelFrame(self, text='Выберите режим работы')
        self.choose.set(0)
        manually_mode = Radiobutton(frame, text='Ручной режим', variable=self.choose, value=0)
        manually_mode.grid(column=1, row=5)
        semiautomatic_mode = Radiobutton(frame, text='Полуавтоматический режим', variable=self.choose, value=1)
        semiautomatic_mode.grid(column=1, row=7)
        frame.pack(padx=5, pady=5)
        messages.insert(END, 'После выбора режима работы нажмите "Далее"\n')


class SemiautomaticMode(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.pack(padx=5, pady=5)

    def initUI(self):
        messages.insert(END, 'Введите любой интервал, в котором только голос ведущего(больше 2 секунд)\n')
        frame0 = LabelFrame(self, text='Интервал голоса ведущего')
        start_time = Label(frame0, text=" От(в мс) ")
        start_time.grid(column=0, row=0)
        edit_start_time = Entry(frame0, width=10)
        edit_start_time.grid(column=1, row=0)
        end_time = Label(frame0, text=" До(в мс) ")
        end_time.grid(column=2, row=0)
        edit_end_time = Entry(frame0, width=10)
        edit_end_time.grid(column=3, row=0)
        add_button = Button(frame0, text='Тренировать',
                            command=lambda: self.correctIntervals(edit_start_time.get(), edit_end_time.get()))
        add_button.grid(column=4, row=0, padx=5)
        frame0.pack(fill=X, padx=5, pady=5)

    def correctIntervals(self, start, end):
        NewThread(id_thread=3, interval_presenter=[int(start), int(end)]).start()
        messages.insert(END, 'Откорректируйте полученные интервалы\n')


def getIntervalsNotPresenter():
    for interval_voice in intervals_voices:
        found_intervals = [interval_presenter for interval_presenter in intervals_presenter
                            if interval_presenter[0] >= interval_voice[0]
                           and interval_presenter[1] <= interval_voice[1]]
        if len(found_intervals) > 0:
            for i in range(len(found_intervals)):
                if i == 0 and interval_voice[0] < found_intervals[i][0]:
                    intervals_not_presenter.append([interval_voice[0], found_intervals[i][0]])
                if i == len(found_intervals) - 1 and found_intervals[i][1] < interval_voice[1]:
                    intervals_not_presenter.append([found_intervals[i][1], interval_voice[1]])
                if 0 < i <= len(found_intervals) - 1 and found_intervals[i - 1][1] < found_intervals[i][0]:
                    intervals_not_presenter.append([found_intervals[i - 1][1], found_intervals[i][0]])
        else:
            intervals_not_presenter.append(interval_voice)


def next_window(pwindow):
    global window
    pwindow[1].pack_forget()
    messages.delete(1.0, END)
    if int(window[0]) == 1:
        window2 = Window2(main_window)
        window = (2, window2)
    elif int(window[0]) == 2:
        main_window.geometry('500x500')
        main_window.update_idletasks()
        if window[1].choose.get() == 0:
            window3 = windowInputManually(main_window, intervals_voices, messages)
            global intervals_presenter
            intervals_presenter = window3.intervals_presenter
            getIntervalsNotPresenter()
        else:
            window3 = SemiautomaticMode(main_window)
        window = (3, window3)
        width_main_window, height_main_window = getMainWindowSize(main_window)
        messages.place(x=10, y=height_main_window - 150, width=width_main_window - 20, height=100)
        nextButton.place(x=width_main_window - 150, y=height_main_window - 30, width=100)
    elif int(window[0]) == 3:
        if len(intervals_not_presenter) > 0:
            NewThread(id_thread=2).start()


def getMainWindowSize(root):
    s = root.geometry()
    s = s.split('+')
    s = s[0].split('x')
    width_root = int(s[0])
    height_root = int(s[1])
    return width_root, height_root


global intervals_silence
intervals_silence = []
global intervals_voices
intervals_voices = []
global intervals_presenter
intervals_presenter = []
global intervals_not_presenter
intervals_not_presenter = []
global intervals_together
intervals_together = []
global intervals_someone
intervals_someone = []

main_window = Tk()
main_window.title("Анализ вебинаров")
main_window.geometry('400x300')
main_window.resizable(0, 0)
main_window.update_idletasks()

window1 = Window1(main_window)
global window
window = (1, window1)

width_main_window, height_main_window = getMainWindowSize(main_window)
global messages
messages = Text(main_window)
messages.place(x=10, y=height_main_window - 150, width=width_main_window-20, height=100)

nextButton = Button(main_window, text="Далее", command=lambda: next_window(window))
nextButton.place(x=width_main_window-150, y=height_main_window-30, width=100)

classificationButton = Button(main_window, text="Выделить данные")
inputManuallyButton = Button(main_window, text='Ввести вручную')

main_window.mainloop()
