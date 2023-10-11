import glob
from itertools import combinations
from typing import Any
import yaml

from mahverous.part import load_parts
from mahverous.rule import load_rule
from mahverous.pie import Pie, load_pies


DIR = ''
rule = None


def init(working_dir: str):
  global DIR
  DIR = working_dir

  global rule
  rule = load_rule()

  for name, pie in load_pies().items():
    globals()[name] = pie

  for name, part in load_parts().items():
    globals()[name] = part


class Hand():
  def __init__(self, structure: list[int], restrictions: list[str]):
    self.structure = structure
    self.restrictions = restrictions
    self.variables = [chr(i) for i in range(ord('a'), ord('a') + rule['完成形の枚数'])]  # type: ignore

  def __call__(this, pies):
    return this.partial_check(pies)

  def partial_check(this, pies: list[Pie]):
    loc = {this.variables[i]: pie for i, pie in enumerate(pies)}
    for restriction in this.restrictions:
      try:
        exec(f'ret = ({restriction})', globals(), loc)
        if loc['ret'] is False:
          return False
      except NameError:
        return True
    return True

  def check(this, pies: list[Pie]):
    return this.check_rec([], pies, this.structure)

  def check_rec(
      this,
      current_pies: list[Pie],
      remaining_pies: list[Pie],
      sizes: list[int],
  ) -> bool:
    if not sizes and not remaining_pies:
      return True
    elif not sizes or not remaining_pies:
      return False

    current_size = sizes[0]
    if current_size > len(remaining_pies):
      return False

    pies_index = range(len(remaining_pies))
    current_index_conbinations = list(combinations(pies_index, current_size))
    for current_index_group in current_index_conbinations:
      current_group = [remaining_pies[i] for i in current_index_group]
      if not this.partial_check(current_pies + current_group):
        continue

      remaining = [
          remaining_pies[i] for i in pies_index if i not in current_index_group
      ]
      res = this.check_rec(
          current_pies + current_group,
          remaining,
          sizes[1:],
      )
      if res:
        return True
    return False


def load_hands(dir_name: str = 'hands') -> dict[str, Hand]:
  """Load hands from yaml files in the specified directory."""
  hands: dict[str, Any] = {}
  for fpath in glob.glob(f'{DIR}/{dir_name}/*.yaml'):
    with open(fpath, 'r') as f:
      hands |= yaml.safe_load(f)

  hands_func = {}
  for name, body in hands.items():
    structure = list(map(int, str(body['構造']).split(' ')))
    restrictions = body['制約']
    hands_func[name] = Hand(structure, restrictions)

  return hands_func


def check_hands(pies: list[Pie], dir_name='hands'):
  hands = load_hands(dir_name)
  result = []
  for name, hand in hands.items():
    if hand.check(pies):
      result.append(name)
  return result
