import pydot

# Container for our UML class diagram. Which is a directed graph.
graph = pydot.Dot(graph_name="UML", graph_type="digraph", rankdir="BT", fontname="Helvetica")

# Containers for each of our classes. Each class is a node of the shape "record".
# Note that the label controls what the "class" looks like.
#   This "label" string would have to be created programmatically and would likely involve implementing some class.
person_node = pydot.Node(
    name="Person",
    shape="record",
    label="""{Person|+ name: String\\l+ email: String\\l|+ getContactInfo(): String\\l}"""
)
employee_node = pydot.Node(
    "Employee",
    shape="record",
    label="""{Employee|# employeeId: String\\l# hireDate: Date\\l|+ calcPay(): Money\\l}"""
)
manager_node = pydot.Node(
    "Manager",
    shape="record",
    label="""{Manager|+ level: int\\l|+ approveBudget(amount: Money): bool\\l}"""
)
department_node = pydot.Node(
    "Department",
    shape="record",
    label="""{Department|+ name: String\\l|+ getHeadcount(): int\\l}"""
)
address_node = pydot.Node(
    "Address",
    shape="record",
    label="""{Address|+ street: String\\l+ city: String\\l+ zip: String\\l|}"""
)

# Add nodes to the graph
graph.add_node(person_node)
graph.add_node(employee_node)
graph.add_node(manager_node)
graph.add_node(department_node)
graph.add_node(address_node)

# Add edges for relationships
# Inheritance: Employee --> Person, Manager --> Employee
graph.add_edge(pydot.Edge("Employee", "Person", arrowhead="empty"))
graph.add_edge(pydot.Edge("Manager", "Employee", arrowhead="empty"))

# Composition: Person --> Address (1..*)
graph.add_edge(pydot.Edge("Person", "Address", dir="both", arrowhead="none", arrowtail="diamond", taillabel="1", headlabel="0..*"))

# Association: Department --> Employee (1..*)
graph.add_edge(pydot.Edge("Department", "Employee", arrowhead="none", taillabel="1", headlabel="0..*"))

# Named Association: Department "leads" Manager
graph.add_edge(pydot.Edge("Department", "Manager", arrowhead="none", label="leads", fontsize="10"))

# Write the diagram to a file
graph.write_png("diagrams/demo1.png")

