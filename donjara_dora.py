# mypy: disable-error-code="name-defined"
# https://www.asovision.com/donjara/doraemon/
# https://www.asovision.com/donjara/dx/pdf/score.pdf

from timeit import timeit

import os
from mahverous.init import init
from mahverous.pie import load_pies
from mahverous.part import load_parts
from mahverous.hand import load_hands, check_hands, get_point

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


def test():
  assert ミラクルセット([
      ドラえもん, ドラえもん, ドラえもん,
      ドラえもんT, ドラえもん, ドラえもん,
      ドラえもん, ドラえもんT, ドラえもん,
  ])
  assert not ミラクルセット([
      ドラえもん, ドラえもん, ドラえもん,
      ドラえもんT, ドラえもん, ドラえもん,
      ドラえもん, ドラえもんT, ジャイアン,
  ])
  assert hands['2個1個セット']([
      ドラえもん, ドラえもん, ドラえもん,
      しずか, しずか, しずか,
      ドラえもん, ドラえもんT, ドラえもん,
  ])
  assert not hands['2個1個セット']([
      ドラえもん, ドラえもん, ドラえもん,
      しずか, しずか, しずか,
      ジャイアン, ジャイアン, ジャイアン,
  ])
  assert いろいろセット([
      ドラえもん, ドラえもん, ドラえもん,
      しずか, しずか, しずか,
      ジャイアン, ジャイアン, ジャイアン,
  ])
  assert not いろいろセット([
      ドラえもん, ドラえもん, ドラえもん,
      しずか, しずか, しずか,
      ジャイアン, ジャイアン, ジャイコ,
  ])
  assert 大集合セット([
      ドラえもん, のび太, しずか,
      ジャイアン, スネ夫, ドラミ,
      のび太のママ, 出木杉, ジャイアンのかあちゃん,
  ])
  assert not 大集合セット([
      ドラえもん, のび太, しずか,
      ジャイアン, スネ夫, ドラミ,
      のび太のママ, 出木杉, 出木杉,
  ])
  assert 空の旅セット([
      ドラえもんT, のび太T, しずかT,
      ドラえもんT, のび太T, しずかT,
      ドラえもんT, のび太T, しずかT,
  ])
  print('----------')
  assert not 空の旅セット([
      ドラえもんT, のび太T, しずかT,
      ドラえもんT, のび太T, しずかT,
      ドラえもんT, のび太T, しずか,
  ])
  assert 野比家セット([
      のび太, のび太T, のび太,
      のび太のママ, のび太のママ, のび太のママ,
      のび太のパパ, のび太のパパ, のび太のパパ,
  ])
  assert not 野比家セット([
      のび太, のび太T, のび太,
      のび太のママ, のび太のママ, のび太のママ,
      ジャイアンのかあちゃん, ジャイアンのかあちゃん, ジャイアンのかあちゃん,
  ])
  assert 剛田家セット([
      ジャイアン, ジャイアン, ジャイアン,
      ジャイコ, ジャイコ, ジャイコ,
      ジャイアンのかあちゃん, ジャイアンのかあちゃん, ジャイアンのかあちゃん,
  ])
  assert not 剛田家セット([
      ジャイアン, ジャイアン, ジャイアン,
      ジャイコ, ジャイコ, ジャイコ,
      のび太のママ, のび太のママ, のび太のママ,
  ])
  assert 未来セット([
      ドラえもん, ドラえもんT, ドラえもん,
      ドラミ, ドラミ, ドラミT,
      セワシ, セワシ, セワシ,
  ])
  assert not 未来セット([
      ドラえもん, ドラえもんT, ドラえもん,
      ドラミ, ドラミ, ドラミT,
      ドラえもん, ドラえもん, ドラえもん,
  ])
  assert ジャイアンリサイタル([
      歌うジャイアン, 歌うジャイアン, 歌うジャイアン,
      ドラえもん, ドラえもん, ドラえもん,
      ドラミ, ドラミ, ドラミ,
  ])
  assert not ジャイアンリサイタル([
      歌うジャイアン, 歌うジャイアン, 歌うジャイアン,
      ジャイアン, ジャイアンT, ジャイアン,
      ドラミ, ドラミ, ドラミ,
  ])
  assert なかよしセット([
      のび太, のび太, のび太,
      ドラえもん, ドラえもん, ドラえもん,
      しずか, しずか, しずか,
  ])
  assert not なかよしセット([
      のび太, のび太, のび太,
      ドラミ, ドラミ, ドラミ,
      しずか, しずか, しずか,
  ])
  assert 大好きセット([
      のび太, のび太, のび太,
      ドラミ, ドラミ, ドラミ,
      しずか, しずか, しずか,
  ])
  assert not 大好きセット([
      のび太, のび太, のび太,
      ドラえもん, ドラえもん, ドラえもん,
      ドラミ, ドラミ, ドラミ,
  ])
  assert お前の物は俺の物俺の物は俺の物セット([
      ジャイアン, ジャイアンT, ジャイアン,
      スネ夫, スネ夫, スネ夫T,
      ドラえもん, ドラえもん, ドラえもん,
  ])
  assert not お前の物は俺の物俺の物は俺の物セット([
      ジャイアン, ジャイアンT, ジャイアン,
      ドラミ, ドラミ, ドラミ,
      ドラえもん, ドラえもん, ドラえもん,
  ])


test()


def check(hands, n=1):
  print('----------')
  print(hands)
  res = []

  def inner():
    if not res:
      for r in check_hands(hands):
        res.append(r)
  t = timeit(inner, number=1)
  print(f'成立役: {res}')
  print(f'得点: {get_point(res)}')
  print(f'所要時間: {t}')


check([
    ドラえもん, ドラえもん, ドラえもん,
    しずか, しずか, しずか,
    ドラえもん, ドラえもんT, ドラえもん,
])

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
])

check([
    ドラえもん, ドラえもんT, のび太,
    のび太T, しずか, しずかT,
    ドラえもん, のび太, スネ夫
])
