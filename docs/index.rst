Siamese Prototype v2.0: Production-Ready Async Rule Engine
==========================================================

.. image:: https://img.shields.io/badge/python-3.11+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.11+

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT License

Siamese Prototype is a high-performance, asynchronous backward-chaining rule engine designed for production environments. It supports logic-based decision making and can interact with external non-blocking I/O resources such as web APIs or databases.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   quickstart
   user_guide/index
   api/index
   examples/index
   advanced/index
   contributing

.. raw:: html

   <div class="admonition note">
   <p class="admonition-title">Quick Start</p>
   <p>Want to get started immediately? Check out the <a href="quickstart.html">Quick Start Guide</a> or browse <a href="examples/index.html">Examples</a>.</p>
   </div>

Key Features
-----------

* 😎 **Fully Asynchronous**: Built on `asyncio` to handle I/O-bound tasks without blocking
* 👀 **Structured Logging**: Integrated with `loguru` for powerful and configurable tracing and debugging
* ⚙️ **External Configuration**: Load facts and rules from human-readable YAML files
* 🪜 **Extensible Async Built-ins**: Easily write custom Python `async` functions to extend engine logic
* 🚀 **Robust and Thread-Safe**: Query resolution process is stateless, allowing safe concurrent querying from multiple async tasks
* 🧰 **Control & Safety**: Prevents infinite loops with configurable search depth and limits solution count

Installation
-----------

Install the library and its dependencies from the project root:

.. code-block:: bash

   uv sync

Or using pip:

.. code-block:: bash

   pip install siamese-prototype

Quick Example
------------

.. code-block:: python

   import asyncio
   from siamese import RuleEngine

   async def main():
       # Initialize engine
       engine = RuleEngine()
       
       # Add facts
       engine.add_fact("parent", "david", "john")
       engine.add_fact("parent", "john", "mary")
       
       # Add rules
       engine.add_rule(
           ("grandparent", "?GP", "?GC"),
           [("parent", "?GP", "?P"), ("parent", "?P", "?GC")]
       )
       
       # Query asynchronously
       print("Query: Who are David's grandchildren?")
       async for solution in engine.query("grandparent", "david", "?GC"):
           print(f"  - Solution: {solution}")

   if __name__ == "__main__":
       asyncio.run(main())

Output:

.. code-block:: text

   Query: Who are David's grandchildren?
     - Solution: {'?GC': 'mary'}

.. raw:: html

   <div class="admonition tip">
   <p class="admonition-title">Tip</p>
   <p>Check out <a href="examples/index.html">complete examples</a> for more usage patterns and advanced features.</p>
   </div>

License
-------

MIT License - see LICENSE file for details. 