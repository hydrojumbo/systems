import sys
import argparse

import systems
from exceptions import MissingDelimiter


def parse_stock(model, name):
    name = name.strip()
    infinite = False
    if name.startswith('[') and name.endswith(']'):
        name = name[1:-1]
        infinite = True

    exists = model.get_stock(name)
    if exists:
        return exists

    if infinite:
        return model.infinite_stock(name)
    return model.stock(name)


def parse_flow(model, src, dest, txt):
    parts = txt.split(",")
    val = parts[0].strip()

    # guess class by value
    if "." in val:
        rate_class = systems.Conversion
        val = float(val)
    else:
        rate_class = systems.Rate
        val = int(val)

    # use specified class if any
    if len(parts) > 1:
        class_str = parts[1].strip()
        if class_str == "leak":
            rate_class = systems.Leak
        elif class_str == "conversion":
            rate_class = systems.Conversion
        elif class_str == "rate":
            rate_class = systems.Rate

    rate = rate_class(val)
    return model.flow(src, dest, rate)


def parse(txt):
    m = systems.Model("Parsed")

    stocks = []
    by_name = {}
    flows = []

    for line in txt.split('\n'):
        line = line.strip()
        # ignore comments
        if line == "" or line.startswith("#"):
            continue

        try:
            source_name, rest  = line.split(">")
        except ValueError:
            raise MissingDelimiter(">", line)

        try:
            dest_name, args = rest.split("@")
        except ValueError:
            raise MissingDelimiter("@", line)            

        source = parse_stock(m, source_name)
        dest = parse_stock(m, dest_name)

        parse_flow(m, source, dest, args)

    return m


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-r', '--rounds', type=int, help="number of rounds to run evaluation", default=10)
    p.add_argument('--csv', action='store_true', default=False)
    args = p.parse_args()

    txt = sys.stdin.read()
    model = parse(txt)
    if args.csv:
        model.run(rounds=args.rounds, sep=",", pad=False)
    else:
        model.run(rounds=args.rounds)


if __name__ == "__main__":
    main()
