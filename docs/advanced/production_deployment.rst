Production Deployment
=====================

This guide covers best practices for deploying Siamese Prototype in production environments.

Environment Setup
----------------

### Configuration Management

Use environment variables for configuration:

.. code-block:: python

   import os
   from siamese import RuleEngine
   
   class ProductionEngine:
       def __init__(self):
           self.engine = RuleEngine()
           
           # Load configuration from environment
           self.log_level = os.getenv('SIAMESE_LOG_LEVEL', 'INFO')
           self.max_depth = int(os.getenv('SIAMESE_MAX_DEPTH', '25'))
           self.max_solutions = int(os.getenv('SIAMESE_MAX_SOLUTIONS', '100'))
           
           # Configure engine
           self.engine.configure_logging(level=self.log_level)
       
       async def safe_query(self, *args, **kwargs):
           """Safe query with production limits"""
           kwargs.setdefault('max_depth', self.max_depth)
           kwargs.setdefault('max_solutions', self.max_solutions)
           
           return self.engine.query(*args, **kwargs)

### Docker Deployment

Create a Dockerfile for containerized deployment:

.. dockerfile

   FROM python:3.11-slim
   
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gcc \
       && rm -rf /var/lib/apt/lists/*
   
   # Copy requirements
   COPY pyproject.toml uv.lock ./
   
   # Install Python dependencies
   RUN pip install uv && uv sync --frozen
   
   # Copy application code
   COPY src/ ./src/
   COPY knowledge/ ./knowledge/
   
   # Create non-root user
   RUN useradd -m -u 1000 siamese && chown -R siamese:siamese /app
   USER siamese
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
       CMD python -c "import asyncio; from siamese import RuleEngine; asyncio.run(RuleEngine().query_one('test', 'value'))"
   
   # Default command
   CMD ["python", "-m", "your_app"]

### Kubernetes Deployment

Create Kubernetes manifests:

.. code-block:: yaml

   # deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: siamese-engine
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: siamese-engine
     template:
       metadata:
         labels:
           app: siamese-engine
       spec:
         containers:
         - name: siamese
           image: your-registry/siamese:latest
           ports:
           - containerPort: 8000
           env:
           - name: SIAMESE_LOG_LEVEL
             value: "INFO"
           - name: SIAMESE_MAX_DEPTH
             value: "25"
           resources:
             requests:
               memory: "256Mi"
               cpu: "250m"
             limits:
               memory: "512Mi"
               cpu: "500m"
           livenessProbe:
             httpGet:
               path: /health
               port: 8000
             initialDelaySeconds: 30
             periodSeconds: 10
           readinessProbe:
             httpGet:
               path: /ready
               port: 8000
             initialDelaySeconds: 5
             periodSeconds: 5

Performance Optimization
-----------------------

### Connection Pooling

Implement connection pooling for external services:

.. code-block:: python

   import aiohttp
   import asyncio
   from contextlib import asynccontextmanager
   
   class ConnectionPool:
       def __init__(self):
           self.session = None
           self._lock = asyncio.Lock()
       
       async def get_session(self):
           """Get or create HTTP session"""
           if self.session is None:
               async with self._lock:
                   if self.session is None:
                       connector = aiohttp.TCPConnector(
                           limit=100,
                           limit_per_host=30,
                           ttl_dns_cache=300
                       )
                       self.session = aiohttp.ClientSession(connector=connector)
           return self.session
       
       async def close(self):
           """Close session"""
           if self.session:
               await self.session.close()
               self.session = None
   
   # Global connection pool
   connection_pool = ConnectionPool()
   
   async def pooled_http_get(goal, bindings):
       """HTTP built-in with connection pooling"""
       session = await connection_pool.get_session()
       url = goal.args[0]
       
       async with session.get(url) as response:
           if response.status == 200:
               data = await response.json()
               new_bindings = bindings.copy()
               new_bindings[goal.args[1]] = data
               yield new_bindings

### Caching Strategy

Implement multi-level caching:

.. code-block:: python

   import asyncio
   from functools import lru_cache
   from typing import Dict, Any
   
   class CacheManager:
       def __init__(self):
           self.memory_cache = {}
           self.cache_lock = asyncio.Lock()
       
       async def get(self, key: str) -> Any:
           """Get value from cache"""
           async with self.cache_lock:
               return self.memory_cache.get(key)
       
       async def set(self, key: str, value: Any, ttl: int = 300):
           """Set value in cache with TTL"""
           async with self.cache_lock:
               self.memory_cache[key] = {
                   'value': value,
                   'expires': asyncio.get_event_loop().time() + ttl
               }
       
       async def cleanup(self):
           """Remove expired entries"""
           current_time = asyncio.get_event_loop().time()
           async with self.cache_lock:
               expired_keys = [
                   key for key, data in self.memory_cache.items()
                   if data['expires'] < current_time
               ]
               for key in expired_keys:
                   del self.memory_cache[key]
   
   # Global cache manager
   cache_manager = CacheManager()
   
   async def cached_builtin(goal, bindings):
       """Built-in with caching"""
       cache_key = f"{goal.name}:{goal.args}"
       
       # Try cache first
       cached_result = await cache_manager.get(cache_key)
       if cached_result:
           new_bindings = bindings.copy()
           new_bindings[goal.args[-1]] = cached_result
           yield new_bindings
           return
       
       # Perform expensive operation
       result = await expensive_operation(goal.args)
       
       # Cache result
       await cache_manager.set(cache_key, result, ttl=300)
       
       new_bindings = bindings.copy()
       new_bindings[goal.args[-1]] = result
       yield new_bindings

Monitoring and Observability
---------------------------

### Health Checks

Implement comprehensive health checks:

.. code-block:: python

   from fastapi import FastAPI, HTTPException
   import asyncio
   
   app = FastAPI()
   engine = None
   
   @app.on_event("startup")
   async def startup_event():
       global engine
       engine = ProductionEngine()
       await engine.load_knowledge_base()
   
   @app.get("/health")
   async def health_check():
       """Basic health check"""
       try:
           # Test basic query
           result = await engine.query_one("test", "value")
           return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}
       except Exception as e:
           raise HTTPException(status_code=503, detail=str(e))
   
   @app.get("/ready")
   async def readiness_check():
       """Readiness check"""
       if engine is None:
           raise HTTPException(status_code=503, detail="Engine not ready")
       return {"status": "ready"}
   
   @app.get("/metrics")
   async def metrics():
       """Application metrics"""
       return {
           "queries_processed": engine.query_count,
           "average_response_time": engine.avg_response_time,
           "memory_usage": engine.memory_usage,
           "uptime": engine.uptime
       }

### Logging Configuration

Configure structured logging for production:

.. code-block:: python

   import logging
   import json
   from datetime import datetime
   
   class StructuredLogger:
       def __init__(self):
           self.logger = logging.getLogger("siamese")
           self.logger.setLevel(logging.INFO)
           
           # JSON formatter
           formatter = logging.Formatter(
               '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
               '"message": "%(message)s", "module": "%(name)s"}'
           )
           
           # Console handler
           console_handler = logging.StreamHandler()
           console_handler.setFormatter(formatter)
           self.logger.addHandler(console_handler)
       
       def log_query(self, query, execution_time, success):
           """Log query execution"""
           self.logger.info(
               f"Query executed",
               extra={
                   "query": query,
                   "execution_time": execution_time,
                   "success": success,
                   "event_type": "query_execution"
               }
           )
       
       def log_error(self, error, context):
           """Log errors"""
           self.logger.error(
               f"Error occurred: {error}",
               extra={
                   "error": str(error),
                   "context": context,
                   "event_type": "error"
               }
           )

Security Considerations
----------------------

### Input Validation

Validate all inputs to prevent injection attacks:

.. code-block:: python

   import re
   from typing import Any
   
   class InputValidator:
       def __init__(self):
           self.allowed_predicates = {
               'parent', 'grandparent', 'sibling', 'user', 'permission'
           }
           self.max_args = 10
       
       def validate_query(self, *args) -> bool:
           """Validate query arguments"""
           if not args:
               return False
           
           predicate = args[0]
           if not isinstance(predicate, str):
               return False
           
           if predicate not in self.allowed_predicates:
               return False
           
           if len(args) > self.max_args:
               return False
           
           # Validate variable names
           for arg in args[1:]:
               if isinstance(arg, str) and arg.startswith('?'):
                   if not re.match(r'^\?[a-zA-Z_][a-zA-Z0-9_]*$', arg):
                       return False
           
           return True
   
   # Use in production engine
   validator = InputValidator()
   
   async def safe_query(engine, *args, **kwargs):
       """Safe query with validation"""
       if not validator.validate_query(*args):
           raise ValueError("Invalid query arguments")
       
       return engine.query(*args, **kwargs)

### Rate Limiting

Implement rate limiting to prevent abuse:

.. code-block:: python

   import time
   from collections import defaultdict
   
   class RateLimiter:
       def __init__(self, max_requests: int = 100, window: int = 60):
           self.max_requests = max_requests
           self.window = window
           self.requests = defaultdict(list)
       
       def is_allowed(self, client_id: str) -> bool:
           """Check if request is allowed"""
           now = time.time()
           
           # Clean old requests
           self.requests[client_id] = [
               req_time for req_time in self.requests[client_id]
               if now - req_time < self.window
           ]
           
           # Check limit
           if len(self.requests[client_id]) >= self.max_requests:
               return False
           
           # Record request
           self.requests[client_id].append(now)
           return True

### Authentication and Authorization

Implement proper authentication:

.. code-block:: python

   from fastapi import Depends, HTTPException, status
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
   
   security = HTTPBearer()
   
   async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
       """Verify JWT token"""
       token = credentials.credentials
       
       try:
           # Verify token (implement your JWT verification)
           payload = verify_jwt_token(token)
           return payload
       except Exception:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid authentication credentials"
           )
   
   @app.post("/query")
   async def execute_query(
       query: dict,
       user: dict = Depends(verify_token)
   ):
       """Execute query with authentication"""
       # Check user permissions
       if not has_permission(user, "execute_query"):
           raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail="Insufficient permissions"
           )
       
       # Execute query
       result = await engine.query(**query)
       return {"result": result}

Error Handling
-------------

### Graceful Degradation

Handle failures gracefully:

.. code-block:: python

   class ResilientEngine:
       def __init__(self):
           self.engine = RuleEngine()
           self.fallback_mode = False
       
       async def query_with_fallback(self, *args, **kwargs):
           """Query with fallback handling"""
           try:
               async for solution in self.engine.query(*args, **kwargs):
                   yield solution
           except Exception as e:
               # Log error
               logger.error(f"Query failed: {e}")
               
               # Switch to fallback mode
               self.fallback_mode = True
               
               # Return cached or simplified results
               yield from self.get_fallback_results(*args)
       
       async def get_fallback_results(self, *args):
           """Get fallback results"""
           # Implement fallback logic
           pass

### Circuit Breaker

Implement circuit breaker pattern:

.. code-block:: python

   import asyncio
   from enum import Enum
   
   class CircuitState(Enum):
       CLOSED = "closed"
       OPEN = "open"
       HALF_OPEN = "half_open"
   
   class CircuitBreaker:
       def __init__(self, failure_threshold: int = 5, timeout: int = 60):
           self.failure_threshold = failure_threshold
           self.timeout = timeout
           self.state = CircuitState.CLOSED
           self.failure_count = 0
           self.last_failure_time = 0
       
       async def call(self, func, *args, **kwargs):
           """Execute function with circuit breaker"""
           if self.state == CircuitState.OPEN:
               if time.time() - self.last_failure_time > self.timeout:
                   self.state = CircuitState.HALF_OPEN
               else:
                   raise Exception("Circuit breaker is open")
           
           try:
               result = await func(*args, **kwargs)
               self.on_success()
               return result
           except Exception as e:
               self.on_failure()
               raise e
       
       def on_success(self):
           """Handle successful call"""
           self.failure_count = 0
           self.state = CircuitState.CLOSED
       
       def on_failure(self):
           """Handle failed call"""
           self.failure_count += 1
           self.last_failure_time = time.time()
           
           if self.failure_count >= self.failure_threshold:
               self.state = CircuitState.OPEN

Deployment Checklist
-------------------

1. **Environment Configuration**
   - Set appropriate log levels
   - Configure resource limits
   - Set up environment variables

2. **Security**
   - Implement authentication
   - Validate all inputs
   - Use HTTPS in production
   - Set up rate limiting

3. **Monitoring**
   - Configure health checks
   - Set up metrics collection
   - Implement structured logging
   - Set up alerting

4. **Performance**
   - Use connection pooling
   - Implement caching
   - Set appropriate timeouts
   - Monitor resource usage

5. **Reliability**
   - Implement circuit breakers
   - Add graceful degradation
   - Set up backups
   - Test failure scenarios

6. **Scalability**
   - Use load balancing
   - Implement horizontal scaling
   - Monitor performance metrics
   - Plan for growth

.. raw:: html

   <div class="admonition tip">
   <p class="admonition-title">Tip</p>
   <p>Start with a simple deployment and gradually add complexity. Monitor everything and be prepared to iterate based on real-world usage patterns.</p>
   </div> 