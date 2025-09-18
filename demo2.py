from uml import *

# A UML Class Diagram is made up of classifiers and the relationships between them.
classifiers = []
relationships = []

###### DEFINE CLASSES ######
person = Class(
    name="Person",
    properties=[
        Property(name="name", scope=Scope.PUBLIC, data_type="String"),
        Property(name="email", scope=Scope.PUBLIC, data_type="String")
    ],
    operations=[
        Operation(name="getContactInfo", scope=Scope.PUBLIC, parameters=[], return_type="String")
    ]
)
classifiers.append(person)

employee = Class(
    name="Employee",
    properties=[
        Property(name="employeeId", scope=Scope.PROTECTED, data_type="String"),
        Property(name="hireDate", scope=Scope.PROTECTED, data_type="Date")
    ],
    operations=[
        Operation(name="calcPay", scope=Scope.PUBLIC,
            parameters=[
                Property(name="hours", scope=Scope.PUBLIC, data_type="int")
            ],
            return_type="Money"
        )
    ]
)
classifiers.append(employee)

manager = Class(
    name="Manager",
    properties=[
        Property(name="level", scope=Scope.PUBLIC, data_type="int"),
    ],
    operations=[
        Operation(name="approveBudget", scope=Scope.PUBLIC,
            parameters=[
                Property(name="amount", scope=Scope.PUBLIC, data_type="Money")
            ],
            return_type="bool"
        )
    ]
)
classifiers.append(manager)

department = Class(
    name="Department",
    properties=[
        Property(name="name", scope=Scope.PUBLIC, data_type="String"),
    ],
    operations=[
        Operation(name="getHeadcount", scope=Scope.PUBLIC, parameters=[], return_type="int")
    ]
)
classifiers.append(department)

address = Class(
    name="Address",
    properties=[
        Property(name="street", scope=Scope.PUBLIC, data_type="String"),
        Property(name="city", scope=Scope.PUBLIC, data_type="String"),
        Property(name="zip", scope=Scope.PUBLIC, data_type="String")
    ],
    operations=[]
)
classifiers.append(address)

###### DEFINE RELATIONSHIPS ######
employee_person = Relationship(
    source=employee,
    target=person,
    relation_type=RelationshipType.GENERALIZATION
)
relationships.append(employee_person)

manager_employee = Relationship(
    source=manager,
    target=employee,
    relation_type=RelationshipType.GENERALIZATION
)
relationships.append(manager_employee)

person_address = Relationship(
    source=person,
    target=address,
    relation_type=RelationshipType.AGGREGATION
)
relationships.append(person_address)

department_employee = Relationship(
    source=department,
    target=employee,
    relation_type=RelationshipType.AGGREGATION
)
relationships.append(department_employee)

department_manager = Relationship(
    source=department,
    target=manager,
    relation_type=RelationshipType.COMPOSITION
)
relationships.append(department_manager)

diagram = ClassDiagram(classifiers, relationships)
diagram.to_pydot().write_png("diagrams/demo2.png")
diagram.to_pydot(custom_styling=True).write_png("diagrams/demo2_styled.png")

