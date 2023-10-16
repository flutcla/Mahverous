import glob
from itertools import permutations
from typing import Any

import yaml

from mahverous.pie import Pie, load_pies
from mahverous.rule import Rule
from mahverous.restriction_builder import build_restriction

DIR = ''


def init(working_dir: str) -> None:
  global DIR
  DIR = working_dir
  for name, pie in load_pies().items():
    globals()[name] = pie

  for name, part in load_parts().items():
    globals()[name] = part

  Rule()


class Part():
  """A class representing a part."""
  def __init__(self, variables: list[str], restrictions: list[str], prescrpt: list[str], postscript: list[str], ordered: bool) -> None:
    self.variables = variables
    self.restrictions = restrictions
    self.prescript = prescrpt
    self.postscript = postscript
    self.ordered = ordered

  def run_prescript(self) -> None:
    if self.prescript:
      for script in self.prescript:
        exec(script, globals())

  def run_postscript(self) -> None:
    if self.postscript:
      for script in self.postscript:
        exec(script, globals())

  def __call__(self, *args: Pie) -> bool:
    if Rule().run_script:
      self.run_prescript()
    # 順番が存在するパーツを検査する場合、全通り試す
    if self.ordered:
      args_perm = list(permutations(args))
    else:
      args_perm = [args]
    for args in args_perm:
      loc = {self.variables[i]: arg for i, arg in enumerate(args)}

      for restriction in self.restrictions:
        exec(f'ret = ({restriction})', globals(), loc)
        if loc['ret'] is False:
          break
      else:
        # 全制約を満たした場合 True を返す
        if Rule().run_script:
          self.run_postscript()
        return True
    return False


PARTS_CACHE: dict[str, Part] = {}


def load_parts(dir_name: str = 'parts') -> dict[str, Part]:
  """Load parts from yaml files in the specified directory."""
  global PARTS_CACHE
  if PARTS_CACHE:
    return PARTS_CACHE
  parts: dict[str, Any] = {}
  for fpath in glob.glob(f'{DIR}/{dir_name}/*.yaml'):
    with open(fpath, 'r') as f:
      parts |= yaml.safe_load(f)

  parts_func: dict[str, Part] = {}
  for name, body in parts.items():
    name, *fargs = name.split()
    restrictions = build_restriction(body['制約'])
    if '前処理' in body.keys():
      prescript: list[str] = body['前処理']
    else:
      prescript = []
    if '後処理' in body.keys():
      postscript: list[str] = body['後処理']
    else:
      postscript = []
    ordered = body.get('順番', False)
    parts_func[name] = Part(fargs, restrictions, prescript, postscript, ordered)

  PARTS_CACHE = parts_func
  return parts_func
