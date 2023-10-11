# mypy: disable-error-code="name-defined"
# https://asobistore.jp/content/donjaracg/
# https://toy.bandai.co.jp/manuals/manual.php?id=2672881&time=1678931858&sig=1f27e3d145ad747d6328c5f16a4c4600

from timeit import timeit

import os
from mahverous.init import init
from mahverous.pie import load_pies
from mahverous.part import load_parts
from mahverous.hand import load_hands, check_hands


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


def test():
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


test()


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
    島村卯月, 緒方智絵里, 小早川紗枝,
    佐久間まゆ, 椎名法子, 道明寺歌鈴,
    中野有香, 前川みく, 遊佐こずえ,
])

check([
    島村卯月, 緒方智絵里, 小早川紗枝,
    佐久間まゆ, 椎名法子, 道明寺歌鈴,
    渋谷凛, 川島瑞樹, 桐生つかさ,
])

check([
    十時愛梨, 神崎蘭子, 渋谷凛,
    塩見周子, 島村卯月, 高垣楓,
    安部菜々, 本田未央, 北条加蓮,
])
