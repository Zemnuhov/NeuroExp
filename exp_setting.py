from typing import *
from stimulus_type import *


class ExperimentSetting:

    def __init__(self, stimulus: List[Union[Video, Text, Image, Choice]], default_delay: int = 5000,
                 background_color: str = '#6d6d6d'):
        self.stimulus = stimulus
        self.default_delay = default_delay
        self.background_color = background_color
