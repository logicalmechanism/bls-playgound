from dataclasses import dataclass

from src.bls12_381 import (g1_identity, g1_point, g2_point, gt_identity,
                           invert, pair)
from src.Registry.boneh_lynn_shacham import BonehLynnShacham
from src.Registry.element import Element
from src.Registry.registry import Registry


@dataclass
class Payment:
    s: BonehLynnShacham
    # x, y, f
    initial: tuple[int, int, int]
    # x, y, f
    final: tuple[int, int, int]
    receiver: Registry
    f: int
    b: int
    A: Element = Element(g1_identity)
    B: Element = Element(g1_identity)
    P: Element = Element(g1_point(1))
    Q: Element = Element(g2_point(1))
    QI: Element = invert(Q.value)

    def __post_init__(self):
        for i in self.initial:
            p = Element(g1_point(i))
            self.A = self.A + p

        for f in self.final:
            p = Element(g1_point(f))
            self.B = self.B + p

    def prove(self) -> bool:
        value_conservation = pair(self.Q.value, self.A.value) * pair(self.QI, self.B.value) == gt_identity
        spend_validation = self.s.prove()
        return all([value_conservation, spend_validation])
