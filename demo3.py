from uml import *

classifiers = []
relationships = []

###### DEFINE CLASSES ######
# Base abstract entity
entity = Class(
    name="Entity",
    properties=[
        Property(name="id", scope=Scope.PROTECTED, data_type="UUID"),
        Property(name="createdAt", scope=Scope.PROTECTED, data_type="DateTime"),
        Property(name="updatedAt", scope=Scope.PROTECTED, data_type="DateTime"),
    ],
    operations=[
        Operation(name="save", scope=Scope.PUBLIC, parameters=[], return_type="void", is_abstract=True),
        Operation(name="delete", scope=Scope.PUBLIC, parameters=[], return_type="void"),
    ],
    is_abstract=True
)
classifiers.append(entity)

person = Class(
    name="Person",
    properties=[
        Property(name="name", scope=Scope.PUBLIC, data_type="String"),
        Property(name="email", scope=Scope.PUBLIC, data_type="String"),
        Property(name="phone", scope=Scope.PRIVATE, data_type="String"),
    ],
    operations=[
        Operation(name="getContactInfo", scope=Scope.PUBLIC, parameters=[], return_type="String"),
        Operation(name="validateEmail", scope=Scope.PRIVATE, parameters=[], return_type="bool"),
    ]
)
classifiers.append(person)

employee = Class(
    name="Employee",
    properties=[
        Property(name="employeeId", scope=Scope.PROTECTED, data_type="String"),
        Property(name="hireDate", scope=Scope.PROTECTED, data_type="Date"),
        Property(name="salary", scope=Scope.PRIVATE, data_type="Money"),
    ],
    operations=[
        Operation(name="calcPay", scope=Scope.PUBLIC, parameters=[
            Property(name="hours", scope=Scope.PUBLIC, data_type="int")], return_type="Money"),
        Operation(name="requestVacation", scope=Scope.PUBLIC, parameters=[
            Property(name="days", scope=Scope.PUBLIC, data_type="int")], return_type="bool"),
    ]
)
classifiers.append(employee)

manager = Class(
    name="Manager",
    properties=[
        Property(name="level", scope=Scope.PUBLIC, data_type="int"),
        Property(name="bonusBudget", scope=Scope.PRIVATE, data_type="Money"),
    ],
    operations=[
        Operation(name="approveBudget", scope=Scope.PUBLIC, parameters=[
            Property(name="amount", scope=Scope.PUBLIC, data_type="Money")], return_type="bool"),
        Operation(name="promoteEmployee", scope=Scope.PUBLIC, parameters=[
            Property(name="emp", scope=Scope.PUBLIC, data_type="Employee")], return_type="bool"),
    ]
)
classifiers.append(manager)

contractor = Class(
    name="Contractor",
    properties=[
        Property(name="contractId", scope=Scope.PUBLIC, data_type="String"),
        Property(name="rate", scope=Scope.PUBLIC, data_type="Money"),
    ],
    operations=[
        Operation(name="submitInvoice", scope=Scope.PUBLIC, parameters=[
            Property(name="hours", scope=Scope.PUBLIC, data_type="int")], return_type="Money"),
    ]
)
classifiers.append(contractor)

department = Class(
    name="Department",
    properties=[
        Property(name="name", scope=Scope.PUBLIC, data_type="String"),
        Property(name="budget", scope=Scope.PUBLIC, data_type="Money"),
    ],
    operations=[
        Operation(name="getHeadcount", scope=Scope.PUBLIC, parameters=[], return_type="int"),
        Operation(name="allocateBudget", scope=Scope.PUBLIC, parameters=[
            Property(name="amount", scope=Scope.PUBLIC, data_type="Money")], return_type="bool"),
    ]
)
classifiers.append(department)

