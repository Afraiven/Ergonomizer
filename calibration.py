from tkinter import *
import cv2
from PIL import Image, ImageTk
from tkinter import font
from tkinter.ttk import Combobox
from detection import BlinkDetector
import sys
import os
import json
import webbrowser
from tkinter import ttk
import dlib


detector = None
predictor = None


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except (ValueError, Exception):
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


class Loading:
    def __init__(self, is_polish):
        global detector, predictor

        def progress(current_value):
            progressbar["value"] = current_value

        root = Tk()

        if not is_polish:
            root.title("Calibration")
        else:
            root.title("Kalibracja")
        root.attributes("-topmost", True)

        root.resizable(False, False)

        window_height = 200
        window_width = 550
        max_value = 100

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        font1 = font.Font(family="Consolas", size=20)
        light_blue_color = "#%02x%02x%02x" % (175, 234, 247)
        root.configure(bg=light_blue_color)
        space_label = Label(root, text="    ", font=font1, bg=light_blue_color)
        space_label.pack()
        if not is_polish:
            l1 = Label(root, text="  Calibration module is loading  ", font=font1, bg=light_blue_color)
        else:
            l1 = Label(root, text="  Trwa ładowanie ekranu kalibracji  ", font=font1, bg=light_blue_color)
        l1.pack()
        progressbar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        progressbar.pack(side=TOP)
        space_label2 = Label(root, text=" ", font=font1, bg=light_blue_color)
        space_label2.pack()

        value = 0
        progressbar["value"] = value
        progressbar["maximum"] = max_value
        divisions = 10
        for i in range(divisions):
            value += 10
            if i == 0:
                detector = dlib.get_frontal_face_detector()
                predictor = dlib.shape_predictor(resource_path(r'.\img\shape_predictor_68_face_landmarks.dat'))
            progressbar.after(50, progress(value))
            progressbar.update()
        root.destroy()
        root.quit()


