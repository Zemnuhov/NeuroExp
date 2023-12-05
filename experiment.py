from pathlib import Path
from tkinter import *
from exp_setting import ExperimentSetting
from PIL import ImageTk, Image
import stimulus_type as s_type
import time


class Experiment(Tk):
    __exp_result = []
    __timer = time.time_ns()

    def __init__(self, setting: ExperimentSetting):
        super().__init__()
        self.img = None
        self.current_item = 0
        self.setting = setting
        self.bind('<Escape>', lambda x: self.destroy())
        self.attributes("-fullscreen", True)
        self.configure(bg=self.setting.background_color)
        self.stimulus_stack = []
        self.__update()
        mainloop()

    def __update(self):
        if self.current_item >= len(self.setting.stimulus):
            print(self.__exp_result)
            self.destroy()
        else:
            if isinstance(self.setting.stimulus[self.current_item], s_type.Text):
                self.show_text_stimulus(self.setting.stimulus[self.current_item])
            if isinstance(self.setting.stimulus[self.current_item], s_type.Image):
                self.show_image_stimulus(self.setting.stimulus[self.current_item])
            if isinstance(self.setting.stimulus[self.current_item], s_type.Choice):
                self.__timer = time.time_ns()
                self.show_choice_stimulus(self.setting.stimulus[self.current_item])
            self.update()
            if not isinstance(self.setting.stimulus[self.current_item], s_type.Choice):
                self.after(self.setting.stimulus[self.current_item].delay, self.__update)
            self.current_item += 1

    def show_image_stimulus(self, image_stimulus: s_type.Image):
        self.__clear_stack()
        pil_img = Image.open(image_stimulus.path)
        canvas_label = Canvas(self, width=pil_img.width, height=pil_img.height, bg=self.setting.background_color)
        canvas_label.pack(expand=True)
        self.img = ImageTk.PhotoImage(pil_img)
        canvas_label.create_image(0, 0, anchor=NW, image=self.img)
        self.stimulus_stack.append(canvas_label)

    def show_text_stimulus(self, text_stimulus: s_type.Text):
        self.__clear_stack()
        label = Label(text=text_stimulus.value, background=self.setting.background_color,
                      foreground=text_stimulus.text_color, font=text_stimulus.font)
        self.stimulus_stack.append(label)
        label.pack(expand=True)

    def user_choice(self, variant: str):
        stimulus = Path(self.setting.stimulus[self.current_item - 2].path).name if isinstance(
            self.setting.stimulus[self.current_item - 2], (
                s_type.Image,
                s_type.Video,
                s_type.Sound
            )
        ) else self.setting.stimulus[self.current_item - 2].value
        self.__exp_result.append(
            {
                'stimulus': stimulus,
                'choice': variant,
                'reaction': time.time_ns() - self.__timer
            }
        )
        self.__update()

    def show_choice_stimulus(self, choice: s_type.Choice):
        self.__clear_stack()
        if isinstance(choice.choice_buttons, str) and choice.choice_buttons.lower() == 'mouse':
            self.rowconfigure(index=0, weight=1)
            for idx, item in enumerate(choice.variants):
                self.columnconfigure(index=idx, weight=1)
                label = Button(text=item, font='Arial 40', background=self.setting.background_color,
                               command=lambda x=item: self.user_choice(x))
                label.grid(column=idx, row=0, ipadx=40, ipady=40)
                self.stimulus_stack.append(label)

    def __clear_stack(self):
        for stimulus in self.stimulus_stack:
            stimulus.forget()
            stimulus.destroy()
