# Contributing to AI Emotional Engine for Telugu Story Creation

Thank you for your interest in contributing to the AI Emotional Engine for Telugu Story Creation! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:

1. A clear, descriptive title
2. A detailed description of the issue
3. Steps to reproduce the bug
4. Expected behavior
5. Actual behavior
6. Screenshots (if applicable)
7. Environment information (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for enhancements! Please create an issue with:

1. A clear, descriptive title
2. A detailed description of the proposed enhancement
3. Any relevant examples or mockups
4. Why this enhancement would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python -m pytest tests/`)
6. Commit your changes (`git commit -m "Add amazing feature"`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Pull Request Guidelines

* Follow the coding style of the project
* Include tests for new functionality
* Update documentation as needed
* Keep pull requests focused on a single topic
* Reference any relevant issues in your PR description

## Development Setup

1. Clone the repository
   ```bash
   git clone https://github.com/DIRAKHIL/super-agi-telugu-story-engine.git
   cd super-agi-telugu-story-engine
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up configuration
   ```bash
   cp src/config/default.py src/config/local.py
   # Edit local.py with your specific settings
   ```

5. Run tests to verify setup
   ```bash
   python -m pytest tests/
   ```

## Coding Standards

* Follow PEP 8 style guidelines
* Write docstrings for all functions, classes, and modules
* Maintain test coverage above 90%
* Use type hints where appropriate

## Contribution Areas

We welcome contributions in the following areas:

### Agent Development
* Create new specialized agents
* Improve existing agent implementations
* Enhance agent interaction patterns

### Telugu Language Processing
* Improve Telugu NLP capabilities
* Add support for regional dialects
* Enhance transliteration and translation

### Cultural Adaptation
* Improve cultural authenticity
* Add support for regional variations
* Enhance representation of Telugu traditions

### Testing and Evaluation
* Add new test cases
* Improve evaluation metrics
* Create benchmarks for story quality

### Documentation
* Improve existing documentation
* Add tutorials and examples
* Translate documentation to Telugu

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).