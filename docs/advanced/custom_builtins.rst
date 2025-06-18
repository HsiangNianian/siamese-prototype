Custom Built-in Functions
=========================

This guide explains how to create custom async built-in functions to extend Siamese Prototype's capabilities.

Built-in Function Basics
-----------------------

A built-in function is an async generator function that takes two parameters:

- `goal`: The current goal being processed
- `bindings`: Current variable bindings

The function should yield new binding dictionaries when successful.

Basic Structure
--------------

.. code-block:: python

   async def my_builtin(goal, bindings):
       """
       Custom built-in function
       
       Args:
           goal: Current goal (Term object)
           bindings: Current variable bindings (dict)
       
       Yields:
           dict: New bindings when successful
       """
       # Extract arguments from goal
       arg1 = goal.args[0]
       arg2 = goal.args[1]
       
       # Perform your logic
       result = await some_async_operation(arg1, arg2)
       
       if result:
           # Create new bindings
           new_bindings = bindings.copy()
           new_bindings[goal.args[2]] = result
           yield new_bindings

Registering Built-ins
--------------------

Register custom built-ins when creating the engine:

.. code-block:: python

   from siamese import RuleEngine
   
   # Define your custom built-ins
   custom_builtins = {
       "my_builtin": my_builtin,
       "http_get": http_get_builtin,
       "database_query": db_query_builtin
   }
   
   # Create engine with custom built-ins
   engine = RuleEngine(builtins=custom_builtins)

Common Patterns
--------------

### HTTP Requests

.. code-block:: python

   import aiohttp
   
   async def http_get_json(goal, bindings):
       """Fetch JSON data from URL"""
       url = goal.args[0]
       var_name = goal.args[1]
       
       async with aiohttp.ClientSession() as session:
           async with session.get(url) as response:
               if response.status == 200:
                   data = await response.json()
                   new_bindings = bindings.copy()
                   new_bindings[var_name] = data
                   yield new_bindings

### Database Queries

.. code-block:: python

   import asyncpg
   
   async def db_query(goal, bindings):
       """Execute database query"""
       query = goal.args[0]
       var_name = goal.args[1]
       
       # Get database connection from bindings or global
       conn = await get_db_connection()
       
       try:
           result = await conn.fetch(query)
           new_bindings = bindings.copy()
           new_bindings[var_name] = result
           yield new_bindings
       finally:
           await conn.close()

### File Operations

.. code-block:: python

   import aiofiles
   
   async def read_file(goal, bindings):
       """Read file content"""
       filepath = goal.args[0]
       var_name = goal.args[1]
       
       async with aiofiles.open(filepath, 'r') as f:
           content = await f.read()
           new_bindings = bindings.copy()
           new_bindings[var_name] = content
           yield new_bindings

### Mathematical Operations

.. code-block:: python

   import math
   
   async def calculate_sqrt(goal, bindings):
       """Calculate square root"""
       number = goal.args[0]
       var_name = goal.args[1]
       
       if isinstance(number, (int, float)) and number >= 0:
           result = math.sqrt(number)
           new_bindings = bindings.copy()
           new_bindings[var_name] = result
           yield new_bindings

### Conditional Logic

.. code-block:: python

   async def if_then_else(goal, bindings):
       """Conditional execution"""
       condition = goal.args[0]
       then_value = goal.args[1]
       else_value = goal.args[2]
       var_name = goal.args[3]
       
       # Evaluate condition
       if condition:
           result = then_value
       else:
           result = else_value
       
       new_bindings = bindings.copy()
       new_bindings[var_name] = result
       yield new_bindings

Advanced Patterns
----------------

### Multiple Results

Some built-ins can yield multiple results:

.. code-block:: python

   async def search_users(goal, bindings):
       """Search users by criteria"""
       criteria = goal.args[0]
       var_name = goal.args[1]
       
       # Search database
       users = await search_database(criteria)
       
       # Yield each user as a separate result
       for user in users:
           new_bindings = bindings.copy()
           new_bindings[var_name] = user
           yield new_bindings

