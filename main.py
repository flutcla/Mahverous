# mypy: disable-error-code="name-defined"

from timeit import timeit

import load_hands
import load_parts
import load_pies
from load_pies import Pie

pies = load_pies.load_pies()
for name, pie in pies.items():
  globals()[name] = pie

parts = load_parts.load_parts()
for name, part in parts.items():
  globals()[name] = part

hands = load_hands.load_hands()
for name, hand in hands.items():
  globals()[name] = hand


assert 雀頭(白, 白)
assert 刻子(白, 白, 白)
assert not 刻子(白, 白, 中)
assert 順子(索1, 索2, 索3)
assert not 順子(白, 索2, 索3)
assert 順子(索4, 索2, 索3)

assert 大三元([
    白, 白, 白,
    發, 發, 發,
    中, 中, 中,
    筒1, 筒2, 筒3,
    萬7, 萬7
])

assert not 大三元([
    白, 白, 白,
    發, 發, 發,
    中, 中, 中,
    筒1, 筒5, 筒3,
    萬7, 萬7
])

assert 大四喜([
    東, 東, 東,
    南, 南, 南,
    西, 西, 西,
    北, 北, 北,
    白, 白
])

assert not 大四喜([
    筒1, 筒1, 筒1,
    南, 南, 南,
    西, 西, 西,
    北, 北, 北,
    白, 白
])

assert 字一色([
    東, 東, 東,
    南, 南, 南,
    西, 西, 西,
    北, 北, 北,
    白, 白
])


def check(hands: list[Pie]):
  print('----------')
  print(hands)
  t = timeit(lambda: load_hands.check_hands(hands), number=10) / 10
  print(load_hands.check_hands(hands))
  print(f'平均所要時間: {t}')


check([
    東, 東, 東,
    南, 南, 南,
    西, 西, 西,
    北, 北, 北,
    索1, 索1
])

check([
    索1, 索1,
    北, 北, 北,
    南, 南, 南,
    東, 東, 東,
    西, 西, 西
])

check([
    索1, 索1, 索1,
    索2, 索2, 索2,
    索3, 索3, 索3,
    索4, 索4, 索4,
    索5, 索5
])
