# mypy: disable-error-code="name-defined"
# https://toy.bandai.co.jp/series/donjara/item/detail/13292/

import os

from mahverous.game import Game
from mahverous.hand import load_hands
from mahverous.init import init
from mahverous.part import load_parts
from mahverous.pie import load_pies
from mahverous.player import Player

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


# test()


Player([
    キラー, キラー, キラー,
    カイドウ, カイドウ, カイドウ,
    # モンキーDルフィ, ロロノアゾロ, ナミ,
    モンキーDルフィ, トラファルガーロー, ユースタスキッド,
]).debug_check_hand()

Player([
    モンキーDルフィ, モンキーDルフィ, モンキーDルフィ,
    ロロノアゾロ, ロロノアゾロ, ロロノアゾロ,
    サンジ, サンジ, サンジ,
]).debug_check_hand()

game = Game()
game.play_cli()
