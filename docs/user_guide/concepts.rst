Core Concepts
=============

This chapter introduces Siamese Prototype's core concepts and terminology.

Facts
-----

Facts are statements known to be true. In Siamese Prototype, facts are represented as predicates and arguments.

.. code-block:: python

   # Adding facts
   engine.add_fact("parent", "david", "john")  # david is john's parent
   engine.add_fact("person", "alice")          # alice is a person
   engine.add_fact("age", "bob", 25)           # bob's age is 25

Fact syntax:
- The first argument is the predicate name (string)
- Subsequent arguments are the predicate values
- Arguments can be strings, numbers, booleans, etc.

Rules
-----

Rules are used to derive new knowledge from known facts. Rules consist of two parts:
- **Rule head**: The conclusion to be derived
- **Rule body**: The conditions that must be satisfied

.. code-block:: python

   # Rule: If A is P's parent and P is C's parent, then A is C's grandparent
   engine.add_rule(
       ("grandparent", "?A", "?C"),           # Rule head
       [                                       # Rule body
           ("parent", "?A", "?P"),
           ("parent", "?P", "?C")
       ]
   )

Variables
---------

Variables start with `?` and represent unknown values. During rule execution, variables are bound to specific values.

.. code-block:: python

   # Variable examples
   "?X"      # Single variable
   "?Person" # Descriptive variable name
   "?A", "?B", "?C"  # Multiple variables

Variable binding example:

.. code-block:: python

   # Given facts: parent(david, john)
   # Query: parent(david, ?X)
   # Result: {'?X': 'john'}

Queries
-------

Queries are questions posed to the knowledge base. Queries can contain variables, and the engine will try to find all possible solutions.

.. code-block:: python

   # Simple query
   async for solution in engine.query("parent", "david", "?Child"):
       print(f"David's child: {solution['?Child']}")
   
   # Complex query
   async for solution in engine.query("grandparent", "?GP", "?GC"):
       print(f"{solution['?GP']} is {solution['?GC']}'s grandparent")

Unification
-----------

Unification is the process of matching and binding variables. When the engine tries to apply rules, it:

1. Attempts to unify the query goal with the rule head
2. If successful, applies variable bindings to the rule body
3. Recursively solves each goal in the rule body

.. code-block:: python

   # Unification example
   # Query: grandparent(david, ?GC)
   # Rule: grandparent(?A, ?C) :- parent(?A, ?P), parent(?P, ?C)
   # 
   # Unification process:
   # 1. Unify grandparent(david, ?GC) with grandparent(?A, ?C)
   # 2. Bindings: ?A = david, ?C = ?GC
   # 3. Apply bindings to rule body: parent(david, ?P), parent(?P, ?GC)
   # 4. Solve each goal...

Async Execution
--------------

Siamese Prototype is fully asynchronous, which means:

- Queries don't block the event loop
- Multiple queries can be processed simultaneously
- Built-in functions can perform I/O operations (such as HTTP requests, database queries)

.. code-block:: python

   # Async queries
   async def multiple_queries():
       engine = RuleEngine()
       # ... Add facts and rules ...
       
       # Can execute multiple queries simultaneously
       query1 = engine.query("parent", "david", "?Child")
       query2 = engine.query("grandparent", "?GP", "mary")
       
       async for solution in query1:
           print(f"Query1 result: {solution}")
       
       async for solution in query2:
           print(f"Query2 result: {solution}")

Knowledge Base
--------------

The knowledge base is a collection of facts and rules. Siamese Prototype provides multiple ways to manage the knowledge base:

.. code-block:: python

   # Programmatic addition
   engine.add_fact("parent", "david", "john")
   engine.add_rule(("grandparent", "?A", "?C"), [...])
   
   # Load from file
   engine.load_from_file("knowledge.yaml")
   
   # Auto-search for files
   engine.load_kb_auto("knowledge.yaml")  # Search current and parent directories

Built-in Functions
-----------------

Built-in functions are predefined logical operations that can:

- Perform comparison operations (equals, not equals, greater than, etc.)
- Perform mathematical operations
- Perform external I/O operations
- Execute custom logic

.. code-block:: python

   # Built-in function example
   engine.add_rule(
       ("adult", "?Person"),
       [("age", "?Person", "?Age"), ("gte", "?Age", 18)]
   )

.. raw:: html

   <div class="admonition tip">
   <p class="admonition-title">Tip</p>
   <p>Understanding these core concepts is key to effectively using Siamese Prototype. It's recommended to gradually familiarize yourself with these concepts through practical use.</p>
   </div> 