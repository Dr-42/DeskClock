import tkinter

import math  # Required For Coordinates Calculation
import time  # Required For Time Handling

can_width = 150
can_height = 150

class main(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.x = can_width/2  # Center Point x
        self.y = can_height/2  # Center Point
        self.length = 50  # Stick Length
        self.creating_all_function_trigger()

    # Creating Trigger For Other Functions
    def creating_all_function_trigger(self):
        self.create_canvas_for_shapes()
        self.creating_background_()
        self.creating_sticks()
        return

    # Creating Background
    def creating_background_(self):
        self.image = tkinter.PhotoImage(file='clock.gif')
        self.canvas.create_image(can_width/2, can_height/2, image=self.image)
        return

    # creating Canvas
    def create_canvas_for_shapes(self):
        self.canvas = tkinter.Canvas(self, bg='gray99', width=can_width, height=can_height)
        self.canvas.pack(expand='yes', fill='both')
        return

    # Creating Moving Sticks
    def creating_sticks(self):
        self.sticks = []
        for i in range(3):
            store = self.canvas.create_line(
                self.x, self.y, self.x+self.length, self.y+self.length, width=2, fill='red')
            self.sticks.append(store)
        return

    # Function Need Regular Update
    def update_class(self):
        now = time.localtime()
        t = time.strptime(str(now.tm_hour), "%H")
        hour = int(time.strftime("%I", t))*5
        now = (hour, now.tm_min, now.tm_sec)
        # Changing Stick Coordinates
        for n, i in enumerate(now):
            x, y = self.canvas.coords(self.sticks[n])[0:2]
            cr = [x, y]
            cr.append(self.length*math.cos(math.radians(i*6)-math.radians(90))+self.x)
            cr.append(self.length*math.sin(math.radians(i*6)-math.radians(90))+self.y)
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

