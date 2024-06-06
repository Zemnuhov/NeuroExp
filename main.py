from neuroexplib.exp_setting import ExperimentSetting
from neuroexplib.experiment import Experiment
from neuroexplib.stimulus_type import *

if __name__ == '__main__':
    app = Experiment(
        ExperimentSetting(
            stimulus=[
                Text(1000, '+', 'white'),
                Video(1000, path='C:/Presentation/Stimuls/21.mp4', play_to_end=True),
                Choice(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
                Image(5000, path="C:/Presentation/Stimuls/1.jpg"),
                Choice(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
                Image(5000, path="C:/Presentation/Stimuls/2.jpg"),
                Choice(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
                Image(5000, path="C:/Presentation/Stimuls/3.jpg"),
                Choice(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
            ],
            default_delay=500,
            parallel_port_address=0x3EFC
        )
    )