project = Class(
    name="Project",
    properties=[
        Property(name="title", scope=Scope.PUBLIC, data_type="String"),
        Property(name="deadline", scope=Scope.PUBLIC, data_type="Date"),
        Property(name="budget", scope=Scope.PUBLIC, data_type="Money"),
    ],
    operations=[
        Operation(name="getBudget", scope=Scope.PUBLIC, parameters=[], return_type="Money"),
        Operation(name="extendDeadline", scope=Scope.PUBLIC, parameters=[
            Property(name="days", scope=Scope.PUBLIC, data_type="int")], return_type="bool"),
    ]
)
classifiers.append(project)

address = Class(
    name="Address",
    properties=[
        Property(name="street", scope=Scope.PUBLIC, data_type="String"),
        Property(name="city", scope=Scope.PUBLIC, data_type="String"),
        Property(name="zip", scope=Scope.PUBLIC, data_type="String"),
        Property(name="country", scope=Scope.PUBLIC, data_type="String"),
    ],
    operations=[]
)
classifiers.append(address)

payable = Class(
    name="(interface) Payable",
    properties=[],
    operations=[
        Operation(name="calcPay", scope=Scope.PUBLIC, parameters=[], return_type="Money", is_abstract=True)
    ],
    is_abstract=True
)
classifiers.append(payable)

payment_type = Class(
    name="(enum) PaymentType",
    properties=[
        Property(name="CASH", scope=Scope.PUBLIC, data_type="PaymentType"),
        Property(name="CREDIT", scope=Scope.PUBLIC, data_type="PaymentType"),
        Property(name="TRANSFER", scope=Scope.PUBLIC, data_type="PaymentType"),
        Property(name="CRYPTO", scope=Scope.PUBLIC, data_type="PaymentType"),
    ],
    operations=[]
)
classifiers.append(payment_type)

invoice = Class(
    name="Invoice",
    properties=[
        Property(name="invoiceId", scope=Scope.PUBLIC, data_type="String"),
        Property(name="amount", scope=Scope.PUBLIC, data_type="Money"),
        Property(name="status", scope=Scope.PUBLIC, data_type="String"),
    ],
    operations=[
        Operation(name="markPaid", scope=Scope.PUBLIC, parameters=[], return_type="bool"),
        Operation(name="sendReminder", scope=Scope.PUBLIC, parameters=[], return_type="void"),
    ]
)
classifiers.append(invoice)

###### RELATIONSHIPS ######
# Generalization
relationships.append(Relationship(person, entity, RelationshipType.GENERALIZATION))
relationships.append(Relationship(employee, person, RelationshipType.GENERALIZATION))
relationships.append(Relationship(manager, employee, RelationshipType.GENERALIZATION))
relationships.append(Relationship(contractor, person, RelationshipType.GENERALIZATION))

# Composition / Aggregation
relationships.append(Relationship(person, address, RelationshipType.AGGREGATION))
relationships.append(Relationship(department, employee, RelationshipType.AGGREGATION))
relationships.append(Relationship(department, manager, RelationshipType.COMPOSITION))
relationships.append(Relationship(project, department, RelationshipType.COMPOSITION))
relationships.append(Relationship(invoice, project, RelationshipType.COMPOSITION))

# Associations
relationships.append(Relationship(employee, project, RelationshipType.ASSOCIATION))
relationships.append(Relationship(manager, project, RelationshipType.ASSOCIATION))
relationships.append(Relationship(contractor, project, RelationshipType.ASSOCIATION))
relationships.append(Relationship(invoice, payment_type, RelationshipType.ASSOCIATION))

# Realizations
relationships.append(Relationship(employee, payable, RelationshipType.REALIZATION))
relationships.append(Relationship(contractor, payable, RelationshipType.REALIZATION))

# Dependencies
relationships.append(Relationship(manager, payment_type, RelationshipType.DEPENDENCY))
relationships.append(Relationship(invoice, person, RelationshipType.DEPENDENCY))

###### BUILD DIAGRAM ######
diagram = ClassDiagram(classifiers, relationships)
diagram.to_pydot().write_png("diagrams/demo3.png")
diagram.to_pydot(custom_styling=True).write_png("diagrams/demo3_styled.png")
