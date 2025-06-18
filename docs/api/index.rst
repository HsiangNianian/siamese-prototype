API Reference
=============

This section provides complete API reference documentation for Siamese Prototype.

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   rule_engine
   knowledge_base
   core
   builtins
   resolver
   unification

Main Modules
------------

* :doc:`rule_engine` - Main rule engine class
* :doc:`knowledge_base` - Knowledge base management
* :doc:`core` - Core data structures (Term, Variable, Rule, etc.)
* :doc:`builtins` - Built-in functions
* :doc:`resolver` - Query resolver
* :doc:`unification` - Unification algorithm

Quick Imports
------------

.. code-block:: python

   from siamese import RuleEngine
   from siamese.core import Variable, Term, Rule
   from siamese.builtins import DEFAULT_BUILTINS

.. raw:: html

   <div class="admonition note">
   <p class="admonition-title">Note</p>
   <p>Most users only need to use the <code>RuleEngine</code> class. Other modules are mainly for advanced usage and extensions.</p>
   </div> 