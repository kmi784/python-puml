from plantweb.render import render

from puml.src import logger, UmlChart
from test.conftest import MockParent, MockCore, MockClass

obj1, obj2, obj3 = UmlChart(), UmlChart(), UmlChart()
obj1.add_class(MockCore)
obj2.add_class(MockParent)
obj3.add_class(MockClass)


code = """
class MockCore {
}
 class MockParent {
        +attr_abstract: bool
        +abstract_method(arg: bool) -> bool
}
 class MockClass {
        +attr_basic: int
        +attr_union: Union[int, float]
        +attr_list: List[MockCore]
        +attr_tuple: Tuple[int, MockCore]
        +core: bool
        +basic_method(arg1: MockCore, arg2: MockCore) -> List[Union[int, float]]
        +{static}static_method(arg: Optional[List[Union[int, float]]]) -> None
        
"""

svg_bytes, _, _, _ = render(code, engine="plantuml", format="svg")

with open("chart.svg", "wb") as f:
    f.write(svg_bytes)

print(obj1, obj2, obj3)