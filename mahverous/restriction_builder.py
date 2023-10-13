from collections import deque
from typing import Any, Generator
from sympy import Symbol, And, Or, to_cnf


class Builder():
  expr_to_symbol_dict: dict[str, Symbol]
  symbol_to_expr_dict: dict[Symbol, str]
  gen: Generator[Symbol, None, None]

  def __init__(self) -> None:
    self.expr_to_symbol_dict = {}
    self.symbol_to_expr_dict = {}
    self.gen = self.fresh_var_gen()

  def fresh_var_gen(self) -> Generator[Symbol, None, None]:
    i = 0
    while True:
      yield Symbol(f'var_{str(i)}_')
      i += 1

  def make_fresh_symbol(self) -> Symbol:
    return next(self.gen)

  def expr_to_symbol(self, expr: str):
    if expr in self.expr_to_symbol_dict.keys():
      return self.expr_to_symbol_dict[expr]
    else:
      symbol = self.make_fresh_symbol()
      self.expr_to_symbol_dict[expr] = symbol
      self.symbol_to_expr_dict[symbol] = expr
      return symbol

  def symbol_to_expr(self, symbol: Symbol):
    return self.symbol_to_expr_dict[symbol]

  def to_sympy(self, expr: list[Any]) -> list[Symbol | And | Or]:
    queue = deque(expr)
    ret: list[Symbol | And | Or] = []
    while queue:
      subexpr = queue.popleft()
      if subexpr == 'or':
        operands = queue.popleft()
        ret.append(Or(*self.to_sympy(operands)))
      elif subexpr == 'and':
        operands = queue.popleft()
        ret.append(And(*self.to_sympy(operands)))
      else:
        ret.append(self.expr_to_symbol(subexpr))
    return ret

  def build(self, expr):
    cnf_str = str(to_cnf(self.to_sympy(expr)[0]))
    closures = [s.strip(' ()') for s in cnf_str.split('&')]
    replaced_closures = []
    for closure in closures:
      replaced = closure.replace('|', ' or ').replace('~', ' not ')
      for symbol, expr in self.symbol_to_expr_dict.items():
        replaced = replaced.replace(str(symbol), expr)
      replaced_closures.append(replaced)
    return replaced_closures


def build_restriction(expr: list[Any]):
  return Builder().build(expr)


if __name__ == '__main__':
  expr = ['or', ['a', 'b', 'and', ['c', 'd', 'or', ['e', 'f', 'g'], 'or', ['h', 'i']]]]
  builder = Builder()
  print(builder.to_sympy(expr))
  print(builder.build(expr))
