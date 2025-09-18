from abc import ABC
from enum import Enum, auto
from typing import List
import pydot

class ClassDiagram:
    def __init__(self,
                 classifiers: List['Classifier'],
                 relationships: List['Relationship']):
        self._classifiers = classifiers
        self._relations = relationships

    def to_pydot(
            self,
            size: str = "8,10",
            ratio: str = "auto",
            custom_styling: bool = False
    ) -> pydot.Dot:
        """
        Convert ClassDiagram into a pydot.Dot graph.

        Parameters:
            size (str): Graph size in inches, e.g. "8,10".
            ratio (str): Graphviz ratio setting ("auto", "fill", "compress", "expand", or a number).
            custom_styling (bool): If True, applies wacky demo styling. Otherwise, defaults.
        """
        # Base graph
        graph = pydot.Dot(
            graph_type="digraph",
            rankdir="BT",
            # ratio=ratio,
            # size=size,
            dpi="300"
        )

        if custom_styling:
            graph.set("fontname", "Comic Sans MS")
            graph.set("bgcolor", "#fceabb:#f8b500")
            graph.set("splines", "ortho")
            graph.set("ranksep", "1.2")
            graph.set("nodesep", "0.8")

            graph.set_node_defaults(
                shape="record",
                fontname="Comic Sans MS",
                fontsize="12",
                style="rounded,filled,bold",
                fillcolor="#74b9ff:#a29bfe",
                gradientangle="90",
                color="#ff0066",
                fontcolor="#111111",
                penwidth="2"
            )

            graph.set_edge_defaults(
                fontname="Courier New",
                fontsize="10",
                color="#ff5733",
                style="dashed",
                arrowsize="1.5",
                penwidth="2"
            )

        # Add classifier nodes
        for classifier in self._classifiers:
            graph.add_node(classifier.to_pydot())

        # Add relationship edges
        for relation in self._relations:
            graph.add_edge(relation.to_pydot())

        return graph

class Classifier(ABC):
    def __init__(self,
                 name: str,
                 properties: List['Property'],
                 operations: List['Operation']):
        self._name = name
        self._properties = properties
        self._operations = operations
        if type(self) is Classifier:
            raise TypeError("Classifier is an abstract class and cannot be instantiated directly")

    @property
    def name(self) -> str:
        return self._name

    @property
    def properties(self) -> List['Property']:
        return self._properties

    @property
    def operations(self) -> List['Operation']:
        return self._operations

    def to_pydot(self) -> pydot.Node:
        return pydot.Node(
            self._name,
            shape="record",
            label=self._make_label()
        )

    def _make_label(self) -> str:
        parts = ["{",f"{self._name}", "|"]
        for p in self._properties:
            parts.append(f"{p.scope.value} {p.name}: {p.data_type}\\l")
        parts.append("|")
        for o in self._operations:
            parts.append(f"{o.scope.value} {o.name}({', '.join(p.name for p in o.parameters)}): {o.return_type}\\l")
        parts.append("}")
        return "".join(parts)

class Class(Classifier):
    def __init__(self,
                 name: str,
                 properties: List['Property'],
                 operations: List['Operation'],
                 is_abstract = False):
        super().__init__(name, properties, operations)
        self._is_abstract = is_abstract

    @property
    def is_abstract(self) -> bool:
        return self._is_abstract

class Scope(Enum):
    PACKAGE     = "~"
    PRIVATE     = "-"
    PROTECTED   = "#"
    PUBLIC      = "+"

class Member(ABC):
    def __init__(self,
                 name: str,
                 scope: Scope,
                 is_abstract: bool,
                 is_static: bool):
        if type(self) is Member:
            raise TypeError("Member is an abstract class and cannot be instantiated directly")
        self._name = name
        self._scope = scope
        self._is_abstract = is_abstract
        self._is_static = is_static

    @property
    def name(self) -> str:
        return self._name

    @property
    def scope(self) -> Scope:
        return self._scope

    @property
    def is_static(self) -> bool:
        return self._is_static

    @property
    def is_abstract(self) -> bool:
        return self._is_abstract

class Property(Member):
    def __init__(self,
                 name: str,
                 scope: Scope,
                 data_type: str,
                 is_abstract: bool = False,
                 is_static: bool = False):
        super().__init__(name, scope, is_abstract, is_static)
        self._data_type = data_type

    @property
    def data_type(self) -> str:
        return self._data_type

class Operation(Member):
    def __init__(self,
                 name: str,
                 scope: Scope,
                 parameters: List[Property],
                 return_type: str,
                 is_abstract: bool = False,
                 is_static: bool = False):
        super().__init__(name, scope, is_abstract, is_static)
        self._parameters = parameters
        self._return_type = return_type

    @property
    def parameters(self) -> List[Property]:
        return self._parameters

    @property
    def return_type(self) -> str:
        return self._return_type

class RelationshipType(Enum):
    DEPENDENCY = auto()
    ASSOCIATION = auto()
    AGGREGATION = auto()
    COMPOSITION = auto()
    GENERALIZATION = auto()
    REALIZATION = auto()

class Relationship:
    def __init__(self,
                 source: Classifier,
                 target: Classifier,
                 relation_type: RelationshipType):
        self._source = source
        self._target = target
        self._relation_type = relation_type

    @property
    def source(self) -> Classifier:
        return self._source

    @property
    def target(self) -> Classifier:
        return self._target

    @property
    def type(self) -> RelationshipType:
        return self._relation_type

    def to_pydot(self) -> pydot.Edge:
        # default attributes
        attrs = {
            "arrowhead": "none",
            "arrowtail": "none",
            "style": "solid",
        }

        if self.type == RelationshipType.DEPENDENCY:
            attrs.update({"style": "dashed", "arrowhead": "vee"})

        elif self.type == RelationshipType.ASSOCIATION:
            attrs.update({"arrowhead": "none"})

        elif self.type == RelationshipType.AGGREGATION:
            attrs.update({"arrowhead": "none", "arrowtail": "odiamond", "dir": "both"})

        elif self.type == RelationshipType.COMPOSITION:
            attrs.update({"arrowhead": "none", "arrowtail": "diamond", "dir": "both"})

        elif self.type == RelationshipType.GENERALIZATION:
            attrs.update({"arrowhead": "empty"})

        elif self.type == RelationshipType.REALIZATION:
            attrs.update({"style": "dashed", "arrowhead": "empty"})

        return pydot.Edge(self.source.name, self.target.name, **attrs)


