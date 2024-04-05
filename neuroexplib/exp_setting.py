from typing import *
from neuroexplib.stimulus_type import *


class ExperimentSetting:

    def __init__(self, stimulus: List[Union[Video, Text, Image, Choice]], default_delay: int = 5000,
                 background_color: str = '#6d6d6d', parallel_port_address: int = 0x3EFC):
        self.stimulus = stimulus
        self.default_delay = default_delay
        self.background_color = background_color
        self.parallel_port_address = parallel_port_address
