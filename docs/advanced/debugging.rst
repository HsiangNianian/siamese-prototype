Debugging and Troubleshooting
=============================

This guide covers debugging techniques and common troubleshooting scenarios for Siamese Prototype.

Debugging Techniques
-------------------

### Enable Detailed Logging

Use TRACE level logging to see detailed execution flow:

.. code-block:: python

   # Enable detailed tracing
   engine.configure_logging(level="TRACE")
   
   # Run your query
   async for solution in engine.query("grandparent", "david", "?GC"):
       print(solution)

This will show:
- Goal calls and exits
- Rule applications
- Variable bindings
- Built-in function calls

### Query Analysis

Analyze query execution step by step:

.. code-block:: python

   class QueryAnalyzer:
       def __init__(self, engine):
           self.engine = engine
           self.trace_events = []
       
       async def analyze_query(self, *args, **kwargs):
           """Analyze query execution"""
           print(f"Analyzing query: {args}")
           
           async for event in self.engine.query(*args, **kwargs):
               if hasattr(event, 'type'):  # TraceEvent
                   self.trace_events.append(event)
                   print(f"  {event.type}: {event.goal} (depth: {event.depth})")
               else:  # Solution
                   print(f"  SOLUTION: {event}")
           
           return self.trace_events

### Rule Testing

Test individual rules in isolation:

.. code-block:: python

   async def test_rule(engine, rule_head, rule_body, test_cases):
       """Test a specific rule"""
       print(f"Testing rule: {rule_head} :- {rule_body}")
       
       for test_input, expected_output in test_cases:
           print(f"  Input: {test_input}")
           
           # Create temporary engine with just this rule
           test_engine = RuleEngine()
           test_engine.add_rule(rule_head, rule_body)
           
           # Add test facts
           for fact in test_input.get('facts', []):
               test_engine.add_fact(*fact)
           
           # Run query
           results = []
           async for solution in test_engine.query(*test_input['query']):
               results.append(solution)
           
           print(f"  Expected: {expected_output}")
           print(f"  Got: {results}")
           print(f"  {'✓' if results == expected_output else '✗'}")

Common Issues
------------

### Infinite Recursion

**Problem**: Query runs indefinitely

**Causes**:
- Missing base case in recursive rules
- Circular rule dependencies
- Incorrect rule ordering

**Solutions**:

.. code-block:: python

   # Problematic rule (no base case)
   engine.add_rule(
       ("ancestor", "?A", "?D"),
       [("parent", "?A", "?P"), ("ancestor", "?P", "?D")]
   )
   
   # Fixed rule (with base case)
   engine.add_rule(
       ("ancestor", "?A", "?D"),
       [("parent", "?A", "?D")]  # Base case
   )
   engine.add_rule(
       ("ancestor", "?A", "?D"),
       [("parent", "?A", "?P"), ("ancestor", "?P", "?D")]  # Recursive case
   )

### No Solutions Found

**Problem**: Query returns no results

**Causes**:
- Missing facts
- Incorrect variable names
- Rule doesn't match query

**Debugging**:

.. code-block:: python

   async def debug_no_solutions(engine, query):
       """Debug why no solutions are found"""
       print(f"Debugging query: {query}")
       
       # Check if facts exist
       predicate = query[0]
       print(f"Checking facts for predicate: {predicate}")
       
       # List all facts for this predicate
       # (This would require engine modification to expose facts)
       
       # Check rule heads
       print(f"Checking rules for predicate: {predicate}")
       
       # Test with simpler queries
       for i, arg in enumerate(query[1:], 1):
           if isinstance(arg, str) and arg.startswith('?'):
               print(f"  Testing variable {arg} at position {i}")
               # Try with concrete values

### Variable Binding Issues

**Problem**: Variables not bound correctly

**Causes**:
- Variable name mismatches
- Incorrect unification
- Built-in function issues

**Debugging**:

.. code-block:: python

   async def debug_variable_bindings(engine, query):
       """Debug variable binding issues"""
       print(f"Debugging variable bindings for: {query}")
       
       # Enable detailed logging
       engine.configure_logging(level="TRACE")
       
       # Run query and capture all bindings
       bindings_history = []
       
       async for event in engine.query(*query):
           if hasattr(event, 'type') and event.type == 'EXIT':
               # This would require engine modification to capture bindings
               print(f"  Goal {event.goal} succeeded")
       
       return bindings_history

### Built-in Function Errors

**Problem**: Custom built-ins fail

**Debugging**:

