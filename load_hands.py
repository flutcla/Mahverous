# mypy: disable-error-code="name-defined"

import glob
from itertools import combinations
from typing import Any
from concurrent.futures import ProcessPoolExecutor

import yaml

import load_parts
import load_pies
import load_rule
from load_pies import Pie

rule = load_rule.load_rule()

for name, pie in load_pies.load_pies().items():
  globals()[name] = pie

for name, part in load_parts.load_parts().items():
  globals()[name] = part


class Hand():
  variables = [chr(i) for i in range(ord('a'), ord('a') + rule['完成形の枚数'])]

  def __init__(self, structure: list[int], restrictions: list[str]):
    self.structure = structure
    self.restrictions = restrictions

  def __call__(this, pies):
    return this.partial_check(pies)

  def partial_check(this, pies: list[Pie]):
    loc = {this.variables[i]: pie for i, pie in enumerate(pies)}
    for restriction in this.restrictions:
      try:
        exec(f'ret = ({restriction})', globals(), loc)
        if loc['ret'] is False:
          return False
      except Exception:
        return True
    return True

  def check(this, pies: list[Pie]):
    # return this.check_rec([], pies, this.structure)
    return this.check_rec_parallel([], pies, this.structure, max_workers=8)

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

  def worker(this, current_pies, remaining_pies, sizes, current_index_group):
    current_group = [remaining_pies[i] for i in current_index_group]
    if not this.partial_check(current_pies + current_group):
        return False

    pies_index = range(len(remaining_pies))
    remaining = [
        remaining_pies[i] for i in pies_index if i not in current_index_group
    ]

    return this.check_rec(
        current_pies + current_group,
        remaining,
        sizes[1:],
    )

  def check_rec_parallel(
      this,
      current_pies,
      remaining_pies,
      sizes,
      max_workers=4
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

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(
            this.worker,
            [current_pies] * len(current_index_conbinations),
            [remaining_pies] * len(current_index_conbinations),
            [sizes] * len(current_index_conbinations),
            current_index_conbinations,
        ))

    return any(results)


def load_hands() -> dict[str, Hand]:
  hands: dict[str, Any] = {}
  for fpath in glob.glob('hands/*.yaml'):
    with open(fpath, 'r') as f:
      hands |= yaml.safe_load(f)

  hands_func = {}
  for name, body in hands.items():
    structure = list(map(int, body['構造'].split(' ')))
    restrictions = body['制約'].split('and')
    hands_func[name] = Hand(structure, restrictions)

  return hands_func


def check_hands(pies: list[Pie]):
  hands = load_hands()
  result = []
  for name, hand in hands.items():
    if hand.check(pies):
      result.append(name)
  return result


if __name__ == '__main__':

  hands = load_hands()
  for name, hand in hands.items():
    globals()[name] = hand

  assert 大三元.partial_check([
      白, 白, 白,
  ])
  assert not 大三元.partial_check([
      白, 發, 發,
  ])

  assert not 大三元.check([
      東, 東, 東,
      南, 南, 南,
      西, 西, 西,
      北, 北, 北,
      白, 白
  ])

  assert 大四喜.check([
      東, 東, 東,
      南, 南, 南,
      西, 西, 西,
      北, 北, 白,
      白, 北
  ])

  assert 大四喜.check([
      白, 白,
      北, 北, 北,
      西, 西, 西,
      南, 南, 南,
      東, 東, 東,
  ])

  assert 大三元.check([
      索4, 索2, 索3,
      中, 中, 中,
      發, 發, 發,
      筒4, 筒4,
      白, 白, 白,
  ])

  assert 七対子.check([
      索1, 索1,
      索2, 索2,
      索3, 索3,
      索4, 索4,
      索5, 索5,
      索6, 索6,
      索7, 索7,
  ])

  assert not 七対子.check([
      東, 東, 東,
      南, 南, 南,
      西, 西, 西,
      北, 北, 北,
      白, 白
  ])
