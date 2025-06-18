Contributing Guide
=================

Thank you for your interest in the Siamese Prototype project! We welcome all forms of contributions, including code, documentation, tests, bug reports, and feature suggestions.

Ways to Contribute
-----------------

* 🐛 **Bug Reports**: Report bugs in GitHub Issues
* 💡 **Feature Suggestions**: Propose new features or improvements
* 🔧 **Code Contributions**: Submit Pull Requests
* 📚 **Documentation Improvements**: Improve or translate documentation
* 🧪 **Tests**: Add test cases or improve test coverage

Development Environment Setup
----------------------------

1. **Clone the repository**

   .. code-block:: bash

      git clone https://github.com/hsiangnianian/siamese-prototype.git
      cd siamese-prototype

2. **Install dependencies**

   .. code-block:: bash

      uv sync

3. **Run tests**

   .. code-block:: bash

      uv run pytest

4. **Run code checks**

   .. code-block:: bash

      uv run mypy src/
      uv run black src/ tests/
      uv run isort src/ tests/

Code Style
----------

We use the following tools to maintain code quality:

* **Black**: Code formatting
* **isort**: Import sorting
* **mypy**: Type checking
* **pytest**: Testing framework

Code style guidelines:

* Use 4 spaces for indentation
* Line length limit of 88 characters (Black default)
* Use type annotations
* Write docstrings
* Follow PEP 8 standards

Submitting Pull Requests
-----------------------

1. **Create a branch**

   .. code-block:: bash

      git checkout -b feature/your-feature-name
      # or
      git checkout -b fix/your-bug-fix

2. **Make changes**

   Write code, add tests, update documentation, etc.

3. **Run tests**

   .. code-block:: bash

      uv run pytest
      uv run mypy src/

4. **Commit changes**

   .. code-block:: bash

      git add .
      git commit -m "feat: add new feature description"
      git push origin feature/your-feature-name

5. **Create Pull Request**

   Create a Pull Request on GitHub and fill out the template.

Commit Message Standards
-----------------------

We use the `Conventional Commits` standard:

* `feat:` - New feature
* `fix:` - Bug fix
* `docs:` - Documentation changes
* `style:` - Code style changes (no functional impact)
* `refactor:` - Code refactoring
* `test:` - Add or modify tests
* `chore:` - Build process or auxiliary tool changes

Examples:

.. code-block:: text

   feat: add support for custom built-in functions
   fix: resolve variable renaming issue in resolver
   docs: update installation guide
   test: add tests for async built-ins

Testing Guidelines
-----------------

* All new features should have corresponding tests
* Tests should cover normal cases and edge cases
* Use `pytest-asyncio` for async tests
* Test file naming: `test_*.py`

Example test:

.. code-block:: python

   import pytest
   import pytest_asyncio
   from siamese import RuleEngine

   @pytest_asyncio.fixture
   async def engine():
       return RuleEngine()

   @pytest.mark.asyncio
   async def test_basic_fact_query(engine):
       engine.add_fact("test", "value")
       result = await engine.query_one("test", "?X")
       assert result == {"?X": "value"}

Documentation Contributions
--------------------------

* Documentation uses Sphinx and reStructuredText
* Code examples should be runnable
* Keep documentation in sync with code
* Add appropriate cross-references

Bug Reports
-----------

When reporting bugs, please include:

1. **Environment information**
   - Python version
   - Operating system
   - Dependency versions

2. **Reproduction steps**
   - Detailed step-by-step description
   - Minimal reproducible example

3. **Expected behavior**
   - What you expected to see

4. **Actual behavior**
   - What actually happened
   - Error messages (if any)

Feature Suggestions
------------------

When proposing features, please consider:

1. **Problem description**
   - What problem are you trying to solve

2. **Solution**
   - Your proposed solution
   - Possible implementation approaches

3. **Use cases**
   - Who would use this feature
   - How frequently would it be used

4. **Alternatives**
   - Are there other ways to achieve this

Release Process
--------------

1. **Update version number**
   - Update version number in `pyproject.toml`

2. **Update documentation**
   - Update CHANGELOG
   - Update version references in docs

3. **Create release**
   - Create GitHub release
   - Tag the release

4. **Publish to PyPI**
   - Build and upload to PyPI

Getting Help
-----------

If you need help with contributing:

* Check existing issues and pull requests
* Join our discussions on GitHub
* Ask questions in issues

Thank you for contributing to Siamese Prototype! 