import os
import yaml
from easydict import EasyDict

def get_config_dict(input_file_path="C:\\zqhome\\NYU Course\\DBS\\FinalProject\\code\\config.yaml"):
    with open(input_file_path, 'r') as stream:
        return EasyDict(yaml.safe_load(stream))
