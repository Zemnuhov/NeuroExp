from neuroexplib.exp_setting import ExperimentSetting
from neuroexplib.experiment import Experiment
from neuroexplib.stimulus_type import *

if __name__ == '__main__':
    app = Experiment(
        ExperimentSetting(
            stimulus=[
                TextStimulus(1000, '+', 'white'),
                VideoStimulus(1000, path='D:\Presentation\Stimuls/21.mp4', play_to_end=True),
                ChoiceStimulus(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
                ImageStimulus(5000, path="D:\Presentation\Stimuls/1.jpg"),
                ChoiceStimulus(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
                ImageStimulus(5000, path="D:\Presentation\Stimuls/2.jpg"),
                ChoiceStimulus(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
                ImageStimulus(5000, path="D:\Presentation\Stimuls/3.jpg"),
                ChoiceStimulus(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
            ],
            default_delay=500,
            parallel_port_address=0x3EFC
        )
    )
