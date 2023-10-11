# mypy: disable-error-code="name-defined"

from timeit import timeit

import os
from mahverous.init import init
from mahverous.pie import load_pies
from mahverous.part import load_parts
from mahverous.hand import load_hands, check_hands

CWD = os.getcwd()
DIR = f'{CWD}/donjara_dora'

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


def check(hands, n=10):
  print('----------')
  print(hands)
  res = []

  def inner():
    if not res:
      for r in check_hands(hands):
        res.append(r)
  t = timeit(inner, number=n) / n
  print(res)
  print(f'平均所要時間: {t}')


check([
    ドラえもん, ドラえもん, ドラえもん,
    ドラえもん, ドラえもん, ドラえもん,
    ドラえもん, ドラえもん, ドラえもん,
])

check([
    ドラえもん, のび太, しずか,
    ジャイアン, スネ夫, ドラミ,
    のび太のママ, 出木杉, ジャイアンのかあちゃん
])

check([
    ドラえもんT, のび太T, しずかT,
    ドラえもんT, のび太T, しずかT,
    ドラえもんT, のび太T, しずかT,
])

check([
    のび太, のび太T, のび太,
    のび太のママ, のび太のママ, のび太のママ,
    のび太のパパ, のび太のパパ, オールマイティ,
])

check([
    オールマイティ, オールマイティ, のび太,
    のび太のママ, のび太のママ, のび太のママ,
    のび太のパパ, のび太のパパ, のび太のパパ,
], n=5)

check([
    ドラえもん, ドラえもんT, のび太,
    のび太T, しずか, しずかT,
    ドラえもん, のび太, スネ夫
])
