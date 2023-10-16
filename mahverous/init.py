from mahverous import hand, part, pie, rule


def init(working_dir: str) -> None:
  rule.init(working_dir)
  pie.init(working_dir)
  part.init(working_dir)
  hand.init(working_dir)
