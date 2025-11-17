# Contributing to Catholic Ride Share

Thank you for your interest in contributing to Catholic Ride Share! This project serves the Catholic community by ensuring transportation is never a barrier to participating in church life.

## Code of Conduct

- Be respectful and charitable in all interactions
- Focus on what is best for the community
- Show empathy towards other contributors
- Accept constructive criticism gracefully

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, etc.)

### Suggesting Features

1. Search existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach

### Code Contributions

1. **Fork the repository**
   ```bash
   git fork https://github.com/yourusername/catholic-ride-share
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Write or update tests
   - Update documentation as needed

4. **Test your changes**
   ```bash
   cd backend
   pytest
   black .
   isort .
   flake8 .
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Describe what changes you made and why
   - Reference any related issues
   - Ensure all tests pass

## Development Setup

See README.md for detailed setup instructions.

Quick start:
```bash
# Clone your fork
git clone https://github.com/yourusername/catholic-ride-share
cd catholic-ride-share

# Set up backend
cd backend
cp .env.example .env
# Edit .env with your settings

# Run with Docker
docker-compose up -d
```

## Code Style Guidelines

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Format with Black (line length 100)
- Sort imports with isort
- Maximum complexity: keep functions focused and small

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Reference issues and PRs when relevant

Example:
```
Add driver verification endpoint

- Implement document upload
- Add verification status tracking
- Create admin review interface

Closes #123
```

## Testing

- Write tests for all new features
- Ensure existing tests pass
- Aim for >80% code coverage
- Include both unit and integration tests

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_auth.py
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all functions and classes
- Update API documentation as needed
- Create or update docs/ files for architecture changes

## Review Process

1. Automated tests must pass
2. Code review by maintainer(s)
3. Changes requested if needed
4. Approval and merge

## Areas for Contribution

### High Priority
- AI matching algorithm improvements
- Safety and moderation features
- Mobile app development (React Native)
- Multi-language support

### Good First Issues
Look for issues tagged with `good first issue` for beginner-friendly tasks.

### Documentation
- Improve setup instructions
- Add API examples
- Create user guides
- Translate documentation

### Testing
- Add test coverage
- Create integration tests
- Performance testing

## Questions?

- Open an issue with the `question` label
- Check existing documentation
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for helping build a tool that serves the Catholic community!
