import yaml
import glob

class Pie():
  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)

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
