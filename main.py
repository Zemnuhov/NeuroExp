from exp_setting import ExperimentSetting
from experiment import Experiment
from stimulus_type import *

if __name__ == '__main__':
    app = Experiment(
        ExperimentSetting(
            stimulus=[
                Text(1000, 'Тут описание экспиремента', 'white'),
                Image(5000, path="D:\Work/Neuro\Presentation\Stimuls/1.jpg"),
                Choice(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
                Image(5000, path="D:\Work/Neuro\Presentation\Stimuls/2.jpg"),
                Choice(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
                Image(5000, path="D:\Work/Neuro\Presentation\Stimuls/3.jpg"),
                Choice(10000, ['-3', '-2', '-1', '0', '1', '2', '3'], 'mouse'),
            ],
            default_delay=500
        )
    )
