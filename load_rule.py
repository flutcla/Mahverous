import yaml


def load_rule():
  with open('rule.yaml', 'r') as f:
    rule = yaml.safe_load(f)
  return rule
