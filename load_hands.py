import glob
from typing import Any, Generator, Literal
import yaml

import load_rule
import load_pies
from load_pies import Pie
import load_parts

rule = load_rule.load_rule()

pies = load_pies.load_pies()
for name, pie in pies.items():
  globals()[name] = pie

parts = load_parts.load_parts()
for name, part in parts.items():
  globals()[name] = part

class Hand():
  variables = [chr(i) for i in range(ord('a'), ord('a')+rule['完成形の枚数'])]
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

  # 牌を send で受け取り、満たすなら StopIteration で True を、満たさないなら False を返すジェネレータ
  def check_it(this) -> Generator[Literal[True], Pie, bool]:
    i = 0
    loc = {}
    while i < len(this.variables):
      pie: Pie = yield True
      loc[this.variables[i]] = pie
      i += 1
      for restriction in this.restrictions:
        try:
          exec(f'ret = ({restriction})', globals(), loc)
          if loc['ret'] is False:
            return False
        except Exception as e:
          continue
    return True

def load_hands() -> dict[str, Hand]:
  hands: dict[str, Any] = {}
  for fpath in glob.glob('hands/*.yaml'):
    with open(fpath, 'r') as f:
      hands |= yaml.safe_load(f)

  hands_func = {}
  for name, body in hands.items():
    restrictions = body['制約'].split('and')
    hands_func[name] = Hand(restrictions)

  return hands_func

def check_hands(pies: list[Pie]):
  hands = load_hands()
  result = []
  for name, hand in hands.items():
    for pie in pies:
      if check_rec(hand, [], pie, pies):
        result.append(name)
        break
  return result

def check_rec(hand: Hand, current_pies: list[Pie], next_pie: Pie, left_pies: list[Pie]):
  current_pies = current_pies.copy()
  left_pies = left_pies.copy()
  it = hand.check_it()
  next(it)
  current_pies.append(next_pie)
  left_pies.remove(next_pie)
  try:
    [it.send(pie) for pie in current_pies]
    for pie in left_pies:
      if check_rec(hand, current_pies, pie, left_pies):
        return True
  except StopIteration as e:
    return e.value
