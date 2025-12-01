# CLAUDE.md - AI Assistant Guidelines

This file provides context and guidelines for AI assistants working with this codebase.

## Repository Overview

This is a new repository that is currently being set up. As the codebase evolves, this document should be updated to reflect the current structure and conventions.

**Repository Name:** codex-test
**Status:** New/In Development

## Project Structure

```
codex-test/
├── CLAUDE.md          # AI assistant guidelines (this file)
└── .git/              # Git repository
```

*Note: Update this section as the project structure evolves.*

## Development Workflow

### Getting Started

1. Clone the repository
2. Set up the development environment (add specific instructions as needed)
3. Follow the coding conventions outlined below

### Git Conventions

- **Branch Naming:** Use descriptive branch names
  - Features: `feature/<description>`
  - Bug fixes: `fix/<description>`
  - Documentation: `docs/<description>`
- **Commit Messages:** Write clear, descriptive commit messages
  - Use imperative mood ("Add feature" not "Added feature")
  - Keep the first line under 50 characters
  - Add details in the body if needed
- **Pull Requests:** Provide context and link to related issues

### Code Style

*Add language-specific style guidelines as the project develops.*

General principles:
- Write clear, self-documenting code
- Keep functions focused and small
- Add comments only when the logic isn't self-evident
- Follow existing patterns in the codebase

## Key Commands

*Add commonly used commands as the project develops, such as:*

```bash
# Build (add when applicable)
# npm run build / make / cargo build

# Test (add when applicable)
# npm test / pytest / cargo test

# Lint (add when applicable)
# npm run lint / flake8 / cargo clippy
```

## Architecture Notes

*Document key architectural decisions and patterns here as the project develops.*

## AI Assistant Guidelines

When working with this codebase, AI assistants should:

1. **Read before modifying** - Always read existing code before suggesting changes
2. **Follow existing patterns** - Match the style and conventions already in use
3. **Minimize changes** - Make only the changes necessary to accomplish the task
4. **Avoid over-engineering** - Don't add unnecessary abstractions or features
5. **Test changes** - Run tests and verify changes work before committing
6. **Update documentation** - Keep this CLAUDE.md and other docs up to date

### What to Avoid

- Don't add features beyond what was requested
- Don't refactor unrelated code without explicit request
- Don't introduce new dependencies without justification
- Don't add unnecessary comments or documentation
- Don't create files unless absolutely necessary

## Testing

*Add testing guidelines and commands as the project develops.*

## Dependencies

*List key dependencies and their purposes as they are added.*

## Environment Setup

*Add environment variables and configuration requirements as needed.*

---

*Last updated: 2025-12-01*
*Update this file as the project evolves to keep AI assistants well-informed.*
