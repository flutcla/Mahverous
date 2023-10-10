from pprint import pprint

import load_parts
import load_pies

pies = load_pies.load_pies()
parts = load_parts.load_parts()

pprint(parts['雀頭'].check(pies['白'], pies['白']))
pprint(parts['刻子'].check(pies['白'], pies['白'], pies['白']))
pprint(parts['刻子'].check(pies['白'], pies['白'], pies['中']))
pprint(parts['順子'].check(pies['索1'], pies['索2'], pies['索3']))
pprint(parts['順子'].check(pies['白'], pies['索2'], pies['索3']))
