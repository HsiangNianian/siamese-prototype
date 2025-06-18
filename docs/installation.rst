Installation Guide
=================

System Requirements
------------------

* Python 3.11 or higher
* Supported operating systems: Linux, macOS, Windows

Installation Methods
-------------------

Using uv (Recommended)
~~~~~~~~~~~~~~~~~~~~~

`uv` is a fast Python package manager and installer. If you haven't installed uv yet, install it first:

.. code-block:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh

Then run from the project root:

.. code-block:: bash

   uv sync

Using pip
~~~~~~~~

.. code-block:: bash

   pip install siamese-prototype

Installing from Source
~~~~~~~~~~~~~~~~~~~~~

If you want to install the latest version from source:

.. code-block:: bash

   git clone https://github.com/hsiangnianian/siamese-prototype.git
   cd siamese-prototype
   uv sync
   uv run pip install -e .

Verifying Installation
---------------------

After installation, you can verify it works:

.. code-block:: python

   import asyncio
   from siamese import RuleEngine

   async def test_installation():
       engine = RuleEngine()
       engine.add_fact("test", "hello")
       
       result = await engine.query_one("test", "?X")
       print(f"Installation successful! Result: {result}")

   asyncio.run(test_installation())

If you see output "Installation successful! Result: {'?X': 'hello'}", the installation was successful.

Dependencies
-----------

Main dependencies include:

* `loguru >= 0.6.0` - Structured logging
* `PyYAML >= 6.0` - YAML file parsing
* `aiohttp >= 3.8.1` - Async HTTP client

Development dependencies:

* `pytest >= 8.4.1` - Testing framework
* `pytest-asyncio >= 1.0.0` - Async testing support

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

**Issue**: Import error "No module named 'siamese'"
   **Solution**: Make sure you're in the correct virtual environment and have run `uv sync` or `pip install`.

**Issue**: Version compatibility error
   **Solution**: Make sure you're using Python 3.11 or higher.

**Issue**: YAML parsing error
   **Solution**: Make sure PyYAML is installed: `pip install PyYAML`.

Getting Help
-----------

If you encounter installation issues, please:

1. Check that your Python version meets the requirements
2. Ensure all dependencies are properly installed
3. Check `GitHub Issues <https://github.com/hsiangnianian/siamese-prototype/issues>`_ for similar problems
4. Create a new issue describing your problem 