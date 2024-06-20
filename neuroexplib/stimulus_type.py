from dataclasses import dataclass
from typing import *

from neuroexplib.stimulus.trigger_type import TriggerType


@dataclass
class StimulusType:
    delay: int

@dataclass
class TextStimulus(StimulusType):
    value: str
    text_color: str
    trigger_type: Optional[TriggerType] = None
    font: str = 'Arial 20'
@dataclass
class ImageStimulus(StimulusType):
    path: str
    trigger_type: Optional[TriggerType] = None

@dataclass
class SoundStimulus(StimulusType):
    path: str
    play_to_end: bool = True
    trigger_type: Optional[TriggerType] = None
@dataclass
class VideoStimulus(StimulusType):
    path: str
    play_to_end: bool = True
    trigger_type: Optional[TriggerType] = None

@dataclass
class ChoiceStimulus(StimulusType):
    delay = -1
    variants: List
    choice_buttons: Union[List, str] = 'mouse'



