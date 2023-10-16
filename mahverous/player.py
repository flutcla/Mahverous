import time

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

  def check_hand(self) -> list['mahverous.hand.Hand']:
    from mahverous.hand import check_hands
    Rule().run_prescript()
    result = check_hands(self.hand)
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
