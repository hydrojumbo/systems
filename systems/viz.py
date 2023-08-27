"""
Tooling to convert a model into a graphviz diagram.
"""
import sys

from graphviz import Digraph

from . import parse
from .errors import ParseException

def as_dot(model, rankdir="TB", label=""):
    mapping = {s.name: str(i) for i, s in enumerate(model.stocks)}    
    dot = Digraph(comment=model.name)
    dot.attr(rankdir=rankdir)
    dot.attr(label=label)
    for stock in model.stocks:
        if (str(stock.maximum) == 'inf'):
            dot.node(mapping[stock.name], '{' + f'{stock.name}|Initial: {stock.initial}' + '}', shape='record')
        else:    
            dot.node(mapping[stock.name], '{' + f'{stock.name}|Initial: {stock.initial}|Max: {stock.maximum}' + '}', shape='record')

    for flow in model.flows:
        source_id = mapping[flow.source.name]
        destination_id = mapping[flow.destination.name]
        dot.edge(source_id, destination_id, label=f'{flow.rate}')

    return dot


def main():
    txt = sys.stdin.read()

    try:
        model = parse.parse(txt)
    except ParseException as pe:
        print(pe)
        return

    dot = as_dot(model)
    print(dot.source)


if __name__ == "__main__":
    main()
