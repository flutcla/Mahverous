import asyncio
import itertools
import os
import random
from collections import deque
from typing import Self
from concurrent.futures import ProcessPoolExecutor

from mahverous import hand as hand_
from mahverous import part as part_
from mahverous import pie as pie_
from mahverous import rule as rule_
from mahverous.pie import Pie, load_pies
from mahverous.player import Player
from mahverous.rule import Rule
random.seed(0)
loop = asyncio.get_event_loop()
executor = ProcessPoolExecutor(max_workers=5)


class Game():
  instance: Self | None = None
  working_dir: str
  players: list[Player]
  wall_tiles: deque[Pie]
  current_player_index: int
  current_player: Player
  game_count: int
  current_game_count: int

  def __new__(cls, working_dir: str = '') -> Self:
    if cls.instance:
      return cls.instance  # type: ignore

    rule_.init(working_dir)
    pie_.init(working_dir)
    part_.init(working_dir)
    hand_.init(working_dir)

    cls.instance = super().__new__(cls)
    cls.working_dir = working_dir

    cls.game_count = Rule()['ゲーム']['局数']
    cls.current_game_count = 1

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
            f'Player {i}',
            Rule()['ゲーム']['初期点数']
        ) for i in range(Rule()['ゲーム']['プレイヤー数'])
    ]
    cls.current_player_index = 0
    cls.current_player = cls.players[0]

    return cls.instance

  def reset(self) -> None:
    self.current_game_count += 1

    wall_tiles: list[Pie] = []
    pies = load_pies()
    for pie in pies.values():
      wall_tiles += [pie] * pie.count
    random.shuffle(wall_tiles)
    self.wall_tiles = deque(wall_tiles)

    for player in self.players:
      player.hand = [self.wall_tiles.popleft() for _ in range(self.hand_count)]

    self.current_player_index = (self.current_game_count - 1) % len(self.players)
    self.current_player = self.players[self.current_player_index]

  def increment_player(self) -> None:
    self.current_player_index = (self.current_player_index + 1) % len(self.players)
    self.current_player = self.players[self.current_player_index]

  def play_cli(self) -> None:
    while True:
      wait_for_enter(f'{self.current_player} の番です。残り枚数: {len(self.wall_tiles)}')

      self.current_player.sort_hand()
      print_line()
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
        self.game_end(win_player=self.current_player, agari_pie=tsumo)

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
      print(f'{pop_pie.to_str()} を捨てました。')

      # 判定の先読み
      for p in itertools.islice(self.wall_tiles, 0, 5):
        loop.run_in_executor(executor, self.current_player.check_hand, p)

      # ロン判定
      if not pop_pie.is_allmighty:
        for player in self.players:
          if player == self.current_player:
            continue
          msg = '役の判定中……'
          print(msg, end='', flush=True)
          res = player.check_hand(pop_pie)
          print('\b' * len(msg) * 2, end='', flush=True)
          if res:
            self.game_end(win_player=player, agari_pie=pop_pie, ron=self.current_player)

      self.increment_player()
      input('Enterを押してください......')
      clear_console()

  def game_end(self, win_player: Player, agari_pie: Pie, ron: Player | None = None) -> None:
    score = Rule().点数  # type: ignore
    score_strings = ['', '- 点数表 -']
    win_player.score += score
    if ron:
      ron.score -= score
      for player in self.players:
        if player == win_player:
          score_strings.append(f'{player}, {player.score} (+{score})')
        elif player == ron:
          score_strings.append(f'{player}, {player.score} (-{score})')
        else:
          score_strings.append(f'{player}, {player.score}')
    else:
      change_score = score // (len(self.players) - 1)
      for player in self.players:
        if player == win_player:
          score_strings.append(f'{player}, {player.score} (+{score})')
        else:
          player.score -= change_score
          score_strings.append(f'{player}, {player.score} (-{change_score})')

    win_player.sort_hand()
    wait_for_enter('\n'.join([
        f'== {win_player} あがり！ ==',
        f'{win_player.hand_to_str()} | {agari_pie.to_str()}',
        f'{score}点: {Rule().成立役}',  # type: ignore
        '\n'.join(score_strings)
    ]))

    if self.current_game_count == self.game_count:
      exit()

    self.reset()
    wait_for_enter(f'第 {self.current_game_count} 局を開始します。')
    self.play_cli()


def print_line() -> None:
  print('-' * os.get_terminal_size().columns)


def clear_console() -> None:
  os.system("cls" if os.name in ("nt", "dos") else "clear")


def wait_for_enter(message: str = '') -> None:
  clear_console()
  print_line()
  if message:
    print(message)
  input('Enterを押してください......')
  clear_console()
