# mypy: disable-error-code="name-defined"

import os
from timeit import timeit

from mahverous.hand import check_hands, load_hands
from mahverous.init import init
from mahverous.part import load_parts
from mahverous.pie import Pie, load_pies

CWD = os.getcwd()
DIR = f'{CWD}/mahjong'

init(DIR)

pies = load_pies()
for name, pie in pies.items():
  locals()[name] = pie

parts = load_parts()
for name, part in parts.items():
  locals()[name] = part

hands = load_hands()
for name, hand in hands.items():
  locals()[name] = hand


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


def check(pies: list[Pie]) -> None:
  print('----------')
  print(pies)
  t = timeit(lambda: check_hands(pies), number=1)
  print(check_hands(pies))
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

check([
    索1, 索1,
    索2, 索2,
    索3, 索3,
    索4, 索4,
    索5, 索5,
    索6, 索6,
    索7, 索7,
])

check([
    索1, 索2, 索3,
    索4, 索5, 索6,
    索7, 索8, 索9,
    筒1, 筒2, 筒3,
    筒4, 筒5
])
