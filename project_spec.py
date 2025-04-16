import unittest
from typing import Iterable, List, NamedTuple, Sequence, Tuple

import tabulate

Edge = Tuple[str, str]


class N(NamedTuple):
    label: str
    participants: List[str]
    description: str
    depends: List[str] = []
    status: str = "pending"

    def get_edges(self) -> Iterable[Edge]:
        for src in self.depends:
            yield src, self.label

    def to_gv(self):
        tooltip_text = " ".join(self.description.split())
        if self.status == "done":
            return '{0} [style=filled, fillcolor=green, tooltip="{1}"];'.format(
                self.label, tooltip_text
            )
        elif self.status == "blocked":
            return '{0} [style=filled, fillcolor=chocolate, tooltip="{1}"];'.format(
                self.label, tooltip_text
            )
        elif self.status == "failed":
            return '{0} [style=filled, fillcolor=red, tooltip="{1}"];'.format(
                self.label, tooltip_text
            )
        elif self.status == "pending":
            return '{0}[tooltip="{1}"];'.format(self.label, tooltip_text)
        else:
            raise Exception("unknown node status {0}".format(self.status))


class Proj:
    nodes: Sequence[N]
    edges: Sequence[Edge]
    rankdir: str

    def __init__(self, nodes: Sequence[N], rankdir: str = "LR"):
        labels = [n.label for n in nodes]
        label_set = set(labels)
        assert len(labels) == len(label_set)

        edges: List[Edge] = []
        for n in nodes:
            edges.extend(n.get_edges())

        edge_set = set(edges)
        assert len(edges) == len(edge_set)

        for src, dst in edges:
            assert src in label_set, src
            assert dst in label_set, dst

        self.nodes = nodes
        self.edges = edges
        self.rankdir = rankdir

    def to_gv(self):
        ns = "\n".join([n.to_gv() for n in self.nodes])
        edge_lines = ["{0} -> {1};".format(src, dst) for src, dst in self.edges]
        edge_txt = "\n".join(edge_lines)

        return 'digraph {rankdir="%s";\n\n%s\n%s\n}' % (self.rankdir, ns, edge_txt)

    def to_table(self) -> str:
        rows = []
        for n in self.nodes:
            rows.append([n.label, n.status, " ".join(n.participants), n.description])
        headers = "goal status participants description".split()
        rows.sort(key=lambda r: r[0])
        table = tabulate.tabulate(rows, headers=headers, tablefmt="github")

        return table


class Test(unittest.TestCase):
    def test(self):
        nodes = [
            N(
                "a",
                participants=["@valentinboyanov"],
                description="a project called project a",
            ),
            N(
                "b",
                participants=["@valentinboyanov", "@igarridot"],
                description="project b",
                depends=["a"],
            ),
        ]

        proj = Proj(nodes)

        print(proj.to_gv())
        print(proj.to_table())
