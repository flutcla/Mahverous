# mypy: disable-error-code="name-defined"
# https://toy.bandai.co.jp/series/donjara/item/detail/13292/

from timeit import timeit

import os
from mahverous.init import init
from mahverous.pie import load_pies
from mahverous.part import load_parts
from mahverous.hand import load_hands, check_hands

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


def test():
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
], n=1)
