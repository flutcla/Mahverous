import yaml
import glob

class Pie():
  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)

  def __repr__(self):
    return f'Pie({self.__dict__})'

  def __eq__(self, __value: object) -> bool:
    if not isinstance(__value, Pie):
      return False
    return self.__dict__ == __value.__dict__

def load_pies():
  pies = {}
  for fpath in glob.glob('pie/*.yaml'):
    with open(fpath, 'r') as f:
      pie = yaml.safe_load(f)
      pies |= pie

  ret = {}
  for k, v in pies.items():
    ret[k] = Pie(**v)
  return ret