### Error Handling

Handle errors gracefully:

.. code-block:: python

   async def safe_http_get(goal, bindings):
       """Safe HTTP request with error handling"""
       url = goal.args[0]
       var_name = goal.args[1]
       
       try:
           async with aiohttp.ClientSession() as session:
               async with session.get(url, timeout=10) as response:
                   if response.status == 200:
                       data = await response.json()
                       new_bindings = bindings.copy()
                       new_bindings[var_name] = data
                       yield new_bindings
       except Exception as e:
           # Log error but don't fail the query
           print(f"HTTP request failed: {e}")
           # Optionally yield error information
           new_bindings = bindings.copy()
           new_bindings[var_name] = {"error": str(e)}
           yield new_bindings

### Caching

Implement caching for expensive operations:

.. code-block:: python

   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_expensive_operation(x):
       # Expensive computation
       return complex_calculation(x)
   
   async def cached_builtin(goal, bindings):
       """Built-in with caching"""
       input_value = goal.args[0]
       var_name = goal.args[1]
       
       result = cached_expensive_operation(input_value)
       new_bindings = bindings.copy()
       new_bindings[var_name] = result
       yield new_bindings

### Stateful Built-ins

Built-ins can maintain state:

.. code-block:: python

   class CounterBuiltin:
       def __init__(self):
           self.counter = 0
       
       async def __call__(self, goal, bindings):
           """Increment counter"""
           var_name = goal.args[0]
           
           self.counter += 1
           new_bindings = bindings.copy()
           new_bindings[var_name] = self.counter
           yield new_bindings

Using Built-ins in Rules
-----------------------

Define rules that use your custom built-ins:

.. code-block:: python

   # Rule using HTTP built-in
   engine.add_rule(
       ("user_info", "?Username", "?Info"),
       [("http_get_json", "https://api.github.com/users/?Username", "?Info")]
   )
   
   # Rule using database built-in
   engine.add_rule(
       ("user_profile", "?UserId", "?Profile"),
       [("db_query", "SELECT * FROM users WHERE id = ?UserId", "?Profile")]
   )
   
   # Rule using mathematical built-in
   engine.add_rule(
       ("distance", "?X1", "?Y1", "?X2", "?Y2", "?Dist"),
       [
           ("subtract", "?X2", "?X1", "?DX"),
           ("subtract", "?Y2", "?Y1", "?DY"),
           ("multiply", "?DX", "?DX", "?DX2"),
           ("multiply", "?DY", "?DY", "?DY2"),
           ("add", "?DX2", "?DY2", "?Sum"),
           ("calculate_sqrt", "?Sum", "?Dist")
       ]
   )

Testing Built-ins
----------------

Test your custom built-ins:

.. code-block:: python

   import pytest
   import pytest_asyncio
   
   @pytest.mark.asyncio
   async def test_http_get_builtin():
       # Test HTTP built-in
       goal = Term("http_get_json", ["https://httpbin.org/json", "?Result"])
       bindings = {}
       
       results = []
       async for new_bindings in http_get_json(goal, bindings):
           results.append(new_bindings)
       
       assert len(results) == 1
       assert "?Result" in results[0]
       assert "slideshow" in results[0]["?Result"]

Best Practices
-------------

1. **Handle errors gracefully**: Don't let built-ins crash the entire query
2. **Use appropriate timeouts**: For external service calls
3. **Implement caching**: For expensive operations
4. **Keep built-ins focused**: Each built-in should do one thing well
5. **Document your built-ins**: Explain parameters and behavior
6. **Test thoroughly**: Ensure built-ins work correctly
7. **Consider performance**: Built-ins can be bottlenecks
8. **Use async properly**: Don't block the event loop
9. **Validate inputs**: Check argument types and values
10. **Log operations**: For debugging and monitoring

.. raw:: html

   <div class="admonition tip">
   <p class="admonition-title">Tip</p>
   <p>Start with simple built-ins and gradually add complexity. Test each built-in thoroughly before using it in production rules.</p>
   </div> 