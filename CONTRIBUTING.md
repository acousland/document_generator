# Contributing to Document Generator

Thank you for your interest in contributing to the Document Generator project!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/document_generator.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements-dev.txt`

## Development Setup

### Install in Development Mode

```bash
pip install -e .
```

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=document_generator --cov-report=html
```

### Code Style

We use Black for code formatting and Flake8 for linting:

```bash
black document_generator/
flake8 document_generator/
```

## Making Changes

1. Write tests for your changes
2. Make your changes
3. Run tests to ensure everything passes
4. Format your code with Black
5. Commit your changes with a descriptive message
6. Push to your fork
7. Create a Pull Request

## Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Include tests for new functionality
- Update documentation as needed
- Ensure all tests pass
- Follow the existing code style

## Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)

## Feature Requests

We welcome feature requests! Please:

- Check if the feature has already been requested
- Provide a clear use case for the feature
- Describe the expected behavior

## Code of Conduct

Be respectful and inclusive in all interactions. We aim to foster a welcoming community.

## Questions?

Feel free to open an issue for any questions or concerns.

Thank you for contributing!
