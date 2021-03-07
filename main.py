from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config
import tkinter as tk
from tkinter import filedialog

import cv2
import show_realtime_detection

class MainApp(App) :
    def on_start(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(3,640) # set Width
        self.cap.set(4,480) # set Height
        self.overlayMode = False
        self.overlayPath = ""
        self.overlay = None
        Clock.schedule_interval(self.update, 1.0/30.0)
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers) :
        if keycode[1] == 'f8':
            print('Settings open')
            self.popup = SettingsPopup()
            self.popup.ids.overlayModeCheckbox.active = self.overlayMode
            self.popup.ids.overlayPathInput.text = self.overlayPath
            self.popup.ids.overlayPathPickerButton.bind(on_release=self.open_file_picker)  
            self.popup.ids.confirmButton.bind(on_release=self.confirm_changes)
            self.popup.open()

    def open_file_picker(self, _):
        root = tk.Tk()
        root.withdraw()
        self.popup.ids.overlayPathInput.text = filedialog.askopenfilename()

    def confirm_changes(self, _) :
        self.overlayMode = self.popup.ids.overlayModeCheckbox.active
        self.overlayPath = self.popup.ids.overlayPathInput.text
        try:
            self.overlay = cv2.imread(self.overlayPath, -1)
        except: 
            self.overlay = None
        self.popup.dismiss()

    def update(self, dt) :
        ret, img = self.cap.read()
        img = cv2.flip(img, 1)
        result = None
        if self.overlayMode :
            if self.overlay is None and self.overlayPath != "":
                try :
                    self.overlay = cv2.imread(self.overlayPath, -1)
                    result = show_realtime_detection.show_realtime_detection(img, None, overlayMode=False)
                except :
                    result = img
                    self.overlayMode = False
                    print('Overlay path (' + self.overlayPath + ') is invalid. resetting path to empty string')
                    self.overlayPath = ""
                    
            else :
                result = show_realtime_detection.show_realtime_detection(img, self.overlay, overlayMode=self.overlayMode)
        else :
            result = img
        buf = cv2.flip(result, 0).tostring()
        texture = Texture.create(size=(result.shape[1], result.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.root.ids.imageView.texture = texture

class SettingsPopup(Popup) :
    pass

MainApp().run()
cv2.destroyAllWindows()