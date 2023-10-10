import glob
import yaml

class Parts():
  def __init__(this, variables, restrictions):
    this.variables = variables
    this.restrictions = restrictions

  def __call__(this, *args):
    loc = {}
    for i, arg in enumerate(args):
      loc[this.variables[i]] = arg

    for restriction in this.restrictions:
      exec(f'ret = ({restriction})', globals(), loc)
      if loc['ret'] is False:
        return False

    return True


def load_parts():
  parts = {}
  for fpath in glob.glob('parts/*.yaml'):
    with open(fpath, 'r') as f:
      parts |= yaml.safe_load(f)

  parts_func = {}
  for name, body in parts.items():
    name, *fargs = name.split()
    restrictions = body['制約'].split('and')
    parts_func[name] = Parts(fargs, restrictions)

  return parts_func


