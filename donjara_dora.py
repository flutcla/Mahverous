# mypy: disable-error-code="name-defined"
# https://www.asovision.com/donjara/doraemon/
# https://www.asovision.com/donjara/dx/pdf/score.pdf

import os
from mahverous.game import Game

from mahverous.hand import load_hands
from mahverous.init import init
from mahverous.part import load_parts
from mahverous.pie import load_pies
from mahverous.player import Player

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


def test() -> None:
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


# test()

Player([
    ドラえもん, ドラえもん, ドラえもん,
    しずか, しずか, しずか,
    ドラえもん, ドラえもんT, ドラえもん,
]).debug_check_hand()

Player([
    ドラえもん, ドラえもん, ドラえもん,
    ドラえもん, ドラえもん, ドラえもん,
    ドラえもん, ドラえもん, ドラえもん,
]).debug_check_hand()

Player([
    ドラえもん, のび太, しずか,
    ジャイアン, スネ夫, ドラミ,
    のび太のママ, 出木杉, ジャイアンのかあちゃん
]).debug_check_hand()

Player([
    ドラえもんT, のび太T, しずかT,
    ドラえもんT, のび太T, しずかT,
    ドラえもんT, のび太T, しずかT,
]).debug_check_hand()

Player([
    のび太, のび太T, のび太,
    のび太のママ, のび太のママ, のび太のママ,
    のび太のパパ, のび太のパパ, オールマイティ,
]).debug_check_hand()

# Player([
#     オールマイティ, オールマイティ, のび太,
#     のび太のママ, のび太のママ, のび太のママ,
#     のび太のパパ, のび太のパパ, のび太のパパ,
# ]).debug_check_hand()

Player([
    ドラえもん, ドラえもんT, のび太,
    のび太T, しずか, しずかT,
    ドラえもん, のび太, スネ夫
]).debug_check_hand()

game = Game()
game.play_cli()