.. code-block:: python

   async def debug_builtin(builtin_func, goal, bindings):
       """Debug custom built-in function"""
       print(f"Debugging built-in: {builtin_func.__name__}")
       print(f"  Goal: {goal}")
       print(f"  Bindings: {bindings}")
       
       try:
           results = []
           async for new_bindings in builtin_func(goal, bindings):
               results.append(new_bindings)
               print(f"  Yielded: {new_bindings}")
           
           print(f"  Total results: {len(results)}")
           return results
       except Exception as e:
           print(f"  Error: {e}")
           import traceback
           traceback.print_exc()
           return []

Performance Issues
-----------------

### Slow Queries

**Problem**: Queries take too long

**Diagnosis**:

.. code-block:: python

   import time
   
   async def profile_query(engine, *args, **kwargs):
       """Profile query performance"""
       start_time = time.time()
       
       results = []
       async for solution in engine.query(*args, **kwargs):
           results.append(solution)
       
       execution_time = time.time() - start_time
       
       print(f"Query executed in {execution_time:.3f} seconds")
       print(f"Found {len(results)} solutions")
       
       return results, execution_time

**Solutions**:
- Set appropriate `max_depth` and `max_solutions`
- Optimize rule order
- Use caching for expensive operations
- Consider query rewriting

### Memory Issues

**Problem**: High memory usage

**Diagnosis**:

.. code-block:: python

   import psutil
   import os
   
   def monitor_memory():
       """Monitor memory usage"""
       process = psutil.Process(os.getpid())
       memory_info = process.memory_info()
       print(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
       return memory_info.rss

**Solutions**:
- Limit solution count
- Use generators instead of lists
- Clear caches periodically
- Monitor for memory leaks

Debugging Tools
--------------

### Interactive Debugger

Create an interactive debugging session:

.. code-block:: python

   class InteractiveDebugger:
       def __init__(self, engine):
           self.engine = engine
           self.breakpoints = set()
       
       def add_breakpoint(self, predicate):
           """Add breakpoint for predicate"""
           self.breakpoints.add(predicate)
       
       async def debug_query(self, *args):
           """Run query with interactive debugging"""
           print(f"Starting debug session for: {args}")
           
           async for event in self.engine.query(*args):
               if hasattr(event, 'type') and event.type == 'CALL':
                   if event.goal.name in self.breakpoints:
                       print(f"Breakpoint hit: {event.goal}")
                       input("Press Enter to continue...")
               
               print(f"  {event}")

### Query Visualizer

Visualize query execution:

.. code-block:: python

   class QueryVisualizer:
       def __init__(self):
           self.execution_tree = []
       
       def add_node(self, goal, depth, result):
           """Add execution node"""
           self.execution_tree.append({
               'goal': goal,
               'depth': depth,
               'result': result,
               'timestamp': time.time()
           })
       
       def print_tree(self):
           """Print execution tree"""
           for node in self.execution_tree:
               indent = "  " * node['depth']
               status = "✓" if node['result'] else "✗"
               print(f"{indent}{status} {node['goal']}")

### Rule Validator

Validate rule syntax and logic:

.. code-block:: python

   class RuleValidator:
       def validate_rule(self, head, body):
           """Validate rule structure"""
           errors = []
           
           # Check head
           if not isinstance(head, (list, tuple)):
               errors.append("Head must be a list or tuple")
           
           # Check body
           if not isinstance(body, list):
               errors.append("Body must be a list")
           
           for goal in body:
               if not isinstance(goal, (list, tuple)):
                   errors.append(f"Body goal must be list/tuple: {goal}")
           
           # Check for circular dependencies
           if self.has_circular_dependency(head, body):
               errors.append("Rule has circular dependency")
           
           return errors
       
       def has_circular_dependency(self, head, body):
           """Check for circular dependencies"""
           # Implementation would check if head predicate appears in body
           # in a way that could cause infinite recursion
           return False

Best Practices
-------------

1. **Start with simple queries**: Test basic functionality first
2. **Use logging**: Enable TRACE level for debugging
3. **Test rules individually**: Verify each rule works correctly
4. **Check variable names**: Ensure consistency across rules
5. **Monitor performance**: Profile slow queries
6. **Validate input**: Check data types and formats
7. **Handle errors gracefully**: Don't let built-ins crash
8. **Document assumptions**: Note expected behavior
9. **Use breakpoints**: Set strategic debugging points
10. **Keep backups**: Save working configurations

.. raw:: html

   <div class="admonition tip">
   <p class="admonition-title">Tip</p>
   <p>When debugging, start with the simplest possible case and gradually add complexity. This helps isolate the source of problems.</p>
   </div> 