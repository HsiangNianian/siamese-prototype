Quick Start Guide
================

This guide will help you quickly get started with Siamese Prototype through several simple examples to understand the basic concepts and usage.

First Example: Family Relationships
---------------------------------

Let's start with a simple family relationship example:

.. code-block:: python

   import asyncio
   from siamese import RuleEngine

   async def family_example():
       # Create rule engine instance
       engine = RuleEngine()
       
       # Add some facts (known relationships)
       engine.add_fact("parent", "david", "john")
       engine.add_fact("parent", "john", "mary")
       engine.add_fact("parent", "john", "peter")
       
       # Add a rule (inference relationship)
       # Rule: If A is P's parent and P is C's parent, then A is C's grandparent
       engine.add_rule(
           ("grandparent", "?A", "?C"),  # Rule head: A is C's grandparent
           [                              # Rule body: conditions that must be met
               ("parent", "?A", "?P"),   # A is P's parent
               ("parent", "?P", "?C")    # P is C's parent
           ]
       )
       
       # Query: Who are David's grandchildren?
       print("Query: Who are David's grandchildren?")
       async for solution in engine.query("grandparent", "david", "?C"):
           print(f"  - {solution['?C']}")
       
       # Query: Who are Mary's grandparents?
       print("\nQuery: Who are Mary's grandparents?")
       async for solution in engine.query("grandparent", "?A", "mary"):
           print(f"  - {solution['?A']}")

   if __name__ == "__main__":
       asyncio.run(family_example())

Running this example, you'll see:

.. code-block:: text

   Query: Who are David's grandchildren?
     - mary
     - peter
   
   Query: Who are Mary's grandparents?
     - david

Loading Knowledge from YAML Files
--------------------------------

You can also save knowledge bases in YAML files:

Create file `family.yaml`:

.. code-block:: yaml

   facts:
     - [parent, david, john]
     - [parent, john, mary]
     - [parent, john, peter]
     - [parent, sarah, john]
   
   rules:
     - head: [grandparent, '?A', '?C']
       body:
         - [parent, '?A', '?P']
         - [parent, '?P', '?C']
     - head: [sibling, '?S1', '?S2']
       body:
         - [parent, '?P', '?S1']
         - [parent, '?P', '?S2']
         - [neq, '?S1', '?S2']

Then load from file:

.. code-block:: python

   async def load_from_file_example():
       engine = RuleEngine()
       
       # Load knowledge base from YAML file
       engine.load_from_file("family.yaml")
       
       # Query sibling relationships
       print("Query: Who are Mary's siblings?")
       async for solution in engine.query("sibling", "mary", "?S"):
           print(f"  - {solution['?S']}")

Using Async Built-in Functions
----------------------------

Siamese Prototype supports async built-in functions that can perform external I/O operations:

.. code-block:: python

   import aiohttp
   from siamese import RuleEngine

   async def http_get_json(goal, bindings):
       """Async built-in function: fetch JSON data"""
       url = goal.args[0]
       if isinstance(url, str):
           async with aiohttp.ClientSession() as session:
               async with session.get(url) as response:
                   if response.status == 200:
                       data = await response.json()
                       new_bindings = bindings.copy()
                       new_bindings[goal.args[1]] = data
                       yield new_bindings

   async def async_builtin_example():
       # Create engine and register custom built-in function
       engine = RuleEngine(builtins={"http_get_json": http_get_json})
       
       # Add some rules
       engine.add_rule(
           ("user_info", "?Username", "?Info"),
           [("http_get_json", "https://api.github.com/users/?Username", "?Info")]
       )
       
       # Query GitHub user information
       print("Fetching GitHub user information...")
       async for solution in engine.query("user_info", "octocat", "?Info"):
           user_info = solution['?Info']
           print(f"Username: {user_info.get('login')}")
           print(f"Name: {user_info.get('name')}")
           print(f"Followers: {user_info.get('followers')}")

Configuring Logging
------------------

You can configure the engine's logging level to debug the query process:

.. code-block:: python

   async def logging_example():
       engine = RuleEngine()
       
       # Configure detailed logging (for debugging)
       engine.configure_logging(level="TRACE")
       
       # Or configure production logging
       # engine.configure_logging(level="INFO")
       
       engine.add_fact("parent", "david", "john")
       engine.add_rule(
           ("grandparent", "?A", "?C"),
           [("parent", "?A", "?P"), ("parent", "?P", "?C")]
       )
       
       # Queries will show detailed reasoning process
       async for solution in engine.query("grandparent", "david", "?C"):
           print(f"Found solution: {solution}")

Next Steps
---------

Now that you understand the basic usage, you can:

1. Check out :doc:`user_guide/index` for more detailed usage methods
2. Browse :doc:`examples/index` for more examples
3. Read :doc:`api/index` for complete API documentation
4. Learn advanced features in :doc:`advanced/index`

.. raw:: html

   <div class="admonition tip">
   <p class="admonition-title">Tip</p>
   <p>All examples can be found as complete runnable versions in the <code>tests/</code> directory.</p>
   </div> 