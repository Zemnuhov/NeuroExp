from dataclasses import dataclass
from typing import *

@dataclass
class StimulusType:
    delay: int

@dataclass
class Text(StimulusType):
    value: str
    text_color: str
    font: str = 'Arial 20'
@dataclass
class Image(StimulusType):
    path: str

@dataclass
class Sound(StimulusType):
    path: str
    play_to_end: bool = True
@dataclass
class Video(StimulusType):
    path: str
    play_to_end: bool = True

@dataclass
class Choice(StimulusType):
    delay = -1
    variants: List
    choice_buttons: Union[List, str] = 'mouse'



