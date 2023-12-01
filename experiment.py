from tkinter import *
from exp_setting import ExperimentSetting
from PIL import ImageTk, Image
import stimulus_type as s_type


class Experiment(Tk):

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
            self.current_item = 0
        if isinstance(self.setting.stimulus[self.current_item], s_type.Text):
            self.show_text_stimulus(self.setting.stimulus[self.current_item])
        if isinstance(self.setting.stimulus[self.current_item], s_type.Image):
            self.show_image_stimulus(self.setting.stimulus[self.current_item])
        self.update()
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

    def __clear_stack(self):
        for stimulus in self.stimulus_stack:
            stimulus.forget()
