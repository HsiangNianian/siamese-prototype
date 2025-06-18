Knowledge Base Management
==========================

This guide covers advanced techniques for managing large and complex knowledge bases in Siamese Prototype.

Knowledge Base Organization
---------------------------

### Modular Knowledge Bases

Split large knowledge bases into modules:

.. code-block:: yaml

   # users.yaml
   facts:
     - [user, alice, admin]
     - [user, bob, user]
     - [user, charlie, guest]
   
   rules:
     - head: [admin_user, '?User']
       body:
         - [user, '?User', admin]

.. code-block:: yaml

   # permissions.yaml
   facts:
     - [permission, read, file]
     - [permission, write, file]
     - [permission, execute, program]
   
   rules:
     - head: [can_access, '?User', '?Resource']
       body:
         - [user, '?User', '?Role']
         - [permission, '?Action', '?Resource']
         - [role_has_permission, '?Role', '?Action']

Loading Multiple Files
---------------------

.. code-block:: python

   class KnowledgeManager:
       def __init__(self):
           self.engine = RuleEngine()
       
       def load_modules(self, module_files):
           """Load multiple knowledge base modules"""
           for file_path in module_files:
               try:
                   self.engine.load_from_file(file_path)
                   print(f"Loaded: {file_path}")
               except Exception as e:
                   print(f"Failed to load {file_path}: {e}")
       
       def load_all(self, directory="knowledge"):
           """Load all YAML files from directory"""
           import glob
           yaml_files = glob.glob(f"{directory}/*.yaml")
           self.load_modules(yaml_files)

Knowledge Base Validation
------------------------

### Schema Validation

Validate knowledge base structure:

.. code-block:: python

   import yaml
   from typing import Dict, List, Any
   
   class KnowledgeValidator:
       def __init__(self):
           self.schema = {
               "facts": list,
               "rules": list
           }
       
       def validate_file(self, file_path: str) -> bool:
           """Validate knowledge base file"""
           try:
               with open(file_path, 'r') as f:
                   data = yaml.safe_load(f)
               
               return self.validate_structure(data)
           except Exception as e:
               print(f"Validation error in {file_path}: {e}")
               return False
       
       def validate_structure(self, data: Dict[str, Any]) -> bool:
           """Validate data structure"""
           for key, expected_type in self.schema.items():
               if key not in data:
                   print(f"Missing required key: {key}")
                   return False
               if not isinstance(data[key], expected_type):
                   print(f"Invalid type for {key}")
                   return False
           return True

### Rule Validation

Validate rule syntax and logic:

.. code-block:: python

   class RuleValidator:
       def validate_rule(self, rule_data: Dict[str, Any]) -> bool:
           """Validate individual rule"""
           if "head" not in rule_data or "body" not in rule_data:
               return False
           
           head = rule_data["head"]
           body = rule_data["body"]
           
           # Check head is a list/tuple
           if not isinstance(head, (list, tuple)):
               return False
           
           # Check body is a list of lists/tuples
           if not isinstance(body, list):
               return False
           
           for goal in body:
               if not isinstance(goal, (list, tuple)):
                   return False
           
           return True

Knowledge Base Versioning
------------------------

### Version Control Integration

Track knowledge base changes:

.. code-block:: python

   import hashlib
   import json
   from datetime import datetime
   
   class KnowledgeVersioner:
       def __init__(self):
           self.versions = []
       
       def create_version(self, knowledge_data: Dict[str, Any]) -> str:
           """Create version hash for knowledge base"""
           # Create hash of knowledge content
           content = json.dumps(knowledge_data, sort_keys=True)
           version_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
           
           version_info = {
               "hash": version_hash,
               "timestamp": datetime.now().isoformat(),
               "content": knowledge_data
           }
           
           self.versions.append(version_info)
           return version_hash
       
       def get_version(self, version_hash: str) -> Dict[str, Any]:
           """Get knowledge base by version"""
           for version in self.versions:
               if version["hash"] == version_hash:
                   return version["content"]
           return None

Knowledge Base Migration
-----------------------

### Migration Scripts

Handle knowledge base schema changes:

.. code-block:: python

   class KnowledgeMigrator:
       def __init__(self):
           self.migrations = []
       
       def add_migration(self, version: str, migration_func):
           """Add migration function"""
           self.migrations.append((version, migration_func))
       
       def migrate(self, knowledge_data: Dict[str, Any], target_version: str) -> Dict[str, Any]:
           """Migrate knowledge base to target version"""
           current_data = knowledge_data.copy()
           
           for version, migration_func in self.migrations:
               if version <= target_version:
                   current_data = migration_func(current_data)
           
           return current_data
   
   # Example migration
   def migrate_v1_to_v2(data):
       """Migrate from v1 to v2 schema"""
       # Convert old format to new format
       if "old_facts" in data:
           data["facts"] = data.pop("old_facts")
       return data

