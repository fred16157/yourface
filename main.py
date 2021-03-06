from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window

import cv2
import show_realtime_detection

class MainApp(App) :
    def on_start(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,640) # set Width
        self.cap.set(4,480) # set Height
        self.overlayMode = False
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
            


    def update(self, dt) :
        ret, img = self.cap.read()
        img = cv2.flip(img, 1)
        if self.overlay is None :
            self.overlayMode = False
        result = show_realtime_detection.show_realtime_detection(img, self.overlay, overlayMode=self.overlayMode)
        buf = cv2.flip(result, 0).tostring()
        texture = Texture.create(size=(result.shape[1], result.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.root.ids.imageView.texture = texture

MainApp().run()
cv2.destroyAllWindows()