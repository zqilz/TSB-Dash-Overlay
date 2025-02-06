# The Strongest Battlegrounds (TSB) Dash Timer Overlay

This script provides a visual overlay for the Roblox game "The Strongest Battlegrounds" (TSB) to help players track their dash cooldowns. It displays two timer bars: one for front/back dashes and one for side dashes.  The overlay is highly customizable, allowing you to adjust its appearance, position, and timer settings.

## Features

*   **Visual Dash Timers:** Displays two separate timer bars for front/back and side dashes.
*   **Customizable Appearance:**
    *   Change the size, color, and spacing of the timer bars.
    *   Adjust the overall opacity of the overlay.
    *   Modify the position of the overlay on the screen.
    *   Set the colors of the bar outlines and fills.
*   **Accurate Timing:** Uses precise timing to reflect the in-game dash cooldowns.
*   **Flicker Animation:** The timer bars flicker when the cooldown is complete, providing a clear visual cue.
*   **Always-On-Top:** The overlay stays on top of the game window, ensuring it's always visible.
*   **Transparency:** The overlay uses transparency to blend seamlessly with the game.
*   **Easy Control:** Starts timers automatically when the corresponding movement keys are pressed.
*   **Configurable:** All settings are clearly defined and documented within the script, making it easy to customize.

## Requirements

*   Python 3.x
*   Tkinter (usually included with Python)
*   `keyboard` library (`pip install keyboard`)

## Installation

1.  **Install Python:** If you don't have Python installed, download and install it from [python.org](https://www.python.org/). Make sure to add Python to your system's PATH during installation.
2.  **Install the `keyboard` library:** Open a terminal or command prompt and run:

    ```bash
    pip install keyboard
    ```
3.  **Download the Script:** Download the `overlay.py` file.
4. **Run as Administrator:** Right-click `overlay.py` and select `Run as administrator`.  This is REQUIRED for the `keyboard` library to function correctly.

## Usage

1.  **Run the Script:**  Double-click the `overlay.py` file, or run it from the command line using `python overlay.py`.  Make sure to run it as an administrator.
2.  **Start The Strongest Battlegrounds:** Launch the game.
3.  **Position the Overlay:** The overlay will appear at a default position (bottom-left corner).  You can change the default starting position (and many other parameters!) by modifying the configuration variables within the `overlay.py` script (see the "Configuration" section below).  It is recommended that you *not* drag and drop the overlay window; instead, configure its position by editing the script, to ensure it works correctly.
4.  **Play the Game:** The timer bars will automatically start when you press the corresponding movement keys:
    *   **'q' + 'w', 'q' + 's', 'q' + 'w' + 'a', 'q' + 'w' + 'd':**  Starts the front/back dash timer.
    *  **'q', alone, OR 'q' + 'a', 'q' + 'd':** Starts the side dash timer.

## Configuration

The `overlay.py` script is extensively commented, explaining each configuration option. Here's a breakdown of the key settings you can adjust:

*   **`window_x_offset` and `window_y_offset`:**  The initial position of the window (in pixels) relative to the top-left corner of your primary monitor.
*   **`window_opacity`:**  The overall transparency of the overlay (0.0 is fully transparent, 1.0 is fully opaque).
*   **`bar_width` and `bar_height`:** The dimensions of the timer bars (in pixels).
*   **`bar_spacing`:** The horizontal space between the timer bars (in pixels).
*   **`canvas_padding_x` and `canvas_padding_y`:** Padding around the bars within the window (in pixels).
*   **`border_color`:** The color of the bar outlines.
*   **`front_back_fill_color` and `side_dash_fill_color`:** The fill colors for the respective timer bars.
*   **`front_back_dash_duration` and `side_dash_duration`:**  The duration of the timers (in seconds).  These are set to the correct values by default.
*   **`timer_update_interval`:** How often the timers are updated (in seconds). Smaller values = smoother animation but higher CPU usage.
*   **`flicker_speed`:**  The speed of the flicker animation (in milliseconds).
*   **`flicker_count`:**  The number of times the bars flicker when a timer expires.

**Important:** To change these settings, open `overlay.py` in a text editor (like Notepad++, VS Code, or even the built-in IDLE), modify the values, and save the file.  Then, re-run the script.

**Color Names:** The `border_color`, `front_back_fill_color`, and `side_dash_fill_color` settings accept standard Tkinter color names. You can find a comprehensive list here: [TKINTER COLOR CHART](https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html).  You can also use hexadecimal color codes (e.g., `#FF0000` for red).

## Troubleshooting

*   **Overlay Not Appearing:**
    *   Make sure you're running the script as an administrator.
    *   Check that you have the required libraries installed (see "Requirements").
    *   Verify that your `window_x_offset` and `window_y_offset` values are placing the window within your screen's boundaries.  Try setting them to `0, 0` to test.
*   **Overlay Flickering or Not Updating:**
    *   Try increasing the `timer_update_interval` value slightly.
    *   Ensure that no other applications are interfering with the `keyboard` library.
*   **Key Presses Not Detected:**
    *   Again, ensure you are running the script as an administrator.
    *   The `keyboard` library might conflict with certain anti-cheat software or other input-monitoring tools.
*  **Window not transparent / Background visible**:
    * Double-check that `self.root.overrideredirect(True)` is set to `True`.
    * Verify that `self.root.wm_attributes("-transparentcolor", "black")` uses the same color as `self.root.configure(bg='black')`. Change both at the same time to matching valid Tkinter colors.

## Disclaimer

This script is an external tool and is not affiliated with or endorsed by the developers of The Strongest Battlegrounds. Use it at your own risk.  The game's developers may change the game mechanics, which could affect the accuracy or functionality of this overlay.
