import glob
from typing import Any

import yaml

from mahverous.rule import Rule

DIR = ''


def init(working_dir: str) -> None:
  global DIR
  DIR = working_dir


class Pie():
  """A class representing a pie."""

  def __init__(self,
               display_str: str,
               count: int,
               is_allmighty: bool = False,
               **kwargs: dict[str,
                              Any]) -> None:
    self.display_str = display_str
    self.名前 = display_str
    self.count = count
    self.is_allmighty = is_allmighty
    for k, v in kwargs.items():
      setattr(self, k, v)

  def __str__(self) -> str:
    return self.display_str

  def __repr__(self) -> str:
    return self.display_str

  def __eq__(self, __value: object) -> bool:
    if not isinstance(__value, Pie):
      return False
    return self.__dict__ == __value.__dict__

  def __hash__(self) -> int:
    return hash(tuple(self.__dict__.items()))

  def to_str(self) -> str:
    parameters: list[str] = Rule()['ゲーム']['表示するパラメータ']
    return ' '.join([str(self.__getattribute__(parameter)) for parameter in parameters])


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
    ret[k] = Pie(k, (common_param | v)['枚数'], **(common_param | v))

  if Rule().allmighty_count > 0:
    ret['オールマイティ'] = Pie(
        'オールマイティ',
        Rule().allmighty_count,
        is_allmighty=True,
        **common_param)

  PIES_CACHE = ret
  return ret
