import time
from typing import Any

import mahverous
from mahverous.pie import Pie
from mahverous.rule import Rule


class Player():
  name: str
  hand: list[Pie]

  def __init__(self, hand: list[Pie], name: str = 'Anonymous') -> None:
    self.hand = hand
    self.name = name

  def __str__(self) -> str:
    return self.name

  def check_hand(self, tsumo: Pie | None = None) -> list['mahverous.hand.Hand']:
    from mahverous.hand import check_hands
    Rule().run_prescript()
    if tsumo:
      result = check_hands(self.hand + [tsumo])
    else:
      result = check_hands(self.hand)
    if result:
      Rule().run_postscript()
    return result

  def debug_check_hand(self) -> None:
    print('----------')
    print(f'手牌: {self.hand}')
    current_time = time.time()
    res = self.check_hand()
    print(f'成立役: {res}')
    deltat = time.time() - current_time
    print(f'所要時間: {deltat}')

  def hand_to_str(self) -> str:
    strs = []
    for i, pie in enumerate(self.hand):
      s = f'{i}: {pie.to_str()}'
      strs.append(s)
    return ' | '.join(strs)

  def sort_hand(self) -> None:
    if 'ゲーム' in Rule().items.keys() and '整列させるパラメータ' in Rule()['ゲーム']:
      def key(pie: Pie) -> tuple[Any, ...]:
        return tuple(getattr(pie, param) for param in Rule()['ゲーム']['整列させるパラメータ'])
      self.hand.sort(key=key)
