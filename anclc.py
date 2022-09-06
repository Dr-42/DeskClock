import tkinter
import ctypes
import math  # Required For Coordinates Calculation
import time  # Required For Time Handling
import threading
from playsound import playsound
user32 = ctypes.windll.user32

can_width = user32.GetSystemMetrics(0)
can_height = user32.GetSystemMetrics(1)

sound_bool=False
def sound():
    global sound_bool
    if not sound_bool:
        threading.Thread(target=playsound, args=('Gong.wav', ), daemon=True).start()
    sound_bool = True

class main(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.x = can_width/2  # Center Point x
        self.y = can_height/4  # Center Point
        self.minute_length = 100  # Stick Length
        self.hour_length = 60
        self.second_length =  110
        self.minute_width = 4
        self.hour_width = 8
        self.second_width = 2
        self.creating_all_function_trigger()

    # Creating Trigger For Other Functions
    def creating_all_function_trigger(self):
        self.create_canvas_for_shapes()
        self.creating_background_()
        self.creating_sticks()
        return

    # Creating Background
    def creating_background_(self):
        self.image = tkinter.PhotoImage(file='clock_face.png')
        self.canvas.create_image(can_width/2, can_height/4, image=self.image)
        return

    # creating Canvas
    def create_canvas_for_shapes(self):
        self.canvas = tkinter.Canvas(self, bg='gray99', width=can_width, height=can_height, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(expand='yes')
        return

    # Creating Moving Sticks
    def creating_sticks(self):
        self.sticks = []

        store = self.canvas.create_line(
            self.x, self.y, self.x+self.hour_length, self.y+self.hour_length, width=self.hour_width, fill='white')
        self.sticks.append(store)
        
        store = self.canvas.create_line(
            self.x, self.y, self.x+self.minute_length, self.y+self.minute_length, width=self.minute_width, fill='white')
        self.sticks.append(store)

        store = self.canvas.create_line(
            self.x, self.y, self.x+self.second_length, self.y+self.second_length, width=self.second_width, fill='white')
        self.sticks.append(store)

        return

    # Function Need Regular Update
    def update_class(self):
        global sound_bool
        now = time.localtime()
        t = time.strptime(str(now.tm_hour), "%H")
        hour = int(time.strftime("%I", t))*5
        now = (hour, now.tm_min, now.tm_sec)
        if now[1]==0 and now[2]==0:
            sound()
        if now[1]==0 and now[2]==1:
            sound_bool = False
        # Changing Stick Coordinates
        for n, i in enumerate(now):
            x, y = self.canvas.coords(self.sticks[n])[0:2]
            cr = [x, y]
            length = 0
            if n == 0:
                length = self.hour_length
            elif n == 1:
                length = self.minute_length

            else:
                length = self.second_length
            if n == 0:
                cr.append(length*math.cos(math.radians(i*6 + now[1]/2)-math.radians(90))+self.x)
                cr.append(length*math.sin(math.radians(i*6 + now[1]/2)-math.radians(90))+self.y)
            else:
                cr.append(length*math.cos(math.radians(i*6)-math.radians(90))+self.x)
                cr.append(length*math.sin(math.radians(i*6)-math.radians(90))+self.y)
            self.canvas.coords(self.sticks[n], tuple(cr))
        return

def close(event):
    global running
    running = False


# Main Function Trigger
if __name__ == '__main__':
    root = main()
    root.wm_attributes("-transparentcolor", "gray99")
    root.overrideredirect(True)
    global running
    running = True
    root.bind('<Escape>', close)
    # Creating Main Loop
    while running:
        root.update()
        root.update_idletasks()
        root.update_class()

