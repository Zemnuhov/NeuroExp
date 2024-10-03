from pathlib import Path
import random

from neuroexplib.exp_setting import ExperimentSetting
from neuroexplib.experiment import Experiment
from neuroexplib.stimulus_type import *

if __name__ == '__main__':
    stimulus = [path for path in Path("D:/Stimulus/Стимулы/pos").iterdir()] + [path for path in Path(
        "D:/Stimulus/Стимулы/neg").iterdir()]
    stimulus_list = []
    for i in range(1, 201):
        stimulus_path: Path = random.choice(stimulus)
        stimulus_list.append(
            ImageStimulus(
                1000,
                path=str(stimulus_path),
                trigger_type=TriggerType.POSITIVE if "pos" in stimulus_path.parts else TriggerType.NEGATIVE, )
        )
        stimulus_list.append(TextStimulus(1000, '', 'white'))
        if i % 4 == 0 and i != 0:
            stimulus_list.append(ChoiceStimulus(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'), )

    app = Experiment(
        ExperimentSetting(
            stimulus=stimulus_list,
            default_delay=500,
            parallel_port_address=0x3EFC
        )
    )
