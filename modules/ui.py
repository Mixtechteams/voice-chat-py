import tkinter as tk

mic_enable_text = "Включить микрофон"
mic_enable_color = "#c42b1c"
mic_disable_text = "Выключить микрофон"
mic_disable_color = "#81ea00"

class UI:
    conversation = []

    def __init__(self, on_print_click, on_mic_state_changed) -> None:
        self.on_print_click = on_print_click
        self.on_mic_state_changed = on_mic_state_changed
        self.mic_enabled = False
        self.init()
        
    def add_message(self, name, time, text):
        self.conversation += (name, time, text)
        self.text_area.insert(tk.END, f"[{time}] {name}: {text}\n")


    def handle_mic_button_click(self, button: tk.Button):
        self.mic_enabled = not self.mic_enabled
        text = mic_disable_text if self.mic_enabled else mic_enable_text
        color = mic_disable_color if self.mic_enabled else mic_enable_color
        button.config(text=text, bg=color)
        self.on_mic_state_changed(self.mic_enabled)

    def get_log(self):
        return self.text_area.get("1.0","end-1c")

    def init(self):
        # Create a window
        window = tk.Tk()
        self.window = window
        window.geometry("500x200+20+500")  # set the window size
        window.title("Система переговоров")  # set the window title

        # Set window attributes
        window.attributes('-topmost', True)  # make window always on top
        window.attributes('-alpha', 0.9)  # set window transparency
        window.attributes('-toolwindow', True)  # remove minimize and maximize buttons


        # Create a scrollable text area
        text_area = tk.Text(window, height=10)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text_area = text_area

        # Add a scrollbar to the text area
        scrollbar = tk.Scrollbar(text_area)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_area.yview)            

        # Create a frame for the buttons
        button_frame = tk.Frame(window)
        button_frame.pack(side=tk.BOTTOM)

        # Create a mic button
        mic_button = tk.Button(button_frame, 
                            command=lambda: self.handle_mic_button_click(mic_button),
                            text=mic_enable_text, bd=1, relief="solid", highlightthickness=0, highlightbackground="#767D89", padx=10, pady=5, borderwidth=0, bg=mic_enable_color, fg="#000000")
        mic_button.config(highlightcolor="#767D89")
        mic_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a print button
        print_button = tk.Button(button_frame, text="Распечатать запись переговоров", 
                            command=self.on_print_click,
                            bd=1, relief="solid", highlightthickness=0, highlightbackground="#767D89", padx=10, pady=5, borderwidth=0, bg="#FFFFFF", fg="#000000")
        print_button.config(highlightcolor="#767D89")
        print_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def render(self):
            # Run the window
        self.window.update() 
