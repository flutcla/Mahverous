import glob

import yaml

DIR = ''


def init(working_dir: str):
  global DIR
  DIR = working_dir


def load_rule():
  """Load rule from yaml file in the specified directory."""
  fpath = glob.glob(f'{DIR}/rule.yaml')[0]
  with open(fpath, 'r') as f:
    rule = yaml.safe_load(f)
  return rule
