import tkinter as tk
import keyboard
import time
import threading

class TSBOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("TSB Overlay")

        # --- Window Configuration ---
        # `overrideredirect(True)`: Removes the window's title bar and borders, making it a custom-shaped window.  Set to `False` to restore standard window decorations.
        self.root.overrideredirect(True)
        # `window_x_offset` and `window_y_offset`:  Sets the initial position of the window on the screen.  Increase `window_x_offset` to move the window to the right; decrease to move left.  Increase `window_y_offset` to move the window down; decrease to move up.  Values are in pixels.  These are offsets from the top-left corner of the primary monitor.
        # Default: 0, 960
        self.window_x_offset = 0
        self.window_y_offset = 960
        # `configure(bg='black')`: Sets the background color of the window to black.  This is used in conjunction with `-transparentcolor` to make the window transparent.  You can change 'black' to any valid Tkinter color name (e.g., 'red', 'blue', '#FF0000' for red).  This color will be made transparent.
        self.root.configure(bg='black')
        # `wm_attributes("-topmost", True)`: Makes the window always stay on top of other normal windows.  Set to `False` to allow other windows to cover it.
        self.root.wm_attributes("-topmost", True)
        # `wm_attributes("-transparentcolor", "black")`: Makes the 'black' color transparent, creating the overlay effect.  Change 'black' to match the `bg` color if you change the background.
        self.root.wm_attributes("-transparentcolor", "black")
        # `resizable(False, False)`: Prevents the user from resizing the window. Set either `False` to `True` to allow resizing in that dimension (width, height).
        self.root.resizable(False, False)
        # `attributes("-alpha", self.window_opacity)`: Sets the overall opacity of the window.  `1.0` is fully opaque, `0.0` is fully transparent. (Default: 0.5)
        self.window_opacity = 0.5
        self.root.attributes("-alpha", self.window_opacity)

        # --- UI Configuration ---
        # `bar_width` and `bar_height`:  Sets the width and height of each timer bar, in pixels. (Default: 100, 80)
        self.bar_width = 100
        self.bar_height = 80
        # `bar_spacing`: Sets the horizontal spacing between the timer bars, in pixels. (Default: 10)
        self.bar_spacing = 10
        # `canvas_padding_x` and `canvas_padding_y`:  Sets the padding around the timer bars within the window, in pixels.  This creates a border around the entire canvas. (Default: 10, 10)
        self.canvas_padding_x = 10
        self.canvas_padding_y = 10
        # `border_color`: Sets the color of the outline around each timer bar.  Use any valid Tkinter color name.
        self.border_color = "white"
        # `front_back_fill_color`: Sets the fill color of the front/back dash timer bar. Use any valid Tkinter color name.
        self.front_back_fill_color = "cyan"
        # `side_dash_fill_color`: Sets the fill color of the side dash timer bar. Use any valid Tkinter color name.
        self.side_dash_fill_color = "lime"
        # TKINTER COLOR CHART: https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html

        # --- Timer Configuration ---
        # `front_back_dash_duration`: Sets the duration of the front/back dash timer, in seconds. (Default: 5.0, you probably don't need to change this)
        self.front_back_dash_duration = 5.0
        # `side_dash_duration`: Sets the duration of the side dash timer, in seconds. (Default: 2.0, you probably don't need to change this)
        self.side_dash_duration = 2.0
        # `timer_update_interval`: How often the timer is updated, in seconds.  Smaller values result in smoother animation but higher CPU usage.  (Default: 0.03)
        self.timer_update_interval = 0.03
        # `flicker_speed`: Sets the speed of the flicker animation when a timer runs out, in milliseconds.  This is the delay between each on/off cycle. (Default: 100)
        self.flicker_speed = 100
        # `flicker_count`: Sets the number of times the bar flickers when the timer runs out. (Default: 2)
        self.flicker_count = 2

        # --- Timer Variables ---
        # This dictionary stores all the data for each timer bar.  You should generally not modify this directly.
        self.bars = {
            "front_back": {
                "timer": 0,  # Current timer value (initially 0)
                "active": False,  # Is the timer currently running?
                "animating": False,  # Is the flicker animation currently playing?
                "duration": self.front_back_dash_duration,  # Duration of the timer (copied from above)
                "fill_color": self.front_back_fill_color,  # Fill color (copied from above)
                "bar_id": None,  # Tkinter canvas ID of the rectangle for the bar outline
                "fill_id": None,  # Tkinter canvas ID of the rectangle for the bar fill
            },
            "side_dash": {
                "timer": 0,
                "active": False,
                "animating": False,
                "duration": self.side_dash_duration,
                "fill_color": self.side_dash_fill_color,
                "bar_id": None,
                "fill_id": None,
            },
        }

        self.calculate_dimensions()
        self.create_canvas_and_bars()

        keyboard.on_press(self.key_pressed)

        self.update_thread = threading.Thread(target=self.update_timers, daemon=True)
        self.update_thread.start()

    def calculate_dimensions(self):
         self.canvas_width = 2 * self.bar_width + 3 * self.bar_spacing
         self.canvas_height = self.bar_height + 2 * self.canvas_padding_y
         self.window_width = self.canvas_width + 2 * self.canvas_padding_x
         self.window_height = self.canvas_height + 2*self.canvas_padding_y

    def create_canvas_and_bars(self):
         if hasattr(self, 'canvas') and self.canvas:
             self.canvas.destroy()

         self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="black", highlightthickness=0)
         self.canvas.pack(pady=self.canvas_padding_y, padx=self.canvas_padding_x)

         x_pos = self.bar_spacing
         for bar_name, bar_data in self.bars.items():
             bar_x1 = x_pos
             bar_y1 = self.canvas_padding_y
             bar_x2 = bar_x1 + self.bar_width
             bar_y2 = bar_y1 + self.bar_height
             bar_data["bar_id"] = self.canvas.create_rectangle(bar_x1, bar_y1, bar_x2, bar_y2, outline=self.border_color, fill="")
             x_pos = bar_x2 + self.bar_spacing

         self.root.geometry(f"{self.window_width}x{self.window_height}+{self.window_x_offset}+{self.window_y_offset}")


    def key_pressed(self, event):
        if event.name == 'q':
            if (keyboard.is_pressed('w') or keyboard.is_pressed('s') or
                (keyboard.is_pressed('w') and keyboard.is_pressed('d')) or
                (keyboard.is_pressed('w') and keyboard.is_pressed('a'))):
                self.start_timer("front_back")
            elif keyboard.is_pressed('a') or keyboard.is_pressed('d'):
                self.start_timer("side_dash")
            elif not(keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('a') or keyboard.is_pressed('d')):
                self.start_timer("front_back")

    def start_timer(self, bar_name):
        bar_data = self.bars[bar_name]
        if not bar_data["active"]:
            bar_data["timer"] = bar_data["duration"]
            bar_data["active"] = True
            bar_data["animating"] = False

    def update_timers(self):
        while True:
            for bar_name, bar_data in self.bars.items():
                self.update_bar(bar_name)
            time.sleep(self.timer_update_interval)

    def update_bar(self, bar_name):
        bar_data = self.bars[bar_name]

        if bar_data["active"]:
            bar_data["timer"] -= self.timer_update_interval
            if bar_data["timer"] <= 0:
                bar_data["timer"] = 0
                bar_data["active"] = False
                bar_data["animating"] = True
                self.animate_bar(bar_name)
                return

            fill_width = (bar_data["timer"] / bar_data["duration"]) * self.bar_width
            fill_width = max(0, min(fill_width, self.bar_width))

            bar_x1, bar_y1, bar_x2, bar_y2 = self.canvas.coords(bar_data["bar_id"])
            fill_x1 = bar_x2 - fill_width
            fill_x2 = bar_x2

            if bar_data["fill_id"]:
                self.canvas.delete(bar_data["fill_id"])
            bar_data["fill_id"] = self.canvas.create_rectangle(fill_x1, bar_y1, fill_x2, bar_y2, fill=bar_data["fill_color"], outline="")

    def animate_bar(self, bar_name):
        bar_data = self.bars[bar_name]
        if not bar_data["animating"]:
            return

        def flicker(count):
            if count <= 0 or not bar_data["animating"]:
                bar_data["animating"] = False
                if bar_data["fill_id"]:
                    self.canvas.delete(bar_data["fill_id"])
                    bar_data["fill_id"] = None
                return

            bar_x1, bar_y1, bar_x2, bar_y2 = self.canvas.coords(bar_data["bar_id"])

            if count % 2 == 0:
                if bar_data["fill_id"]:
                    self.canvas.delete(bar_data["fill_id"])
                bar_data["fill_id"] = self.canvas.create_rectangle(bar_x1, bar_y1, bar_x2, bar_y2, fill=bar_data["fill_color"], outline="")
            else:
                if bar_data["fill_id"]:
                    self.canvas.delete(bar_data["fill_id"])
                    bar_data["fill_id"] = None

            self.root.after(self.flicker_speed, flicker, count - 1)

        flicker(self.flicker_count * 2)


if __name__ == "__main__":
    root = tk.Tk()
    overlay = TSBOverlay(root)
    root.mainloop()