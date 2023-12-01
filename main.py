
from exp_setting import ExperimentSetting
from experiment import Experiment
from stimulus_type import *

if __name__ == '__main__':
    app = Experiment(
        ExperimentSetting(
            stimulus=[
                Text(1000, 'Test1', 'white'),
                Image(5000, path="C:/Users\Egor\YandexDisk\Obsidian\Файлы\clip_image013.png"),
                Text(1000, 'Test3', 'white'),
                Image(5000, path="C:/Users\Egor\YandexDisk\Obsidian\Файлы\clip_image012.png"),
            ],
            default_delay=500
        )
    )

