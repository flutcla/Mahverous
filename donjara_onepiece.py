# mypy: disable-error-code="name-defined"
# https://toy.bandai.co.jp/series/donjara/item/detail/13292/

from timeit import timeit

import os
from mahverous.init import init
from mahverous.pie import Pie, load_pies
from mahverous.part import load_parts
from mahverous.hand import Hand, load_hands, check_hands, get_point

CWD = os.getcwd()
DIR = f'{CWD}/donjara_onepiece'

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
  assert 大集結セット([
      ナミ, ナミ, ナミ,
      ウソップ, ウソップ, ウソップ,
      サンジ, サンジ, サンジ,
  ])
  assert not 大集結セット([
      ナミ, ナミ, ナミ,
      ウソップ, ウソップ, ウソップ,
      ヒナ, ヒナ, ヒナ,
  ])
  assert 麦わらの一味セット([
      ナミ, ナミ, ナミ,
      ウソップ, ウソップ, ウソップ,
      モンキーDルフィ, トラファルガーロー, ユースタスキッド,
  ])
  assert not 麦わらの一味セット([
      ナミ, ナミ, ナミ,
      ウソップ, ウソップ, ヒナ,
      モンキーDルフィ, トラファルガーロー, ユースタスキッド,
  ])
  assert 麦わらの一味セット([
      ナミ, ナミ, ナミ,
      ウソップ, ウソップ, ウソップ,
      サボ, ハック, コアラ,
  ])
  assert 麦わらの一味セット([
      ナミ, ナミ, ナミ,
      ウソップ, ウソップ, ウソップ,
      トラファルガーロー, スモーカー, フランキー,
  ])
  assert 最悪の世代セット([
      キラー, キラー, キラー,
      ウルージ, ウルージ, ウルージ,
      シャーロットリンリン, カイドウ, モンキーDルフィ,
  ])
  assert not 最悪の世代セット([
      キラー, キラー, キラー,
      ウルージ, ウルージ, カイドウ,
      シャーロットリンリン, カイドウ, モンキーDルフィ,
  ])
  assert 新世界の海賊たちセット([
      キラー, キラー, キラー,
      カイドウ, カイドウ, カイドウ,
      モンキーDルフィ, ロロノアゾロ, ナミ,
  ])
  assert 新世界の海賊たちセット([
      キラー, キラー, キラー,
      カイドウ, カイドウ, カイドウ,
      キング, Xドレーク, スクラッチメンアプー,
  ])
  assert not 新世界の海賊たちセット([
      キラー, キラー, キラー,
      カイドウ, カイドウ, カイドウ,
      キング, Xドレーク, サボ,
  ])


def check(pies: list[Pie]) -> None:
  print('----------')
  print(pies)
  res: list[Hand] = []

  def inner() -> None:
    if not res:
      for r in check_hands(pies):
        res.append(r)
  t = timeit(inner, number=1)
  print(f'成立役: {res}')
  print(f'得点: {get_point(res)}')
  print(f'所要時間: {t}')


check([
    キラー, キラー, キラー,
    カイドウ, カイドウ, カイドウ,
    モンキーDルフィ, ロロノアゾロ, ナミ,
])

check([
    モンキーDルフィ, モンキーDルフィ, モンキーDルフィ,
    ロロノアゾロ, ロロノアゾロ, ロロノアゾロ,
    サンジ, サンジ, サンジ,
])

check([
    モンキーDルフィ, モンキーDルフィ, モンキーDルフィ,
    ロロノアゾロ, ロロノアゾロ, ロロノアゾロ,
    カイドウ, シャーロットリンリン, オールマイティ,
])
