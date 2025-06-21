from customtkinter import *
import random
import time
import threading

set_appearance_mode("dark")
set_default_color_theme("dark-blue")


class ReactionTestApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("Тест на реакцію")
        self.geometry("500x400")

        self.configure(fg_color="midnight blue")

        self.draw_background_pattern()

        self.label = CTkLabel(self, text="Натисни кнопку, коли вона ЗМІНИТЬСЯ", font=("Arial", 16),
                              wraplength=500, justify="center", text_color="light steel blue")
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.button = CTkButton(self, text="Готуйся...", command=self.button_clicked, state="disabled",
                                fg_color="gray20", width=120, height=60, corner_radius=10, font=("Arial", 16))
        self.button.place(relx=0.5, rely=0.4, anchor="center")

        self.start_button = CTkButton(self, text="Почати тест", command=self.start_test, font=("Arial", 14))
        self.start_button.place(relx=0.5, rely=0.7, anchor="center")

        self.reset_all()

    def draw_background_pattern(self):
        colors = ["indigo", "midnight blue", "navy", "gray10"]
        size = 30
        for x in range(0, 700, size):
            for y in range(0, 600, size):
                color = random.choice(colors)
                symbols = ["█", "▄", "▀", "─", "│"]
                symbol = random.choice(symbols)
                label = CTkLabel(self, text=symbol, font=("Consolas", 14), text_color=color)
                label.place(x=x, y=y)

    def reset_all(self):
        self.reaction_times = []
        self.completed_modes = []
        self.current_test_type = None
        self.button_ready = False
        self.start_time = 0
        self.test_in_progress = False
        self.test_triggered = False

    def start_test(self):
        if self.test_in_progress:
            return

        self.test_in_progress = True
        self.label.configure(text="Готуйся...", text_color="light steel blue")
        self.start_button.configure(state="disabled")
        self.button.configure(text="Готуйся...", fg_color="gray20", state="normal", corner_radius=10, width=120,
                              height=60)
        self.button_ready = False
        self.test_triggered = False

        if len(self.completed_modes) == 0:
            self.current_test_type = random.choice(["колір", "форму"])
        else:
            self.current_test_type = "форму" if self.completed_modes[0] == "колір" else "колір"

        threading.Thread(target=self.wait_and_trigger_change).start()

    def wait_and_trigger_change(self):
        delay = random.uniform(2, 5)
        time.sleep(delay)

        self.start_time = time.time()
        self.button_ready = True
        self.test_triggered = True

        active_color = "cyan"

        if self.current_test_type == "колір":
            self.button.configure(fg_color=active_color, text="Натисни!", text_color="magenta", corner_radius=10,
                                  width=120, height=60)
        elif self.current_test_type == "форму":
            self.button.configure(width=120, height=120, corner_radius=0, text="Натисни!", text_color="magenta",
                                  fg_color=active_color)

        self.label.configure(text="ШВИДШЕ!", text_color="gold")

    def button_clicked(self):
        if not self.test_triggered:
            self.label.configure(text="Занадто рано! Тест перезапущено.", text_color="red")
            self.reset_after_early_click()
            return

        if not self.button_ready:
            return

        reaction_time = time.time() - self.start_time
        self.reaction_times.append(reaction_time)
        self.completed_modes.append(self.current_test_type)

        self.button_ready = False
        self.test_triggered = False
        self.button.configure(state="disabled", fg_color="gray20", text="Готуйся...", corner_radius=10, width=120,
                              height=60)

        self.label.configure(text=f"Реакція на {self.current_test_type}: {reaction_time:.3f} секунд",
                             text_color="light steel blue")

        if len(self.reaction_times) == 2:
            avg = sum(self.reaction_times) / 2
            result_text = (f"Результати:\n"
                           f"- 1 спроба: {self.reaction_times[0]:.3f} с\n"
                           f"- 2 спроба: {self.reaction_times[1]:.3f} с\n"
                           f"Середній час: {avg:.3f} с")
            self.label.configure(text=result_text, text_color="pale green")
            self.start_button.configure(text="Повторити", state="normal")
            self.reset_all()
        else:
            threading.Thread(target=self.delayed_next_test).start()

    def delayed_next_test(self):
        time.sleep(2)
        self.test_in_progress = False
        self.start_test()

    def reset_after_early_click(self):
        self.button.configure(text="Готуйся...", state="disabled", fg_color="gray20", corner_radius=10, width=120,
                              height=60)
        self.label.after(2000, lambda: self.label.configure(text="Натисни кнопку, коли вона ЗМІНИТЬСЯ",
                                                            text_color="light steel blue"))
        self.start_button.configure(state="normal", text="Почати тест")
        self.reset_all()


app = ReactionTestApp()
app.mainloop()
