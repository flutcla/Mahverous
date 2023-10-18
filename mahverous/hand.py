import glob
from itertools import combinations
import os
import pickle
from typing import Any

import yaml

from mahverous.part import load_parts
from mahverous.pie import Pie, load_pies
from mahverous.restriction_builder import build_restriction
from mahverous.rule import Rule

DIR = ''


def init(working_dir: str) -> None:
  global DIR
  DIR = working_dir

  for name, pie in load_pies().items():
    globals()[name] = pie

  for name, part in load_parts().items():
    globals()[name] = part


class Hand():
  def __init__(self, name: str, structure: list[int], restrictions: list[str], prescript: list[str], postscript: list[str]) -> None:
    self.name = name
    self.structure = structure
    self.restrictions = restrictions
    self.prescript = prescript
    self.postscript = postscript
    self.variables = [chr(i) for i in range(ord('a'), ord('a') + Rule().hand_count)]

  def __call__(self, pies: list[Pie]) -> bool:
    result, result_pies = self.check(pies)
    return result

  def __str__(self) -> str:
    return self.name

  def __repr__(self) -> str:
    return str(self)

  def replace_allmighty(self, pies_list: list[list[Pie]]) -> list[list[Pie]]:
    all_pies = load_pies().copy()
    allmighty = all_pies.pop('オールマイティ')
    if allmighty not in pies_list[0]:
      return pies_list
    ret: list[list[Pie]] = []
    for pies in pies_list:
      idx = pies.index(allmighty)
      for pie in all_pies.values():
        ret.append([pie if i == idx else p for i, p in enumerate(pies)])
    return self.replace_allmighty(ret)

  def partial_check(self, pies: list[Pie]) -> tuple[bool, list[Pie]]:
    # オールマイティがある場合、全牌を試す
    all_pies = load_pies().copy()
    if 'オールマイティ' in all_pies.keys():
      allmighty = all_pies.pop('オールマイティ')
      if allmighty in pies:
        pies_list = self.replace_allmighty([pies])
      else:
        pies_list = [pies]
    else:
      pies_list = [pies]

    for pies in pies_list:
      loc = {self.variables[i]: pie for i, pie in enumerate(pies)}
      for restriction in self.restrictions:
        try:
          exec(f'ret = ({restriction})', globals(), loc)
          if loc['ret'] is False:
            break
        except NameError as e:
          non_defined_var = str(e).split("'")[1]
          if non_defined_var in self.variables:
            return True, []
          else:
            raise e
      else:
        # 制約を全て通過した場合 True を返す
        return True, pies
    return False, []

  def check(self, pies: list[Pie]) -> tuple[bool, list[Pie]]:
    result, result_pies = self.check_rec([], pies, self.structure)
    if result:
      self.run_scripts(result_pies)
    return result, result_pies

  def run_prescript(self) -> None:
    if self.prescript:
      for script in self.prescript:
        exec(script, globals() | locals(), globals())

  def run_postscript(self) -> None:
    if self.postscript:
      for script in self.postscript:
        exec(script, globals() | locals(), globals())

  def run_scripts(self, pies: list[Pie]) -> None:
    Rule().run_script = True
    self.run_prescript()
    self.partial_check(pies)
    self.run_postscript()
    Rule().run_script = False

  def check_rec(
      self,
      current_pies: list[Pie],
      remaining_pies: list[Pie],
      sizes: list[int],
  ) -> tuple[bool, list[Pie]]:
    if not sizes and not remaining_pies:
      return True, current_pies
    elif not sizes or not remaining_pies:
      return False, []

    current_size = sizes[0]
    if current_size > len(remaining_pies):
      return False, []

    pies_index = range(len(remaining_pies))
    current_index_conbinations = list(combinations(pies_index, current_size))
    for current_index_group in current_index_conbinations:
      current_group = [remaining_pies[i] for i in current_index_group]
      partial_res, _ = self.partial_check(current_pies + current_group)
      if not partial_res:
        continue

      remaining = [
          remaining_pies[i] for i in pies_index if i not in current_index_group
      ]
      res, res_pies = self.check_rec(
          current_pies + current_group,
          remaining,
          sizes[1:],
      )
      if res:
        return True, res_pies
    return False, []


HANDS_CACHE: dict[str, Hand] = {}


def load_hands(dir_name: str = 'hands') -> dict[str, Hand]:
  """Load hands from yaml files in the specified directory."""
  global HANDS_CACHE
  if HANDS_CACHE:
    return HANDS_CACHE
  hands: dict[str, Any] = {}
  for fpath in glob.glob(f'{DIR}/{dir_name}/*.yaml'):
    with open(fpath, 'r') as f:
      hands |= yaml.safe_load(f)

  hands_func: dict[str, Hand] = {}
  for name, body in hands.items():
    structure = list(map(int, str(body['構造']).split(' ')))
    restrictions = build_restriction(body['制約'])
    if '前処理' in body.keys():
      prescript: list[str] = body['前処理']
    else:
      prescript = []
    if '後処理' in body.keys():
      postscript: list[str] = body['後処理']
    else:
      postscript = []
    hands_func[name] = Hand(name, structure, restrictions, prescript, postscript)

  HANDS_CACHE = hands_func
  return hands_func


def check_hands(pies: list[Pie], dir_name: str = 'hands') -> list[Hand]:
  cache = get_from_cache(frozenset(pies))
  if cache is not None:
    result: list[Hand] = []
    for pies_, hand in cache:
      hand.check(pies_)
      result.append(hand)
    return result

  hands = load_hands(dir_name).values()
  result = []
  result_hands_list: list[list[Pie]] = []
  for hand in hands:
    res, result_hands = hand.check(pies)
    if res:
      result.append(hand)
      result_hands_list.append(result_hands)
  add_to_cache(frozenset(pies), [(pies_, hand) for pies_, hand in zip(result_hands_list, result)])
  return result


def add_to_cache(key: frozenset[Pie], value: list[tuple[list[Pie], Hand]]) -> None:
  DIR = os.environ['WORK_DIR']
  if os.path.exists(f'{DIR}/cache.pickle'):
    with open(f'{DIR}/cache.pickle', 'rb') as f:
      try:
        CHECK_CACHE = pickle.load(f)
      except (pickle.UnpicklingError, EOFError):
        return
    CHECK_CACHE[key] = value
  else:
    CHECK_CACHE = {key: value}
  with open(f'{DIR}/cache.pickle', 'wb') as f:
    pickle.dump(CHECK_CACHE, f)


def get_from_cache(key: frozenset[Pie]) -> list[tuple[list[Pie], Hand]] | None:
  DIR = os.environ['WORK_DIR']
  if not os.path.exists(f'{DIR}/cache.pickle'):
    return None
  with open(f'{DIR}/cache.pickle', 'rb') as f:
    try:
      CHECK_CACHE: dict[frozenset[Pie], list[tuple[list[Pie], Hand]]] = pickle.load(f)
    except (pickle.UnpicklingError, EOFError):
      return None
  return CHECK_CACHE.get(key, None)