class Calibration:
    def __init__(self, is_polish):
        global detector, predictor

        def hyperlink(url):
            webbrowser.open_new(url)
        Loading(is_polish)

        self.root = Tk()
        if not is_polish:
            self.root.title('Calibration')
        else:
            self.root.title("Kalibracja")
        self.root.geometry("1366x768+250+150")
        self.root.resizable(width=False, height=False)

        self.font1 = font.Font(family="Consolas", size=15)
        self.font2 = font.Font(family="Consolas", size=13)
        self.font3 = font.Font(family="Consolas", size=18)
        self.font4 = font.Font(family="Consolas", size=8)
        self.light_blue_color = "#%02x%02x%02x" % (175, 234, 247)
        self.red_color = "#%02x%02x%02x" % (234, 107, 88)
        self.root.configure(bg=self.light_blue_color)

        f = open(resource_path(r'.\img\settings.json'))
        settings = json.load(f)
        self.calibration_value = settings['wsk']
        self.diagonal_value = settings['dgn']
        f.close()

        self.b = BlinkDetector(is_polish)
        self.b.detector = detector
        self.b.predictor = predictor

        if is_polish:
            self.calibrate_cam_text = '''       Aby program działał poprawnie kamera powinna 
            obejować całą twarz, ustaw kamere w taki sposób
            aby podczas korzystania z komputera program
            widział całą Twoją twarz, unikaj ustawiania jej
            pod kątem, zadbaj również o odpowienie światło
            < - - tutaj
            możesz dowiedzieć się wiecej na temat
            odpowiedniego oświetlenia przy komputerze.'''
            self.slider_text = "Ustaw wartość przy której wykrywanie mrugania działa najlepiej"
            self.sub_slider_text = '''Z uwagi na to, że program jest we wczesnych etapach 
tworzenia kalibracja musi odbywać się manualnie'''

        else:
            self.calibrate_cam_text = '''      Program needs to have the camera set up 
             properly, camera has to cover your entire face.
             Try to position it to be looking at your from
             front, do not set it at an angle. Make sure that
             there is a good enough light around you
             < - - here 
             you can learn more about lightning
             at the computere.'''
            self.slider_text = "Select calibration value (Where blinking detection works best)"
            self.sub_slider_text = '''Due to the fact that this is early version of the program
calibration has to be done manually'''

        self.go_back_button = Button(self.root, text="Zapisz i wróć", borderwidth=0, bg=self.red_color,
                                     font=self.font3, fg="white", command=self.go_back)
        self.go_back_button.place(relx=0.07, rely=0.07, anchor='nw')
        self.go_back_button.config(height=2, width=20)
        if not is_polish:
            self.go_back_button.config(text="Go back & save")
        
        self.calibrate_cam_label = Label(self.root, text=self.calibrate_cam_text, font=self.font1,
                                         bg=self.light_blue_color)

        if is_polish:
            self.calibrate_cam_label.place(relx=-0.02, rely=0.25, anchor='nw')
        else:
            self.calibrate_cam_label.place(relx=-0.04, rely=0.25, anchor='nw')

        self.canvas = Canvas(self.root, width=self.b.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                             height=self.b.cap.get(cv2.CAP_PROP_FRAME_HEIGHT), highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.05, anchor='nw')

        self.slider_label = Label(self.root, text=self.slider_text, font=self.font1, bg=self.light_blue_color)
        self.slider_label.place(relx=0.47, rely=0.72, anchor='nw')

        self.slider_sub_label = Label(self.root, text=self.sub_slider_text,
                                      font=self.font2, bg=self.light_blue_color, fg="gray")
        self.slider_sub_label.place(relx=0.57, rely=0.77, anchor='nw')

        self.slider = Scale(self.root, from_=2.0, to=8.0, length=400, digits=2, resolution=0.1, orient=HORIZONTAL,
                            bg=self.light_blue_color, highlightthickness=0)
        self.slider.place(relx=0.6, rely=0.84, anchor='nw')
        self.slider.set(float(self.calibration_value))

        self.screen_diagonal_label = Label(self.root, text="Podaj przekątną swojego ekranu", font=self.font1,
                                           bg=self.light_blue_color)
        self.screen_diagonal_label.place(relx=0.12, rely=0.72, anchor='nw')
        if not is_polish:
            self.screen_diagonal_label.config(text="Select your screen's diagonal")
        if is_polish:
            values = ["15 cali", "17 cali", "19 cali", "21 cali", "22 cale", "24 cale"]
        else:
            values = ["15 inches", "17 inches", "19 inches", "21 inches", "22 inches", "24 inches"]
        value_index = 33
        for i in range(len(values)):
            if values[i][:2] == str(self.diagonal_value):
                value_index = i
                break
        self.screen_diagonal_select = Combobox(self.root, values=values, state="readonly", font=self.font2)
        self.screen_diagonal_select.place(relx=0.15, rely=0.79, anchor='nw')
        self.screen_diagonal_select.current(value_index)

        self.link_light = Label(self.root, text="     tutaj     ", cursor="hand2", font=self.font4,
                                fg="white", bg=self.red_color)
        self.link_light.place(relx=0.13, rely=0.407, anchor='nw')
        self.link_light.bind("<Button-1>", lambda e: hyperlink(
            "https://iluve.com/strefa-porad/blog-iluve/oswietlenie-biurka-prawidlowe-oswietlenie-miejsca-pracy/"))
        if not is_polish:
            self.link_light.config(text="     here     ")

        self.photo = None

        self.update()

        self.root.mainloop()

    def update(self):
        try:
            if self.slider.get() != self.calibration_value:
                self.calibration_value = self.slider.get()
                print(self.calibration_value)
                self.b.calibration_value = self.calibration_value
            if int(self.screen_diagonal_select.get()[:2]) != self.diagonal_value:
                self.diagonal_value = int(self.screen_diagonal_select.get()[:2])
                print(self.diagonal_value)
                self.b.diagonal_value = self.diagonal_value
            self.b.working()
            try:
                self.b.check_if_blinks()
            except (ValueError, Exception):
                pass
            if self.b.ret:
                self.b.frame = cv2.cvtColor(self.b.frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.b.frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

            self.root.after(1, self.update)
        except (ValueError, Exception):
            pass

    def go_back(self):
        f = open(resource_path(r'.\img\settings.json'))
        settings = json.load(f)
        f.close()
        settings['wsk'] = self.calibration_value
        settings['dgn'] = self.diagonal_value

        with open(resource_path(r'.\img\settings.json'), 'w') as f:
            json.dump(settings, f)
        f.close()

        self.b.__del__()
        self.root.destroy()
        self.root.quit()
