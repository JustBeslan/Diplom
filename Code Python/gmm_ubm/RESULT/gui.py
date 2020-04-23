from RESULT.MainProcessing import Main_Processing
from tkinter.filedialog import *
from threading import Thread

global main_processing


class NewThread(Thread):
    def __init__(self, path=None, name=None, id_thread=None,
                 path_train=None, interval_presenter=None, is_presenter=None):
        Thread.__init__(self)
        self.id = id_thread
        if self.id == 1:
            self.path_video = path
            self.name_video = name
        if self.id == 2:
            self.path_train = path_train
            self.is_presenter = is_presenter
        if self.id == 3:
            self.path_train = path_train
            self.interval_presenter = interval_presenter
            self.is_presenter = is_presenter

    def run(self):
        global main_processing
        if self.id == 1:
            main_processing = Main_Processing(self.path_video, self.name_video, messages)
            messages.insert(END, 'Нажмите "Далее"\n')
        if self.id == 2:
            main_processing.createClassificator(path_train=self.path_train, is_presenter=self.is_presenter)
        if self.id == 3:
            main_processing.createClassificator(interval_presenter=self.interval_presenter,path_train=self.path_train,
                                                is_presenter=self.is_presenter)
        if self.id == 4:
            audio_data = main_processing.audioProcessing
            audio_data.extract_not_presenter(audio_data.filteredPartsData)


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
        editWithPathVideo.pack(side=LEFT, padx=5, pady=5)
        changeDirButton = Button(frame1, text="Выбрать", command=lambda: self.get_path(editWithPathVideo))
        changeDirButton.pack(side=LEFT, padx=5, pady=5)
        frame1.pack(fill=X, padx=5, pady=5)

        frame2 = Frame(self)
        loadVideoButton = Button(frame2, text="Загрузить видео",
                                 command=lambda: self.load_video(editWithPathVideo, loadVideoButton))
        loadVideoButton.pack(padx=5, pady=5)
        frame2.pack(fill=X, padx=5, pady=5)


class Window2(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.pack(padx=5, pady=5)

    def get_path(self, edit):
        edit.delete(0, 100)
        edit.insert(0, askdirectory()+"/")

    def train_presenter(self, start, end):
        start = str(start.get())
        end = str(end.get())
        interval = [int(start), int(end)]
        NewThread(id_thread=3, interval_presenter=interval, path_train=askdirectory()+"/", is_presenter=True).start()

    def train_not_presenter(self, path_train):
        path_train = str(path_train.get())
        NewThread(id_thread=2, path_train=path_train, is_presenter=False).start()

    def extract_not_presenter(self):
        NewThread(id_thread=4).start()

    def initUI(self):

        frame1 = LabelFrame(self, text="Presenter")
        start_time = Label(frame1, text=" От(в мс) ")
        start_time.grid(column=0, row=0)
        edit_start_time = Entry(frame1, width=10)
        edit_start_time.grid(column=1, row=0)
        end_time = Label(frame1, text=" До(в мс) ")
        end_time.grid(column=2, row=0)
        edit_end_time = Entry(frame1, width=10)
        edit_end_time.grid(column=3, row=0)
        trainPresenterButton = Button(frame1, text="Тренировать",
                                      command=lambda: self.train_presenter(edit_start_time, edit_end_time))
        trainPresenterButton.grid(column=4, row=0, columnspan=2, padx=10, pady=5)
        frame1.pack(padx=5, pady=5)

        frame2 = LabelFrame(self, text="Not Presenter")
        editWithPathTrain = Entry(frame2, width=50)
        editWithPathTrain.insert(0, "Укажите путь к тренировочным данным... ")
        editWithPathTrain.grid(column=0, row=0, columnspan=3)
        changeDirButton = Button(frame2, text="Выбрать", command=lambda: self.get_path(editWithPathTrain))
        changeDirButton.grid(column=3, row=0, padx=5)
        trainNotPresenterButton = Button(frame2, text="Тренировать", command=lambda: self.train_not_presenter(editWithPathTrain))
        trainNotPresenterButton.grid(column=1, row=1, columnspan=2, pady=5)
        frame2.pack(fill=X, padx=5, pady=5)

        classificationButton.place(x=10, y=270)
        classificationButton["command"] = lambda: self.extract_not_presenter()


def next_window(pwindow):
    global window
    pwindow[1].pack_forget()
    messages.delete(1.0, END)
    if int(window[0]) == 1:
        window2 = Window2(mainWindow)
        window = (2, window2)


mainWindow = Tk()
mainWindow.title("Анализ вебинаров")
mainWindow.geometry("400x300")
mainWindow.resizable(0, 0)
window1 = Window1(mainWindow)
global window
window = (1, window1)

global messages
messages = Text(mainWindow)
messages.place(x=10, y=165, width=380, height=100)

nextButton = Button(mainWindow, text="Далее", command=lambda: next_window(window))
nextButton.place(x=280, y=270, width=100)

classificationButton = Button(mainWindow, text="Выделить данные")

mainWindow.mainloop()
