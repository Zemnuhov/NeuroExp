from datetime import datetime
from pathlib import Path
from tkinter import *
import cv2
from neuroexplib.exp_setting import ExperimentSetting
from PIL import ImageTk, Image
from neuroexplib.stimulus_type import *
from neuroexplib.trigger.com_port import COMPort
from neuroexplib.trigger.parallel_port import ParallelPort
from neuroexplib.trigger.trigger import Trigger
import time


class Experiment(Tk):
    __exp_result = []
    __timer = datetime.now()

    def __init__(self, setting: ExperimentSetting):
        super().__init__()
        self.parallel: Trigger = (
            COMPort(port=setting.parallel_port_address)
            if isinstance(setting.parallel_port_address, str)
            else ParallelPort(port=setting.parallel_port_address)
        )
        self.parallel.set_data(100)
        self.img = None
        self.current_item = 0
        self.stimulus_count = 0
        self.setting = setting
        self.bind("<Escape>", lambda x: self.destroy())
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
            item = self.setting.stimulus[self.current_item]
            if isinstance(item, TextStimulus):
                self.show_text_stimulus(item)
                self.stimulus_count += 1
            if isinstance(item, ImageStimulus):
                self.show_image_stimulus(item)
                self.stimulus_count += 1
            if isinstance(item, ChoiceStimulus):
                self.__timer = datetime.now()
                self.show_choice_stimulus(item)
            if isinstance(item, VideoStimulus):
                self.show_video_stimulus(item)
                self.stimulus_count += 1
            if isinstance(
                item, (ImageStimulus, VideoStimulus, SoundStimulus, TextStimulus)
            ):
                if item.trigger_type is not None:
                    self.parallel.set_data(item.trigger_type.value)
            self.update()
            if not isinstance(item, (ChoiceStimulus, VideoStimulus)) or (
                isinstance(item, VideoStimulus) and not item.play_to_end
            ):
                self.after(item.delay, self.__update)
            self.current_item += 1

    def show_image_stimulus(self, image_stimulus: ImageStimulus):
        self.__clear_stack()
        pil_img = Image.open(image_stimulus.path)
        canvas_label = Canvas(
            self,
            width=pil_img.width,
            height=pil_img.height,
            bg=self.setting.background_color,
        )
        canvas_label.pack(expand=True)
        self.img = ImageTk.PhotoImage(pil_img)
        canvas_label.create_image(0, 0, anchor=NW, image=self.img)
        self.parallel.set_data(self.stimulus_count+1)
        self.stimulus_stack.append(canvas_label)

    def show_text_stimulus(self, text_stimulus: TextStimulus):
        self.__clear_stack()
        label = Label(
            text=text_stimulus.value,
            background=self.setting.background_color,
            foreground=text_stimulus.text_color,
            font=text_stimulus.font,
        )
        self.parallel.set_data(self.stimulus_count+1)
        self.stimulus_stack.append(label)
        label.pack(expand=True)

    def user_choice(self, variant: str):
        stimulus = (
            Path(self.setting.stimulus[self.current_item - 2].path).name
            if isinstance(
                self.setting.stimulus[self.current_item - 2],
                (ImageStimulus, VideoStimulus, SoundStimulus),
            )
            else self.setting.stimulus[self.current_item - 2].value
        )
        self.__exp_result.append(
            {
                "stimulus": stimulus,
                "choice": variant,
                "reaction": str(datetime.now() - self.__timer),
                "trigger_type": str(
                    self.setting.stimulus[self.current_item - 2].trigger_type
                ),
            }
        )
        self.__update()

    def show_choice_stimulus(self, choice: ChoiceStimulus):
        self.__clear_stack()
        if (
            isinstance(choice.choice_buttons, str)
            and choice.choice_buttons.lower() == "mouse"
        ):
            self.rowconfigure(index=0, weight=1)
            for idx, item in enumerate(choice.variants):
                self.columnconfigure(index=idx, weight=1)
                label = Button(
                    text=item,
                    font="Arial 40",
                    background=self.setting.background_color,
                    command=lambda x=item: self.user_choice(x),
                )
                label.grid(column=idx, row=0, ipadx=40, ipady=40)
                self.stimulus_stack.append(label)

    def show_video_stimulus(self, video_stimulus: VideoStimulus):

        def __convert_frame_to_image(frame):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=img)
            return photo

        def __play_video(canvas: Canvas, video: cv2.VideoCapture):
            ret, frame = video.read()
            if ret:
                self.img = __convert_frame_to_image(frame)
                canvas.create_image(0, 0, image=self.img, anchor=NW)
                self.after(75, lambda x=canvas, y=video: __play_video(x, y))
            else:
                self.after(0, self.__update)

        self.__clear_stack()
        vid = cv2.VideoCapture(video_stimulus.path)
        canvas = Canvas(
            self,
            height=vid.get(cv2.CAP_PROP_FRAME_HEIGHT),
            width=vid.get(cv2.CAP_PROP_FRAME_WIDTH),
        )
        canvas.pack(expand=True)
        self.stimulus_stack.append(canvas)
        vid = cv2.VideoCapture(video_stimulus.path)
        self.parallel.set_data(self.stimulus_count+1)
        __play_video(canvas, vid)

    def __clear_stack(self):
        for stimulus in self.stimulus_stack:
            stimulus.forget()
            stimulus.destroy()
