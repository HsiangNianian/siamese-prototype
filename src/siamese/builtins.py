from typing import AsyncGenerator, Callable
import aiohttp
from .core import Bindings, Goal, UnificationError, Variable
from .unification import Unificator

# A type alias for async built-in functions
AsyncBuiltin = Callable[[Goal, Bindings], AsyncGenerator[Bindings, None]]

async def neq_builtin(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """Succeeds if term1 is not unifiable with term2."""
    term1 = Unificator.substitute(goal.args[0], bindings)
    term2 = Unificator.substitute(goal.args[1], bindings)
    if Unificator.unify(term1, term2, {}) is None:
        yield bindings

async def http_get_json(goal: Goal, bindings: Bindings) -> AsyncGenerator[Bindings, None]:
    """
    Performs an async HTTP GET request and unifies the JSON response with a variable.
    Example: http_get_json('https://httpbin.org/get', ?Response)
    """
    url_term = Unificator.substitute(goal.args[0], bindings)
    result_var = goal.args[1]

    if not isinstance(url_term, str) or not isinstance(result_var, Variable):
        return # Fails if arguments are not of the correct type

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url_term) as response:
                response.raise_for_status()
                json_data = await response.json()
                
                # Try to unify the fetched data with the result variable
                new_bindings = Unificator.unify(result_var, json_data, bindings)
                if new_bindings:
                    yield new_bindings
    except Exception:
        # Fails silently on any network or parsing error
        return

DEFAULT_BUILTINS: dict[str, AsyncBuiltin] = {
    "neq": neq_builtin,
    "http_get_json": http_get_json,
} 