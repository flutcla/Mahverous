import glob
from typing import Any, Self

import yaml

DIR = ''


def init(working_dir: str) -> None:
  global DIR
  DIR = working_dir
  Rule()


class Rule():
  instance: Self | None = None
  rule: dict[str, Any] = {}
  hand_count: int
  allmighty_count: int
  combination: bool

  def __new__(cls) -> Self:
    if cls.instance:
      return cls.instance  # type: ignore
    cls.instance = super().__new__(cls)
    fpath = glob.glob(f'{DIR}/rule.yaml')[0]
    with open(fpath, 'r') as f:
      rule = yaml.safe_load(f)
    cls.hand_count = int(rule['完成形の枚数'])
    cls.allmighty_count = int(rule['オールマイティの枚数'])
    cls.combination = rule['役の複合']
    return cls.instance
