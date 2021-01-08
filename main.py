from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import webbrowser
import os
from calibration import Calibration
from detection import BlinkDetector
import win10toast
from datetime import date
import json
import time
import dlib


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except (ValueError, Exception):
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


b = BlinkDetector()
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(resource_path(r'.\img\shape_predictor_68_face_landmarks.dat'))

b.detector = detector
b.predictor = predictor
file = open(resource_path(r'.\img\settings.json'))
values = json.load(file)
wsk = values['wsk']
dgn = values['dgn']
file.close()
b.calibration_value = wsk
b.diagonal_value = dgn

is_polish = None


class MainGUI:
    def __init__(self, height, width, title):
        global is_polish

        f = open(resource_path(r'.\img\settings.json'))
        settings = json.load(f)
        is_polish = settings['language']
        f.close()

        self.root = Tk()

        self.root.title(title)
        self.height = height
        self.width = width

        self.root.geometry(f"{self.height}x{self.width}+250+150")
        self.root.resizable(width=False, height=False)

        self.font1 = font.Font(family="Consolas", size=50)
        self.font2 = font.Font(family="Consolas", size=17)
        self.light_blue_color = "#%02x%02x%02x" % (175, 234, 247)
        self.red_color = "#%02x%02x%02x" % (234, 107, 88)
        self.root.configure(bg=self.light_blue_color)

        self.title_label = Label(self.root, text="Ergonomizer", font=self.font1, bg=self.light_blue_color)
        self.title_label.place(relx=0.08, rely=0.1, anchor='nw')

        self.polish_subtitle = '''Wielogodzinna praca przy komputerze nie musi wcale wiązać się z bólem.
Dzięki temu programowi dowiesz się jak korzystać z komputera
tak aby Twoje zdrowie nie ucierpiało, a okulista oraz fizjoterapeuta
mogli zrobić sobie wakacje'''

        self.english_subtitle = '''Working at the computer for many hours doesn't has to be causing pain.
This program will teach you how to use your computer
 properly so you health won't suffer anymore and the ophthalmologist 
 and physiotherapist will be able to take a vacation'''

        self.subtitle_label = Label(self.root, text=self.polish_subtitle, font=self.font2, bg=self.light_blue_color)
        self.subtitle_label.place(relx=0.26, rely=0.3, anchor='nw')

        def hyperlink(url):
            webbrowser.open_new(url)

        self.link1 = Label(self.root, text="Dowiedz się wiecej o ergonomii <--", bg=self.light_blue_color,
                           cursor="hand2", font=self.font2, fg="#%02x%02x%02x" % (65, 124, 137))
        self.link1.place(relx=0.08, rely=0.6, anchor='nw')
        self.link1.bind("<Button-1>", lambda e: hyperlink("https://www.pip.gov.pl/ergonomia/index.html"))

        self.link2 = Label(self.root, text="--> Zespół suchego oka", bg=self.light_blue_color, cursor="hand2",
                           font=self.font2, fg="#%02x%02x%02x" % (65, 124, 137))
        self.link2.place(relx=0.2, rely=0.68, anchor='nw')
        self.link2.bind("<Button-1>", lambda e: hyperlink("https://pl.wikipedia.org/wiki/Zespół_suchego_oka"))

        self.link3 = Label(self.root, text="Jak siedzieć przy komputerze ? <--", bg=self.light_blue_color,
                           cursor="hand2", font=self.font2, fg="#%02x%02x%02x" % (65, 124, 137))
        self.link3.place(relx=0.08, rely=0.76, anchor='nw')
        self.link3.bind("<Button-1>", lambda e: hyperlink("https://www.youtube.com/watch?v=Ree1CWifQTg"))

        self.start_button = Button(self.root, text="Rozpocznij !", borderwidth=0, bg=self.red_color,
                                   font=self.font2, fg="white", command=self.after_start)
        self.start_button.place(relx=0.64, rely=0.67, anchor='nw')
        self.start_button.config(height=4, width=30)

        self.polish = ImageTk.PhotoImage(Image.open(resource_path(r'.\img\polish.png'))
                                         .resize((225, 150), Image.ANTIALIAS))
        self.english = ImageTk.PhotoImage(Image.open(resource_path(r'.\img\english.png'))
                                          .resize((225, 150), Image.ANTIALIAS))

        self.language_button = Button(self.root, image=self.polish, bg=self.light_blue_color, borderwidth=0,
                                      activebackground=self.light_blue_color,
                                      command=lambda: self.change_language(True))
        self.language_button.img = self.polish
        self.language_button.place(relx=0.77, rely=0.06, anchor='nw')
        self.change_language(False)

    def change_language(self, x):
        global is_polish

        f = open(resource_path(r'.\img\settings.json'))
        settings = json.load(f)
        f.close()

        if is_polish and x:
            self.language_button.configure(image=self.english)
            is_polish = False
            self.subtitle_label.config(text=self.english_subtitle)
            self.link1.configure(text='Learn more about ergonomy <--')
            self.link2.configure(text='--> Dry eye syndrome')
            self.link3.configure(text='How to sit properly ? <--')
            self.start_button.configure(text='Start !')
            settings['language'] = is_polish
            with open(resource_path(r'.\img\settings.json'), 'w') as f:
                json.dump(settings, f)
            f.close()
        elif not is_polish and x:
            self.language_button.configure(image=self.polish)
            is_polish = True
            self.subtitle_label.config(text=self.polish_subtitle)
            self.link1.configure(text='Dowiedz się wiecej o ergonomii <--')
            self.link2.configure(text='--> Zespół suchego oka')
            self.link3.configure(text='Jak siedzieć przy komputerze ? <--')
            self.start_button.configure(text='Rozpocznij !')
            settings['language'] = is_polish
            with open(resource_path(r'.\img\settings.json'), 'w') as f:
                json.dump(settings, f)
            f.close()
        elif not is_polish and not x:
            self.language_button.configure(image=self.english)
            self.subtitle_label.config(text=self.english_subtitle)
            self.link1.configure(text='Learn more about ergonomy <--')
            self.link2.configure(text='--> Dry eye syndrome')
            self.link3.configure(text='How to sit properly ? <--')
            self.start_button.configure(text='Start !')
        elif is_polish and not x:
            self.language_button.configure(image=self.polish)
            self.subtitle_label.config(text=self.polish_subtitle)
            self.link1.configure(text='Dowiedz się wiecej o ergonomii <--')
            self.link2.configure(text='--> Zespół suchego oka')
            self.link3.configure(text='Jak siedzieć przy komputerze ? <--')
            self.start_button.configure(text='Rozpocznij !')

    def working(self):
        self.root.mainloop()

    def after_start(self):
        self.root.destroy()
        self.root.quit()
        second_window()


