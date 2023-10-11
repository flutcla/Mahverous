import glob
from itertools import permutations

import yaml


class Parts():
  def __init__(this, variables, restrictions, ordered):
    this.variables = variables
    this.restrictions = restrictions
    this.ordered = ordered

  def __call__(this, *args):
    # 順番が存在するパーツを検査する場合、全通り試す
    if this.ordered:
      args_perm = permutations(args)
    else:
      args_perm = [args]
    for args in args_perm:
      loc = {}
      for i, arg in enumerate(args):
        loc[this.variables[i]] = arg

      for restriction in this.restrictions:
        exec(f'ret = ({restriction})', globals(), loc)
        if loc['ret'] is False:
          break
      else:
        # 全制約を満たした場合 True を返す
        return True
    return False


def load_parts():
  parts = {}
  for fpath in glob.glob('parts/*.yaml'):
    with open(fpath, 'r') as f:
      parts |= yaml.safe_load(f)

  parts_func = {}
  for name, body in parts.items():
    name, *fargs = name.split()
    restrictions = body['制約']
    ordered = body['順番']
    parts_func[name] = Parts(fargs, restrictions, ordered)

  return parts_func
