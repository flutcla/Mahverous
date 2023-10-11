import glob
from itertools import permutations
from typing import Any

import yaml

from mahverous.pie import load_pies

DIR = ''


def init(working_dir: str):
  global DIR
  DIR = working_dir
  for name, pie in load_pies().items():
    globals()[name] = pie


class Part():
  """A class representing a part."""
  def __init__(this, variables, restrictions, ordered):
    this.variables = variables
    this.restrictions = restrictions
    this.ordered = ordered

  def __call__(this, *args):
    # 順番が存在するパーツを検査する場合、全通り試す
    if this.ordered:
      args_perm = list(permutations(args))
    else:
      args_perm = [args]
    for args in args_perm:
      loc = {this.variables[i]: arg for i, arg in enumerate(args)}

      for restriction in this.restrictions:
        exec(f'ret = ({restriction})', globals(), loc)
        if loc['ret'] is False:
          break
      else:
        # 全制約を満たした場合 True を返す
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
    restrictions = body['制約']
    ordered = body['順番']
    parts_func[name] = Part(fargs, restrictions, ordered)

  PARTS_CACHE = parts_func
  return parts_func