Knowledge Base Backup
--------------------

### Automated Backups

Create backup strategies:

.. code-block:: python

   import shutil
   import os
   from datetime import datetime
   
   class KnowledgeBackup:
       def __init__(self, backup_dir: str = "backups"):
           self.backup_dir = backup_dir
           os.makedirs(backup_dir, exist_ok=True)
       
       def create_backup(self, knowledge_files: List[str]) -> str:
           """Create backup of knowledge files"""
           timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
           backup_name = f"kb_backup_{timestamp}"
           backup_path = os.path.join(self.backup_dir, backup_name)
           
           os.makedirs(backup_path, exist_ok=True)
           
           for file_path in knowledge_files:
               if os.path.exists(file_path):
                   shutil.copy2(file_path, backup_path)
           
           return backup_path
       
       def restore_backup(self, backup_path: str, target_dir: str):
           """Restore knowledge base from backup"""
           if os.path.exists(backup_path):
               for file_name in os.listdir(backup_path):
                   source = os.path.join(backup_path, file_name)
                   target = os.path.join(target_dir, file_name)
                   shutil.copy2(source, target)

Knowledge Base Testing
---------------------

### Automated Testing

Test knowledge base integrity:

.. code-block:: python

   import pytest
   import pytest_asyncio
   
   class KnowledgeTester:
       def __init__(self, engine: RuleEngine):
           self.engine = engine
       
       async def test_facts(self, test_cases: List[tuple]) -> bool:
           """Test that facts are correctly loaded"""
           for predicate, *args in test_cases:
               result = await self.engine.exists(predicate, *args)
               if not result:
                   print(f"Fact test failed: {predicate}({args})")
                   return False
           return True
       
       async def test_rules(self, test_cases: List[tuple]) -> bool:
           """Test that rules work correctly"""
           for query, expected_results in test_cases:
               results = []
               async for solution in self.engine.query(*query):
                   results.append(solution)
               
               if len(results) != len(expected_results):
                   print(f"Rule test failed: {query}")
                   return False
           
           return True
   
   # Example usage
   @pytest.mark.asyncio
   async def test_knowledge_base():
       engine = RuleEngine()
       engine.load_from_file("knowledge.yaml")
       
       tester = KnowledgeTester(engine)
       
       # Test facts
       fact_tests = [
           ("parent", "david", "john"),
           ("user", "alice", "admin")
       ]
       assert await tester.test_facts(fact_tests)
       
       # Test rules
       rule_tests = [
           (("grandparent", "david", "?GC"), [{"?GC": "mary"}]),
           (("admin_user", "?User"), [{"?User": "alice"}])
       ]
       assert await tester.test_rules(rule_tests)

Knowledge Base Monitoring
------------------------

### Usage Analytics

Monitor knowledge base usage:

.. code-block:: python

   class KnowledgeMonitor:
       def __init__(self):
           self.query_stats = {}
           self.rule_stats = {}
       
       def record_query(self, predicate: str, execution_time: float):
           """Record query statistics"""
           if predicate not in self.query_stats:
               self.query_stats[predicate] = {
                   "count": 0,
                   "total_time": 0,
                   "avg_time": 0
               }
           
           stats = self.query_stats[predicate]
           stats["count"] += 1
           stats["total_time"] += execution_time
           stats["avg_time"] = stats["total_time"] / stats["count"]
       
       def get_stats(self) -> Dict[str, Any]:
           """Get monitoring statistics"""
           return {
               "query_stats": self.query_stats,
               "rule_stats": self.rule_stats
           }

Best Practices
-------------

1. **Organize by domain**: Split knowledge bases by business domain
2. **Use consistent naming**: Follow naming conventions for predicates
3. **Validate regularly**: Check knowledge base integrity
4. **Version control**: Track changes to knowledge bases
5. **Backup frequently**: Create regular backups
6. **Test thoroughly**: Validate rules and facts
7. **Monitor usage**: Track performance and usage patterns
8. **Document changes**: Keep change logs
9. **Use migrations**: Handle schema changes gracefully
10. **Optimize structure**: Organize for performance

.. raw:: html

   <div class="admonition tip">
   <p class="admonition-title">Tip</p>
   <p>Start with a simple knowledge base structure and evolve it as your needs grow. Regular validation and testing will help maintain quality.</p>
   </div> 