from tkinter import *
from RESULT.WindowLoadVideo import WindowLoadVideo
from RESULT.WindowChooseMode import WindowChooseMode
from RESULT.WindowInputManually import windowInputManually
from RESULT.OtherProcessing import extractOtherIntervals
from RESULT.WindowCorrectIntervals import CorrectIntervals

global current_window, main_processing
global intervals_silence, intervals_voices, intervals_presenter
global intervals_not_presenter, intervals_together, intervals_someone


def getMainWindowSize(root):
    s = root.geometry()
    s = s.split('+')
    s = s[0].split('x')
    width_root = int(s[0])
    height_root = int(s[1])
    return width_root, height_root


def manageWindows(main_window, messages):
    global current_window, main_processing
    global intervals_silence, intervals_voices, intervals_presenter
    global intervals_not_presenter, intervals_together, intervals_someone
    if current_window[0] == 1:
        current_window[1].audioProcessing1()
        main_processing = current_window[1].main_processing
        intervals_voices = main_processing.audioProcessing.corrected_intervals_voices
        intervals_silence = main_processing.audioProcessing.intervals_silence
        current_window[1].pack_forget()
        messages.delete(1.0, END)
        current_window = [2, WindowChooseMode(parent=main_window,
                                              messages=messages)]
    elif current_window[0] == 2:
        messages.delete(1.0, END)
        child_window = Toplevel(master=main_window)
        child_window.title = 'Ручная настройка интервалов'
        child_window.focus_set()
        intervals_voices = main_processing.audioProcessing.corrected_intervals_voices
        if current_window[1].choose.get() == 0:
            window3 = windowInputManually(parent=child_window,
                                          intervals_voices=intervals_voices,
                                          messages=messages)
            window3.createWindow()
        else:
            window3 = CorrectIntervals(parent=child_window,
                                       intervals_voices=intervals_voices,
                                       main_processing=main_processing,
                                       messages=messages)
        current_window = [3, window3]
        child_window.mainloop()
    elif current_window[0] == 3:
        intervals_not_presenter = current_window[1].intervals_not_presenter
        intervals_presenter = extractOtherIntervals(intervalsA=intervals_voices,
                                                    intervalsB=intervals_not_presenter)
        messages.insert(END, 'Идет обработка последовательности картинок...\n')
        main_processing.videoAnalyse(intervals_not_presenter=intervals_not_presenter,
                                     split_interval_ms=main_processing.audioProcessing.slice_ms)
        messages.insert(END, 'Обработка последовательности картинок завершена\n')
        messages.insert(END, 'Все интервалы времени сформированы...\n')
        nextButton['text'] = 'Завершить'
        intervals_someone = main_processing.videoProcessing.intervals_someone
        intervals_together = main_processing.videoProcessing.intervals_together
        current_window = [4, None]
    elif current_window[0] == 4:
        print('Интервалы времени тишины : ', intervals_silence)
        print('Интервалы времени разговора ведущего : ', intervals_presenter)
        print('Интервалы времени разговора зрителя : ', intervals_someone)
        print('Интервалы времени разговора зрителя одновременно с ведущим : ', intervals_together)


if __name__ == '__main__':
    main_window = Tk()
    main_window.title("Анализ вебинаров")
    main_window.geometry('400x300')
    main_window.resizable(0, 0)
    main_window.update_idletasks()
    width_main_window, height_main_window = getMainWindowSize(root=main_window)

    messages = Text(main_window)
    messages.place(x=10,
                   y=height_main_window - 150,
                   width=width_main_window - 20,
                   height=100)

    nextButton = Button(main_window, text="Далее")
    nextButton.place(x=width_main_window - 150,
                     y=height_main_window - 30,
                     width=100)

    current_window = [1, WindowLoadVideo(parent=main_window,
                                         messages=messages)]
    nextButton['command'] = lambda: manageWindows(main_window=main_window,
                                                  messages=messages)

    main_window.mainloop()
