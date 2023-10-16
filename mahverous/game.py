import os
import random
from collections import deque
from typing import Self

from mahverous import hand as hand_
from mahverous import part as part_
from mahverous import pie as pie_
from mahverous import rule as rule_
from mahverous.pie import Pie, load_pies
from mahverous.player import Player
from mahverous.rule import Rule


class Game():
  instance: Self | None = None
  working_dir: str
  players: list[Player]
  wall_tiles: deque[Pie]
  current_player_index: int
  current_player: Player

  def __new__(cls, working_dir: str = '') -> Self:
    if cls.instance:
      return cls.instance  # type: ignore

    rule_.init(working_dir)
    pie_.init(working_dir)
    part_.init(working_dir)
    hand_.init(working_dir)

    cls.instance = super().__new__(cls)
    cls.working_dir = working_dir

    # 山の生成
    wall_tiles: list[Pie] = []
    pies = load_pies()
    for pie in pies.values():
      wall_tiles += [pie] * pie.count
    random.shuffle(wall_tiles)
    cls.wall_tiles = deque(wall_tiles)

    # プレイヤーの生成
    cls.hand_count = Rule().hand_count - 1
    cls.players = [
        Player(
            [cls.wall_tiles.popleft() for _ in range(cls.hand_count)],
            f'Player {i}'
        ) for i in range(Rule()['ゲーム']['プレイヤー数'])
    ]
    cls.current_player_index = 0
    cls.current_player = cls.players[0]

    return cls.instance

  def reset(self) -> None:
    self.instance = None
    self.instance = self.__new__(self.__class__, self.working_dir)  # type: ignore

  def increment_player(self) -> None:
    self.current_player_index = (self.current_player_index + 1) % len(self.players)
    self.current_player = self.players[self.current_player_index]

  def play_cli(self) -> None:
    while True:
      clear_console()
      self.current_player.sort_hand()
      print('-----------------------------------------------------')
      print(f'{self.current_player} の番です。残り枚数: {len(self.wall_tiles)}')
      print(f'{self.current_player.hand_to_str()}')
      tsumo = self.wall_tiles.popleft()
      print(f'{self.hand_count}(ツモ牌): {tsumo.to_str()}')

      # 成立判定
      msg = '役の判定中……'
      print(msg, end='', flush=True)
      res = self.current_player.check_hand(tsumo)
      print('\b' * len(msg) * 2, end='', flush=True)
      if res:
        print(f'{self.current_player} あがり！')
        print(f'{Rule().点数}点: {Rule().成立役}')  # type: ignore
        exit()

      while True:
        try:
          pop_index_str = input('捨てたい牌の番号を入力してください: ')
          pop_index = int(pop_index_str)
          if pop_index > self.hand_count:
            raise ValueError
          break
        except Exception:
          print('不正な入力です。', end='')
          continue

      if pop_index != self.hand_count:
        pop_pie = self.current_player.hand.pop(pop_index)
        self.current_player.hand.append(tsumo)
      else:
        pop_pie = tsumo
      print(f'{pop_pie.to_str()} を捨てました')
      self.increment_player()


def clear_console() -> None:
  os.system("cls" if os.name in ("nt", "dos") else "clear")
