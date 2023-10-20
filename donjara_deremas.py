# mypy: disable-error-code="name-defined"
# https://asobistore.jp/content/donjaracg/
# https://toy.bandai.co.jp/manuals/manual.php?id=2672881&time=1678931858&sig=1f27e3d145ad747d6328c5f16a4c4600

import os

from mahverous.game import Game
from mahverous.hand import load_hands
from mahverous.init import init
from mahverous.part import load_parts
from mahverous.pie import load_pies
from mahverous.player import Player

CWD = os.getcwd()
DIR = f'{CWD}/donjara_deremas'

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
  assert アンサンブルセット([
      島村卯月, 緒方智絵里, 小早川紗枝,
      佐久間まゆ, 椎名法子, 道明寺歌鈴,
      中野有香, 前川みく, 遊佐こずえ,
  ])
  assert not アンサンブルセット([
      島村卯月, 緒方智絵里, 小早川紗枝,
      佐久間まゆ, 椎名法子, 道明寺歌鈴,
      中野有香, 前川みく, 安部菜々,
  ])
  assert シンフォニーセット([
      島村卯月, 緒方智絵里, 小早川紗枝,
      佐久間まゆ, 椎名法子, 道明寺歌鈴,
      安部菜々, 輿水幸子, 小日向美穂,
  ])
  assert not シンフォニーセット([
      島村卯月, 緒方智絵里, 小早川紗枝,
      佐久間まゆ, 椎名法子, 道明寺歌鈴,
      渋谷凛, 川島瑞樹, 桐生つかさ,
  ])
  assert リハーサルライブセット([
      島村卯月, 緒方智絵里, 小早川紗枝,
      佐久間まゆ, 椎名法子, 道明寺歌鈴,
      渋谷凛, 川島瑞樹, 桐生つかさ,
  ])
  assert シンデレラガールズユニット([
      十時愛梨, 神崎蘭子, 渋谷凛,
      塩見周子, 島村卯月, 高垣楓,
      安部菜々, 本田未央, 北条加蓮,
  ])
  assert C5(
      小日向美穂, 安部菜々, 島村卯月, 双葉杏, 前川みく
  )
  assert ファイブスターユニット([
      小日向美穂, 安部菜々, 島村卯月, 双葉杏, 前川みく,
      渋谷凛, 高垣楓, 鷹富士茄子, 二宮飛鳥
  ])


# test()

Player([
    島村卯月, 緒方智絵里, 小早川紗枝,
    佐久間まゆ, 椎名法子, 道明寺歌鈴,
    中野有香, 前川みく, 遊佐こずえ,
]).debug_check_hand()

Player([
    島村卯月, 緒方智絵里, 小早川紗枝,
    佐久間まゆ, 椎名法子, 道明寺歌鈴,
    渋谷凛, 川島瑞樹, 桐生つかさ,
]).debug_check_hand()

Player([
    十時愛梨, 神崎蘭子, 渋谷凛,
    塩見周子, 島村卯月, 高垣楓,
    安部菜々, 本田未央, 北条加蓮,
]).debug_check_hand()

Player([
    小日向美穂, 安部菜々, 島村卯月, 双葉杏, 前川みく,
    渋谷凛, 高垣楓, 鷹富士茄子, 二宮飛鳥,
]).debug_check_hand()

Player([
    難波笑美, 緒方智絵里,
    佐藤心, 安部菜々, 高垣楓, 片桐早苗, 三船美優,
    一ノ瀬志希, 宮本フレデリカ,
]).debug_check_hand()

Player([
    宮本フレデリカ, 島村卯月, 喜多日菜子,
    小日向美穂, 島村卯月, 緒方智絵里,
    渋谷凛, 島村卯月, 本田未央,
]).debug_check_hand()

Player([
    神崎蘭子, 鷺沢文香,
    藤原肇, 三船美優, 桐生つかさ, 星輝子,
    渋谷凛, 島村卯月, 本田未央,
]).debug_check_hand()

game = Game()
game.play_cli()
