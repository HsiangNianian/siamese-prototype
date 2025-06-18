Performance Optimization
========================

This guide covers performance optimization techniques and best practices for Siamese Prototype.

Query Optimization
-----------------

### Limit Search Depth

Set appropriate `max_depth` parameters to prevent infinite recursion:

.. code-block:: python

   # Limit search depth for complex queries
   async for solution in engine.query("ancestor", "?A", "?D", max_depth=10):
       print(solution)

### Limit Solutions

Use `max_solutions` to prevent excessive result generation:

.. code-block:: python

   # Get only first 5 solutions
   async for solution in engine.query("person", "?P", max_solutions=5):
       print(solution)

### Optimize Rule Order

Place more specific rules before general ones:

.. code-block:: python

   # Specific rule first
   engine.add_rule(
       ("ancestor", "?A", "?D"),
       [("parent", "?A", "?D")]  # Direct parent
   )
   
   # General rule second
   engine.add_rule(
       ("ancestor", "?A", "?D"),
       [("parent", "?A", "?P"), ("ancestor", "?P", "?D")]  # Recursive
   )

Knowledge Base Optimization
--------------------------

### Index Frequently Used Facts

Group related facts together and use efficient data structures:

.. code-block:: python

   # Add facts in batches for better performance
   facts = [
       ("parent", "david", "john"),
       ("parent", "david", "sarah"),
       ("parent", "john", "mary"),
       # ... more facts
   ]
   
   for fact in facts:
       engine.add_fact(*fact)

### Use Efficient Built-ins

Implement custom built-ins for complex operations:

.. code-block:: python

   async def optimized_lookup(goal, bindings):
       """Optimized database lookup"""
       # Use connection pooling, caching, etc.
       result = await database.lookup(goal.args[0])
       if result:
           new_bindings = bindings.copy()
           new_bindings[goal.args[1]] = result
           yield new_bindings

Memory Management
----------------

### Configure Logging Levels

Use appropriate logging levels in production:

.. code-block:: python

   # Production logging - minimal overhead
   engine.configure_logging(level="WARNING")
   
   # Development logging - detailed tracing
   engine.configure_logging(level="TRACE")

### Reuse Engine Instances

Create engine instances once and reuse them:

.. code-block:: python

   # Good: Reuse engine instance
   engine = RuleEngine()
   engine.load_from_file("knowledge.yaml")
   
   async def process_queries(queries):
       for query in queries:
           async for solution in engine.query(*query):
               yield solution

Async Optimization
-----------------

### Concurrent Queries

Run multiple queries concurrently:

.. code-block:: python

   import asyncio
   
   async def concurrent_queries():
       engine = RuleEngine()
       engine.load_from_file("knowledge.yaml")
       
       # Run queries concurrently
       tasks = [
           engine.query("parent", "david", "?Child"),
           engine.query("sibling", "?S1", "?S2"),
           engine.query("grandparent", "?GP", "?GC")
       ]
       
       results = await asyncio.gather(*[collect_results(task) for task in tasks])
       return results
   
   async def collect_results(query_gen):
       results = []
       async for solution in query_gen:
           results.append(solution)
       return results

### Connection Pooling

Use connection pooling for external services:

.. code-block:: python

   import aiohttp
   
   class PooledHTTPBuiltin:
       def __init__(self):
           self.session = None
       
       async def get_session(self):
           if self.session is None:
               connector = aiohttp.TCPConnector(limit=100)
               self.session = aiohttp.ClientSession(connector=connector)
           return self.session
       
       async def http_get_json(self, goal, bindings):
           session = await self.get_session()
           url = goal.args[0]
           async with session.get(url) as response:
               if response.status == 200:
                   data = await response.json()
                   new_bindings = bindings.copy()
                   new_bindings[goal.args[1]] = data
                   yield new_bindings

Caching Strategies
-----------------

### Result Caching

Implement caching for expensive operations:

.. code-block:: python

   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def expensive_calculation(x, y):
       # Expensive computation
       return complex_math_operation(x, y)
   
   async def cached_builtin(goal, bindings):
       x = goal.args[0]
       y = goal.args[1]
       result = expensive_calculation(x, y)
       new_bindings = bindings.copy()
       new_bindings[goal.args[2]] = result
       yield new_bindings

### Knowledge Base Caching

Cache frequently accessed knowledge:

.. code-block:: python

   class CachedKnowledgeBase:
       def __init__(self):
           self.cache = {}
           self.engine = RuleEngine()
       
       async def query_with_cache(self, *args, **kwargs):
           cache_key = str(args) + str(kwargs)
           if cache_key in self.cache:
               return self.cache[cache_key]
           
           results = []
           async for solution in self.engine.query(*args, **kwargs):
               results.append(solution)
           
           self.cache[cache_key] = results
           return results

Profiling and Monitoring
-----------------------

### Query Performance Monitoring

Monitor query execution times:

.. code-block:: python

   import time
   import asyncio
   
   async def monitored_query(engine, *args, **kwargs):
       start_time = time.time()
       results = []
       
       async for solution in engine.query(*args, **kwargs):
           results.append(solution)
       
       execution_time = time.time() - start_time
       print(f"Query executed in {execution_time:.3f} seconds")
       return results

### Memory Usage Monitoring

Monitor memory usage:

.. code-block:: python

   import psutil
   import os
   
   def log_memory_usage():
       process = psutil.Process(os.getpid())
       memory_info = process.memory_info()
       print(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")

Best Practices Summary
---------------------

1. **Set appropriate limits**: Use `max_depth` and `max_solutions`
2. **Optimize rule order**: Place specific rules before general ones
3. **Use efficient built-ins**: Implement custom functions for complex operations
4. **Reuse engine instances**: Don't recreate engines unnecessarily
5. **Configure logging**: Use appropriate levels for production
6. **Implement caching**: Cache expensive operations and results
7. **Monitor performance**: Track execution times and memory usage
8. **Use connection pooling**: For external service calls
9. **Run queries concurrently**: When possible
10. **Profile regularly**: Identify bottlenecks

.. raw:: html

   <div class="admonition tip">
   <p class="admonition-title">Tip</p>
   <p>Always profile your specific use case. What works well for one application may not be optimal for another.</p>
   </div> 