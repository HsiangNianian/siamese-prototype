Family Relationship Reasoning Examples
====================================

This example demonstrates how to use Siamese Prototype for family relationship reasoning, including the definition and querying of relationships such as parents, grandparents, siblings, etc.

Basic Facts and Rules
--------------------

.. code-block:: python

   import asyncio
   from siamese import RuleEngine

   async def family_example():
       engine = RuleEngine()
       
       # Add basic facts
       engine.add_fact("parent", "david", "john")
       engine.add_fact("parent", "sarah", "john")
       engine.add_fact("parent", "john", "mary")
       engine.add_fact("parent", "john", "peter")
       engine.add_fact("parent", "peter", "alice")
       engine.add_fact("parent", "peter", "bob")
       
       # Add inference rules
       # Grandparent relationship
       engine.add_rule(
           ("grandparent", "?GP", "?GC"),
           [("parent", "?GP", "?P"), ("parent", "?P", "?GC")]
       )
       
       # Sibling relationship
       engine.add_rule(
           ("sibling", "?S1", "?S2"),
           [("parent", "?P", "?S1"), ("parent", "?P", "?S2"), ("neq", "?S1", "?S2")]
       )
       
       # Cousin relationship
       engine.add_rule(
           ("cousin", "?C1", "?C2"),
           [("parent", "?P1", "?C1"), ("parent", "?P2", "?C2"), ("sibling", "?P1", "?P2")]
       )
       
       # Ancestor relationship (recursive)
       engine.add_rule(
           ("ancestor", "?A", "?D"),
           [("parent", "?A", "?D")]
       )
       engine.add_rule(
           ("ancestor", "?A", "?D"),
           [("parent", "?A", "?P"), ("ancestor", "?P", "?D")]
       )

Executing Queries
----------------

.. code-block:: python

       # Query David's grandchildren
       print("David's grandchildren:")
       async for solution in engine.query("grandparent", "david", "?GC"):
           print(f"  - {solution['?GC']}")
       
       # Query Mary's siblings
       print("\nMary's siblings:")
       async for solution in engine.query("sibling", "mary", "?S"):
           print(f"  - {solution['?S']}")
       
       # Query Alice's cousins
       print("\nAlice's cousins:")
       async for solution in engine.query("cousin", "alice", "?C"):
           print(f"  - {solution['?C']}")
       
       # Query all of David's descendants
       print("\nAll of David's descendants:")
       async for solution in engine.query("ancestor", "david", "?D"):
           print(f"  - {solution['?D']}")

   if __name__ == "__main__":
       asyncio.run(family_example())

Run Results
-----------

.. code-block:: text

   David's grandchildren:
     - mary
     - peter
   
   Mary's siblings:
     - peter
   
   Alice's cousins:
     - bob
   
   David's descendants:
     - john
     - mary
     - peter
     - alice
     - bob

Using YAML Files
---------------

You can also save the knowledge base in YAML files:

.. code-block:: yaml

   # family.yaml
   facts:
     - [parent, david, john]
     - [parent, sarah, john]
     - [parent, john, mary]
     - [parent, john, peter]
     - [parent, peter, alice]
     - [parent, peter, bob]
   
   rules:
     - head: [grandparent, '?GP', '?GC']
       body:
         - [parent, '?GP', '?P']
         - [parent, '?P', '?GC']
     
     - head: [sibling, '?S1', '?S2']
       body:
         - [parent, '?P', '?S1']
         - [parent, '?P', '?S2']
         - [neq, '?S1', '?S2']
     
     - head: [cousin, '?C1', '?C2']
       body:
         - [parent, '?P1', '?C1']
         - [parent, '?P2', '?C2']
         - [sibling, '?P1', '?P2']
     
     - head: [ancestor, '?A', '?D']
       body:
         - [parent, '?A', '?D']
     
     - head: [ancestor, '?A', '?D']
       body:
         - [parent, '?A', '?P']
         - [ancestor, '?P', '?D']

Then load from file:

.. code-block:: python

   async def load_from_yaml():
       engine = RuleEngine()
       engine.load_from_file("family.yaml")
       
       # Execute the same queries...
       print("David's grandchildren:")
       async for solution in engine.query("grandparent", "david", "?GC"):
           print(f"  - {solution['?GC']}")

Advanced Queries
---------------

You can also perform more complex queries:

.. code-block:: python

   # Find all people who have siblings
   print("People with siblings:")
   async for solution in engine.query("sibling", "?S1", "?S2"):
       print(f"  - {solution['?S1']} and {solution['?S2']} are siblings")
   
   # Find all grandparent-grandchild relationships
   print("\nAll grandparent-grandchild relationships:")
   async for solution in engine.query("grandparent", "?GP", "?GC"):
       print(f"  - {solution['?GP']} is {solution['?GC']}'s grandparent")

.. raw:: html

   <div class="admonition note">
   <p class="admonition-title">Note</p>
   <p>This example demonstrates the use of recursive rules (ancestor relationship) and complex relationship reasoning (cousin relationship).</p>
   </div> 