RuleEngine
==========

.. automodule:: siamese.engine
   :members:
   :undoc-members:
   :show-inheritance:

RuleEngine Class
---------------

RuleEngine is the main entry point of Siamese Prototype, providing a high-level async interface to manage knowledge bases and execute queries.

Constructor
----------

.. code-block:: python

   RuleEngine(builtins: Optional[Dict[str, AsyncBuiltin]] = None)

**Parameters:**
- ``builtins`` - Optional dictionary of custom built-in functions

**Example:**

.. code-block:: python

   # Use default built-in functions
   engine = RuleEngine()
   
   # Use custom built-in functions
   custom_builtins = {"my_func": my_async_function}
   engine = RuleEngine(builtins=custom_builtins)

Main Methods
------------

Configure Logging
~~~~~~~~~~~~~~~~

.. code-block:: python

   configure_logging(level="INFO", sink=sys.stderr)

Configure engine logging.

**Parameters:**
- ``level`` - Log level ("TRACE", "DEBUG", "INFO", "WARNING", "ERROR")
- ``sink`` - Log output destination

**Example:**

.. code-block:: python

   # Configure detailed logging (for debugging)
   engine.configure_logging(level="TRACE")
   
   # Configure production environment logging
   engine.configure_logging(level="INFO")

Add Facts
~~~~~~~~~

.. code-block:: python

   add_fact(name: str, *args: Any)

Add a fact to the knowledge base.

**Parameters:**
- ``name`` - Predicate name
- ``*args`` - Predicate arguments

**Example:**

.. code-block:: python

   engine.add_fact("parent", "david", "john")
   engine.add_fact("age", "alice", 25)
   engine.add_fact("person", "bob")

Add Rules
~~~~~~~~~

.. code-block:: python

   add_rule(head_tuple: Tuple, body_tuples: List[Tuple])

Add a rule to the knowledge base.

**Parameters:**
- ``head_tuple`` - Rule head (tuple)
- ``body_tuples`` - Rule body (list of tuples)

**Example:**

.. code-block:: python

   engine.add_rule(
       ("grandparent", "?A", "?C"),
       [("parent", "?A", "?P"), ("parent", "?P", "?C")]
   )

Load from File
~~~~~~~~~~~~~~

.. code-block:: python

   load_from_file(filepath: str)

Load knowledge base from YAML file.

**Parameters:**
- ``filepath`` - YAML file path

**Example:**

.. code-block:: python

   engine.load_from_file("knowledge.yaml")

Auto Load
~~~~~~~~~

.. code-block:: python

   load_kb_auto(filename: str)

Automatically search and load knowledge base file (searches current and parent directories).

**Parameters:**
- ``filename`` - File name

**Example:**

.. code-block:: python

   engine.load_kb_auto("knowledge.yaml")

Queries
~~~~~~~

.. code-block:: python

   async def query(
       self,
       name: str,
       *args: Any,
       max_solutions: int = -1,
       max_depth: int = 25,
   ) -> AsyncGenerator[Dict[str, Any], None]

Async query the knowledge base.

**Parameters:**
- ``name`` - Predicate name
- ``*args`` - Query arguments
- ``max_solutions`` - Maximum number of solutions (-1 for unlimited)
- ``max_depth`` - Maximum search depth

**Returns:**
- Async generator yielding solution dictionaries

**Example:**

.. code-block:: python

   async for solution in engine.query("parent", "david", "?Child"):
       print(f"David's child: {solution['?Child']}")

Query Single Solution
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   async def query_one(self, name: str, *args: Any, **kwargs) -> Optional[Dict[str, Any]]

Get the first solution or None.

**Parameters:**
- ``name`` - Predicate name
- ``*args`` - Query arguments
- ``**kwargs`` - Other query parameters

**Returns:**
- Solution dictionary or None

**Example:**

.. code-block:: python

   solution = await engine.query_one("parent", "david", "?Child")
   if solution:
       print(f"Found: {solution['?Child']}")

Check Existence
~~~~~~~~~~~~~~

.. code-block:: python

   async def exists(self, name: str, *args: Any, **kwargs) -> bool

Check if at least one solution exists.

**Parameters:**
- ``name`` - Predicate name
- ``*args`` - Query arguments
- ``**kwargs`` - Other query parameters

**Returns:**
- True if solution exists, False otherwise

**Example:**

.. code-block:: python

   if await engine.exists("parent", "david", "john"):
       print("David is John's parent")

Complete Example
---------------

.. code-block:: python

   import asyncio
   from siamese import RuleEngine

   async def main():
       # Create engine
       engine = RuleEngine()
       
       # Configure logging
       engine.configure_logging(level="INFO")
       
       # Add facts
       engine.add_fact("parent", "david", "john")
       engine.add_fact("parent", "john", "mary")
       
       # Add rules
       engine.add_rule(
           ("grandparent", "?GP", "?GC"),
           [("parent", "?GP", "?P"), ("parent", "?P", "?GC")]
       )
       
       # Query
       print("David's grandchildren:")
       async for solution in engine.query("grandparent", "david", "?GC"):
           print(f"  - {solution['?GC']}")

   if __name__ == "__main__":
       asyncio.run(main())