class SecondGUI:
    def __init__(self, height, width, title):
        self.root = Tk()
        self.toaster = win10toast.ToastNotifier()

        self.root.title(title)
        self.height = height
        self.width = width

        self.blink_on = False
        self.blink_timer = 0
        self.last_blink_ratio_res = None
        self.distance_on = False
        self.distance_timer = 0
        self.distance_result = None
        self.notification_on = False

        self.root.geometry(f"{self.height}x{self.width}+250+150")
        self.root.resizable(width=False, height=False)

        self.font1 = font.Font(family="Consolas", size=30)
        self.font2 = font.Font(family="Consolas", size=17)
        self.light_blue_color = "#%02x%02x%02x" % (175, 234, 247)
        self.red_color = "#%02x%02x%02x" % (234, 107, 88)
        self.root.configure(bg=self.light_blue_color)

        self.data_distance = "brak danych"
        self.data_blink = "brak danych"
        self.data_date = date.today()
        if not is_polish:
            self.data_distance = "no data"
            self.data_blink = "no data"

        self.go_back_button = Button(self.root, text="Powrót", borderwidth=0, bg=self.red_color,
                                     font=self.font2, fg="white", command=self.go_back)
        self.go_back_button.place(relx=0.07, rely=0.07, anchor='nw')
        self.go_back_button.config(height=2, width=16)
        if not is_polish:
            self.go_back_button.configure(text='Go back')

        self.toggle_image_on = ImageTk.PhotoImage(Image.open(resource_path(r'.\img\toggle_on.png'))
                                                  .resize((128, 128), Image.ANTIALIAS))
        self.toggle_image_off = ImageTk.PhotoImage(Image.open(resource_path(r'.\img\toggle_off.png'))
                                                   .resize((128, 128), Image.ANTIALIAS))

        self.toggle_button1 = Button(self.root, image=self.toggle_image_off, bg=self.light_blue_color, borderwidth=0,
                                     activebackground=self.light_blue_color, command=lambda: self.switch_toggle(0))
        self.toggle_button1.img = self.toggle_image_off
        self.toggle_button1.place(relx=0.64, rely=0.10, anchor='nw')

        self.toggle_label1 = Label(self.root, text="Mruganie", font=self.font1, bg=self.light_blue_color)
        self.toggle_label1.place(relx=0.77, rely=0.145, anchor='nw')
        if not is_polish:
            self.toggle_label1.configure(text="Blinking")

        self.toggle_button2 = Button(self.root, image=self.toggle_image_off, bg=self.light_blue_color, borderwidth=0,
                                     activebackground=self.light_blue_color, command=lambda: self.switch_toggle(1))
        self.toggle_button2.img = self.toggle_image_off
        self.toggle_button2.place(relx=0.64, rely=0.26, anchor='nw')

        self.toggle_label2 = Label(self.root, text="Odległość", font=self.font1, bg=self.light_blue_color)
        self.toggle_label2.place(relx=0.77, rely=0.305, anchor='nw')
        if not is_polish:
            self.toggle_label2.configure(text="Distance")

        self.toggle_button3 = Button(self.root, image=self.toggle_image_off, bg=self.light_blue_color, borderwidth=0,
                                     activebackground=self.light_blue_color, command=lambda: self.switch_toggle(2))
        self.toggle_button3.img = self.toggle_image_off
        self.toggle_button3.place(relx=0.64, rely=0.42, anchor='nw')

        self.toggle_label3 = Label(self.root, text="Przypominacz", font=self.font1, bg=self.light_blue_color)
        self.toggle_label3.place(relx=0.77, rely=0.465, anchor='nw')
        if not is_polish:
            self.toggle_label3.configure(text="Reminder")

        self.toggles = [self.toggle_button1, self.toggle_button2, self.toggle_button3]
        self.toggle_labels = [self.toggle_label1, self.toggle_label2, self.toggle_label3]
        self.toggle_status = [0, 0, 0]

        self.calibration_button = Button(self.root, text="Kalibracja", borderwidth=0, bg=self.red_color,
                                         font=self.font2, fg="white", command=self.calibration_init)
        self.calibration_button.place(relx=0.64, rely=0.65, anchor='nw')
        self.calibration_button.config(height=3, width=31)
        if not is_polish:
            self.calibration_button.configure(text="Calibration")
        self.calibration = None

        self.show_res_button = Button(self.root, text="Utwórz nowy raport", borderwidth=0, bg=self.red_color,
                                      font=self.font2, fg="white", command=self.make_a_report)
        self.show_res_button.place(relx=0.64, rely=0.8, anchor='nw')
        self.show_res_button.config(height=3, width=31)
        if not is_polish:
            self.show_res_button.config(text="Create a new report")

        self.report_image = ImageTk.PhotoImage(Image.open(resource_path(r'.\img\raport.png')))
        canvas = Canvas(self.root, width=720, height=570, bg=self.light_blue_color, highlightthickness=0)
        canvas.create_image(-50, -50, image=self.report_image, anchor=NW)
        canvas.place(relx=0.07, rely=0.26, anchor='nw')

        self.data_label = Label(self.root, text=f"Raport z dnia {self.data_date}: ", font=self.font1)
        self.data_label.place(relx=0.09, rely=0.28, anchor='nw')
        if not is_polish:
            self.data_label.config(text=f"Report from {self.data_date}: ", font=self.font1)

        data = f'''   Odległość od monitora: {self.data_distance}\n\n    Częstotliwość mrugania: {self.data_blink}\n\n\n\n Pamiętaj o odpowiedniej pozycji,\n\n    podczas korzysania z komputera, nie\n\n zapomnij również  o prawidłowym \n\n     oświetleniu i robieniu sobie przerw.'''
        if not is_polish:
            data = f'''   Distance from the monitor: {self.data_distance}\n\n   Blinking frequency: {self.data_blink}\n\n\n\n Remember about the correct position\n\n    while working at the computer, \n\n do not forget about proper \n\n     lightning and taking breaks frequently.'''

        self.data_sub_label = Label(self.root, text=data, font=self.font2, fg="gray")
        self.data_sub_label.place(relx=0.07, rely=0.4, anchor='nw')
        try:
            self.update()
        except (ValueError, Exception):
            pass

    def make_a_report(self):
        if self.blink_on:
            self.switch_toggle(0)
            self.toggle_label1.configure(fg="black")
        if self.distance_on:
            self.switch_toggle(1)
            self.toggle_label2.configure(fg="black")
        if self.last_blink_ratio_res is not None:
            if self.last_blink_ratio_res > 8:
                self.data_blink = str(self.last_blink_ratio_res) + " na minutę\n - Prawidłowa"
                if not is_polish:
                    self.data_blink = str(self.last_blink_ratio_res) + " per minute\n - Correct"
            else:
                self.data_blink = str(self.last_blink_ratio_res) + " na minutę\n - Mrugasz za rzadko !"
                if not is_polish:
                    self.data_blink = str(self.last_blink_ratio_res) + " per minute\n - You blink too rarely !"
        else:
            self.data_blink = "brak danych\n\n"
            if not is_polish:
                self.data_blink = "no data\n\n"
        if self.distance_result is not None:
            if self.distance_result > 1:
                self.data_distance = "\n Masz tendecje do przybliżania się"
                if not is_polish:
                    self.data_distance = '\n You tend to move closer to the monitor'
            else:
                self.data_distance = "\n - Prawidłowa"
                if not is_polish:
                    self.data_distance = '\n  - Correct'
        else:
            self.data_distance = "brak danych"
            if not is_polish:
                self.data_distance = "no data"

        data = f'''   Odległość od monitora: {self.data_distance}\n\n    Częstotliwość mrugania: {self.data_blink}\n\n Pamiętaj o odpowiedniej pozycji,\n\n    podczas korzysania z komputera, nie\n\n zapomnij również  o prawidłowym \n\n     oświetleniu i robieniu sobie przerw.'''
        if not is_polish:
            data = f'''   Distance from the monitor: {self.data_distance}\n\n   Blinking frequency: {self.data_blink}\n\n Remember about the correct position\n\n    while working at the computer, \n\n do not forget about proper \n\n     lightning and taking breaks frequently.'''
        self.data_sub_label.configure(text=data)

    def update(self):
        try:
            global b
            b.working()
            if self.blink_on:
                b.check_if_blinks()
            if self.distance_on:
                b.check_if_not_too_close()
            if self.notification_on and int(time.strftime("%M", time.localtime())) % 15 == 0 and\
                    int(time.strftime("%S", time.localtime())) == 0:
                if is_polish:
                    self.toaster.show_toast("Engonomizer",
                                            'Czas na przerwę !\n Napij się wody, rozciągnij ciało i daj odopocząć oczom'
                                            ' aby wrócić z większą produktywkością i koncentracją !',
                                            duration=10, threaded=True)
                else:
                    self.toaster.show_toast("Engonomizer",
                                            "It's time to make a break!\n Drink some water, stretch yourself and give"
                                            " your eyes a rest to comeback with more productivity and concentration!",
                                            duration=10, threaded=True)

            if int(time.time() - self.blink_timer) == 600 and self.blink_on:
                self.toggle_label1.configure(fg="green")
            if int(time.time() - self.distance_timer) == 600 and self.distance_on:
                self.toggle_label2.configure(fg="green")
            self.root.after(1, self.update)
        except (ValueError, Exception):
            pass

    def working(self):
        self.root.mainloop()

    def switch_toggle(self, num_of_toggle):
        if self.toggle_status[num_of_toggle] == 0:
            self.toggles[num_of_toggle].configure(image=self.toggle_image_on)
            self.toggle_labels[num_of_toggle].configure(fg=self.red_color)
            self.toggle_status[num_of_toggle] = 1
            if num_of_toggle == 0:
                if is_polish:
                    self.toaster.show_toast("Engonomizer",
                                            'Włączono funkcje obserwatora mrugania. \nSłuży ona do pomiarów'
                                            'częstotliowści mrugania', duration=4, threaded=True)
                else:
                    self.toaster.show_toast("Ergonomizer",
                                            "Blink observer function has been enabled. \nIt's used to measure the"
                                            " blinking frequency", duration=4, threaded=True)
                self.blink_timer = time.time()
                self.blink_on = True
            if num_of_toggle == 1:
                if is_polish:
                    self.toaster.show_toast("Engonomizer", 'Włączono funkcje obserwatora odległości. \nSłuży ona do'
                                                           ' powiadomiania użytkownika kiedy będzie on zbyt blisko'
                                                           ' ekranu', duration=5, threaded=True)
                else:
                    self.toaster.show_toast("Engonomizer", "Distance observer function has been enabled. \nIt's used"
                                                           " to notify the user when he moves too close to the screen",
                                            duration=5, threaded=True)
                self.distance_timer = time.time()
                self.distance_on = True
            if num_of_toggle == 2:
                if is_polish:
                    self.toaster.show_toast("Engonomizer", 'Włączono funkcję przypominania. \nSłuży ona do'
                                                           ' przypominania użytkownikowi o robieniu przerw, piciu wody'
                                                           ' czy wykonaniu ćwiczeń', duration=5, threaded=True)
                else:
                    self.toaster.show_toast("Engonomizer", 'Reminder function has been enabled. \nIt is used to remind'
                                                           ' the user to take breaks, drink water or exercise',
                                            duration=5, threaded=True)
                self.notification_on = True
        else:
            self.toggles[num_of_toggle].configure(image=self.toggle_image_off)
            self.toggle_labels[num_of_toggle].configure(fg="black")
            self.toggle_status[num_of_toggle] = 0
            if num_of_toggle == 0:
                if is_polish:
                    self.toaster.show_toast("Engonomizer", 'Wyłączono funkcję obserwatora mrugania.', duration=3,
                                            threaded=True)
                else:
                    self.toaster.show_toast("Engonomizer", 'Blink function has been disabled', duration=3,
                                            threaded=True)
                if time.time() - self.blink_timer > 600:
                    self.last_blink_ratio_res = int(b.blink_count / ((time.time() - self.blink_timer)/60))
                self.blink_on = False
            if num_of_toggle == 1:
                if is_polish:
                    self.toaster.show_toast("Engonomizer", 'Wyłączono funkcję obserwatora odległości.', duration=3,
                                            threaded=True)
                else:
                    self.toaster.show_toast("Engonomizer", 'Distance observer function has been disabled.', duration=3,
                                            threaded=True)
                if time.time() - self.distance_timer > 600:
                    self.distance_result = int(b.distance_count / ((time.time() - self.distance_timer)/60))
                self.distance_on = False
            if num_of_toggle == 2:
                if is_polish:
                    self.toaster.show_toast("Engonomizer", 'Wyłączono funkcję przypominania.', duration=3,
                                            threaded=True)
                else:
                    self.toaster.show_toast("Engonomizer", 'Reminder function has been disabled.', duration=3,
                                            threaded=True)
                self.notification_on = False

    def go_back(self):
        self.root.destroy()
        self.root.quit()
        main_window()

    def calibration_init(self):
        global b
        b.__del__()
        self.root.destroy()
        self.root.quit()
        self.calibration = Calibration(is_polish)
        f = open(resource_path(r'.\img\settings.json'))
        settings = json.load(f)
        f.close()
        b = BlinkDetector(is_polish)
        b.detector = detector
        b.predictor = predictor
        b.calibration_value = settings['wsk']
        b.diagonal_value = settings['dgn']
        second_window()


def main_window():
    main_gui = MainGUI(1366, 768, "Ergonomizer")
    main_gui.working()


def second_window():
    second_gui = SecondGUI(1366, 768, "Ergonomizer")
    second_gui.working()


main_window()
