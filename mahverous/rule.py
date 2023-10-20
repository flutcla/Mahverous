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
  run_script = False
  items: dict[str, Any]
  prescript: list[str]
  postscript: list[str]

  def __new__(cls) -> Self:
    if cls.instance:
      return cls.instance  # type: ignore
    cls.instance = super().__new__(cls)
    fpath = glob.glob(f'{DIR}/rule.yaml')[0]
    with open(fpath, 'r') as f:
      rule: dict[str, Any] = yaml.safe_load(f)
    cls.hand_count = int(rule['完成形の枚数'])
    cls.allmighty_count = int(rule['オールマイティの枚数'])
    cls.combination = rule['役の複合']

    cls.prescript = rule.get('前処理', [])
    cls.postscript = rule.get('後処理', [])

    cls.items = rule

    return cls.instance

  @classmethod
  def run_prescript(cls) -> None:
    for script in cls.prescript:
      exec(script, globals())

  @classmethod
  def run_postscript(cls) -> None:
    for script in cls.postscript:
      exec(script, globals())

  def __getitem__(self, __name: str) -> Any:
    return self.items[__name]
