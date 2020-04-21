from RESULT.MainProcessing import Main_Processing
from tkinter.filedialog import *

mainWindow = Tk()
mainWindow.title("Анализ вебинаров")
mainWindow.geometry("400x300")
mainWindow.resizable(0, 0)

editWithPathVideo = Entry(width=30)
editWithPathVideo.insert(0, "Укажите путь к вебинару... ")
editWithPathVideo.place(x=10, y=10, width=310, height=30)


def get_path():
    editWithPathVideo.delete(0, 100)
    editWithPathVideo.insert(0, askopenfilename())


changeDirButton = Button(mainWindow, text="Выбрать", command=get_path)
changeDirButton.place(x=330, y=10)

message = Label(mainWindow)
message.place(x=110, y=50)


def load_video():
    text = str(editWithPathVideo.get())
    name_video = text.split("/")[-1]
    path_video = text.split(name_video)[0]
    if os.path.exists(path_video):
        message["text"] = "Видео загружается..."
        main_Processing = Main_Processing(path_video, name_video, message)
    else:
        message["text"] = "Некорректный путь!!!"


loadVideoButton = Button(mainWindow, text="Загрузить видео", command=load_video)
loadVideoButton.place(x=10, y=50)

mainWindow.mainloop()
