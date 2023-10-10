import yaml
import glob
from pprint import pprint

pies = {}
for fpath in glob.glob('pie/*.yaml'):
  with open(fpath, 'r') as f:
    pie = yaml.safe_load(f)
    pies |= pie

parts = {}
for fpath in glob.glob('parts/*.yaml'):
  with open(fpath, 'r') as f:
    parts |= yaml.safe_load(f)

parts_func = {}
for name, body in parts.items():
  fname, *fargs = name.split()
  def func(*args):
    loc = {}
    for i, arg in enumerate(fargs):
      print(args[i])
      exec(f'{arg} = {args[i]}', globals(), loc)
    exec(f'ret = {body['制約']}', globals(), loc)
    return loc['ret']
  parts_func[fname] = func

pprint(parts_func['雀頭'](pies['白'], pies['白']))
pprint(parts_func['雀頭'](pies['白'], pies['中']))
pprint(parts_func['雀頭'](1, 2))
