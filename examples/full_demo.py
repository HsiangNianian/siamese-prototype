import asyncio
from siamese import RuleEngine
from loguru import logger

async def main():
    """Demonstrates the full capabilities of the async RuleEngine."""
    
    # 1. Initialize the engine and configure logging for detailed tracing
    engine = RuleEngine()
    engine.configure_logging(level="TRACE") # Use "INFO" for less verbose output
    
    # 2. Load knowledge base from an external YAML file
    try:
        engine.load_from_file("examples/knowledge.yaml")
    except Exception as e:
        logger.critical(f"Failed to initialize engine from config: {e}")
        return

    # --- Query 1: Test a rule with a synchronous built-in ('neq') ---
    logger.info("\n--- Querying for siblings of 'john' ---")
    solutions = []
    # The new query method is an async generator
    async for sol in engine.query("sibling", "john", "?S"):
        solutions.append(sol)
        
    if solutions:
        for sol in solutions:
            logger.info(f"Solution: john's sibling is {sol['?S']}")
    else:
        logger.info("No siblings found for john.")

    # --- Query 2: Test the 'exists' convenience method ---
    logger.info("\n--- Checking if 'john' and 'mary' are siblings ---")
    are_siblings = await engine.exists("sibling", "john", "mary")
    logger.info(f"Are john and mary siblings? {'Yes' if are_siblings else 'No'}")

    # --- Query 3: Test a rule with an ASYNCHRONOUS built-in ('http_get_json') ---
    logger.info("\n--- Querying for an external resource using an async built-in ---")
    # This query will make a real HTTP request without blocking the event loop.
    logger.info("Goal: http_get_json('https://httpbin.org/get', ?Response)")
    
    # We use query_one for simplicity
    http_solution = await engine.query_one("http_get_json", "https://httpbin.org/get", "?Response")

    if http_solution:
        response_data = http_solution['?Response']
        ip = response_data.get('origin')
        logger.success(f"Successfully fetched data from httpbin. Your IP appears to be: {ip}")
        # You could now use this IP in further logic...
        # For example: await engine.exists("is_allowed_ip", ip)
    else:
        logger.error("Failed to get a response from the http_get_json built-in.")


if __name__ == "__main__":
    # To run this, you must have installed the package and its dependencies:
    # uv sync
    asyncio.run(main()) 