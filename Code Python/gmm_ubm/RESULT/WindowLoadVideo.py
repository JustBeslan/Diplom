import os
from threading import Thread
from tkinter import Frame, END, Entry, LEFT, Button, X
from tkinter.filedialog import askopenfilename
from RESULT.MainProcessing import Main_Processing


class NewThread(Thread):
    def __init__(self, main_processing=None, messages=None):
        Thread.__init__(self, daemon=True)
        self.main_processing = main_processing
        self.messages = messages

    def run(self):
        self.main_processing.audioProcessing.filtering_audio()
        filtered_data_audio = self.main_processing.audioProcessing.filtered_data_audio
        sr = self.main_processing.audioProcessing.SR
        self.main_processing.audioProcessing.ExtractVoices(filtered_data_audio, sr)

        self.messages.insert(END, 'Выберите режим работы и нажмите "Далее"\n')


class WindowLoadVideo(Frame):
    main_processing = None

    def __init__(self, parent, messages):
        Frame.__init__(self, parent)
        self.parent = parent
        self.messages = messages
        self.initUI()
        self.pack(padx=5,
                  pady=5)

    def get_path(self, edit):
        edit.delete(0, 100)
        edit.insert(0, askopenfilename())

    def threadLoadVideo(self, path_video, name_video):
        self.messages.insert(END, "Видео загружается...\n")
        self.main_processing = Main_Processing(pathVideo=path_video,
                                               nameVideo=name_video,
                                               messages=self.messages)

    def load_video(self, editWithPathVideo, loadVideoButton):
        text = str(editWithPathVideo.get())
        name_video = text.split("/")[-1]
        path_video = text.split(name_video)[0]
        if os.path.exists(path_video):
            Thread(target=lambda: self.threadLoadVideo(path_video=path_video,
                                                       name_video=name_video)).start()
            loadVideoButton["state"] = "disabled"
        else:
            self.messages.insert(END, "Некорректный путь!!!\n")

    def audioProcessing1(self):
        newThread1 = NewThread(main_processing=self.main_processing,
                               messages=self.messages)
        newThread1.start()

    def initUI(self):
        frame1 = Frame(self)
        editWithPathVideo = Entry(master=frame1,
                                  width=50)
        editWithPathVideo.insert(0, "Укажите путь к вебинару... ")
        editWithPathVideo.pack(side=LEFT,
                               padx=5,
                               pady=10)
        changeDirButton = Button(master=frame1,
                                 text="Выбрать",
                                 command=lambda: self.get_path(editWithPathVideo))
        changeDirButton.pack(side=LEFT,
                             padx=5,
                             pady=10)
        frame1.pack(fill=X,
                    padx=5,
                    pady=5)

        frame2 = Frame(self)
        loadVideoButton = Button(master=frame2,
                                 text="Загрузить видео",
                                 command=lambda: self.load_video(editWithPathVideo, loadVideoButton))
        loadVideoButton.pack(padx=5,
                             pady=5)
        frame2.pack(fill=X,
                    padx=5,
                    pady=5)
