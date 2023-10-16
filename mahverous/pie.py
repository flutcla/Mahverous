import glob
from typing import Any

import yaml

from mahverous.rule import Rule

DIR = ''


def init(working_dir: str):
  global DIR
  DIR = working_dir


class Pie():
  """A class representing a pie."""
  def __init__(self, display_str, isAllmighty=False, **kwargs):
    self.display_str = display_str
    self.isAllmighty = isAllmighty
    for k, v in kwargs.items():
      setattr(self, k, v)

  def __str__(self):
    return self.display_str

  def __repr__(self):
    return self.display_str

  def __eq__(self, __value: object) -> bool:
    if not isinstance(__value, Pie):
      return False
    return self.__dict__ == __value.__dict__

  def __hash__(self) -> int:
    return hash(tuple(self.__dict__.items()))


PIES_CACHE: dict[str, Pie] = {}


def load_pies(dir_name: str = 'pies') -> dict[str, Pie]:
  """Load pies from yaml files in the specified directory."""
  global PIES_CACHE
  if PIES_CACHE:
    return PIES_CACHE
  pies: dict[str, Any] = {}
  for fpath in glob.glob(f'{DIR}/{dir_name}/*.yaml'):
    with open(fpath, 'r') as f:
      pie = yaml.safe_load(f)
      pies |= pie

  if 'COMMON' in pies.keys():
    common_param = pies['COMMON']
    pies.pop('COMMON')
  else:
    common_param = {}

  ret = {}
  for k, v in pies.items():
    ret[k] = Pie(k, **(common_param | v))

  if Rule().allmighty_count > 0:
    ret['オールマイティ'] = Pie('オールマイティ', isAllmighty=True)

  PIES_CACHE = ret
  return ret
