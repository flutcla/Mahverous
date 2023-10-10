import glob
import yaml

import load_pies
import load_parts

pies = load_pies.load_pies()
for name, pie in pies.items():
  globals()[name] = pie

parts = load_parts.load_parts()
for name, part in parts.items():
  globals()[name] = part

class Hand():
  variables = [chr(i) for i in range(ord('a'), ord('a')+15)]
  def __init__(self, restrictions):
    self.restrictions = restrictions

  def __call__(this, *args):
    loc = {}
    for i, arg in enumerate(args):
      loc[this.variables[i]] = arg
    for restriction in this.restrictions:
      exec(f'ret = ({restriction})', globals(), loc)
      if loc['ret'] is False:
        return False

    return True

def load_hands():
  hands = {}
  for fpath in glob.glob('hands/*.yaml'):
    with open(fpath, 'r') as f:
      hands |= yaml.safe_load(f)

  hands_func = {}
  for name, body in hands.items():
    restrictions = body['制約'].split('and')
    hands_func[name] = Hand(restrictions)

  return hands_func