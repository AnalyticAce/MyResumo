# Copilot Instructions - Best Development Practices

*My Github Username is:* **AnalyticAce**

This guide establishes development standards and best practices for our tech stack: Python, FastAPI, HTML/CSS, Jinja2, Alpine.js, and AI integrations. Following these practices ensures maintainable, sustainable, and high-quality systems.

## General Instructions
- Always prioritize readability and clarity.
- For algorithm-related code, include explanations of the approach used.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.
- If possible use available tools to search libary documentation to write and suggestion updated code.
- Use consistent naming conventions and follow language-specific best practices.
- Write concise, efficient, and idiomatic code that is also easily understandable.

## Python Development

### Code Style & Structure
- Provide docstrings following PEP 257 conventions and use `ruff`
- Structure projects using a clear module hierarchy
- Use the typing module for type annotations (e.g., List[str], Dict[str, int]).
- Create meaningful docstrings (Google style recommended)
- Break down complex functions into smaller, more manageable functions.
- Maintain proper indentation (use 4 spaces for each level of indentation).
- Place function and class docstrings immediately after the `def` or `class` keyword.
- Use blank lines to separate functions, classes, and code blocks where appropriate.

### Python Best Practices
- Prefer explicit code over implicit
- Use virtual environments (`venv`, `poetry`, or `pipenv`)
- Implement comprehensive error handling with specific exception types
- Follow SOLID principles for OOP code
- Leverage dataclasses for data containers
- Use enums for related constants

### Testing and Edge Cases
- Write unit tests with pytest (aim for >80% coverage)
- Implement integration and end-to-end tests
- Use test fixtures for reusable test components
- Mock external dependencies and services
- Practice TDD where applicable
- Always include test cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.
- Include comments for edge cases and the expected behavior in those cases.
- Write unit tests for functions and document them with docstrings explaining the test cases.


## FastAPI Development

### API Design
- Follow RESTful principles
- Use Pydantic models for request/response validation
- Implement proper status codes and error responses
- Version your APIs (path-based preferred: `/api/v1/...`)
- Organize endpoints using APIRouter for logical grouping

### FastAPI Features
- Leverage dependency injection for shared components
- Use background tasks for non-blocking operations
- Implement middleware for cross-cutting concerns
- Utilize FastAPI's built-in OpenAPI documentation
- Set up proper CORS handling

### Performance
- Use async/await for I/O-bound operations
- Implement caching for expensive operations
- Use connection pooling for database access
- Monitor endpoint performance
- Consider pagination for large result sets

## Frontend Development

### HTML Best Practices
- Use semantic HTML5 elements
- Ensure proper accessibility (ARIA attributes, proper heading structure)
- Validate markup with W3C validator
- Implement responsive design principles
- Keep markup clean and minimal

### CSS Structure
- Follow a naming convention (BEM recommended)
- Use CSS custom properties for theming
- Implement mobile-first responsive design
- Minimize specificity conflicts
- Consider utility-first approach for complex UIs

### Jinja2 Templating
- Create a base template with blocks for content sections
- Use macros for reusable components
- Keep logic in templates minimal
- Leverage template inheritance
- Use includes for partial templates
- Handle empty states gracefully

### Alpine.js Implementation
- Use for interactive components that don't require complex state management
- Follow progressive enhancement principles
- Keep Alpine components focused on a single responsibility
- Use x-data for component state
- Prefer declarative templates over imperative code

## AI Engineering

### Model Integration
- Abstract AI services behind clean interfaces
- Implement circuit breakers for external AI services
- Version your prompts and store them separately from code
- Log interactions with AI services for debugging
- Implement fallbacks for AI service failures

### Prompt Engineering
- Create clear, specific prompts with examples
- Use structured outputs when possible (JSON, etc.)
- Implement prompt versioning
- Test prompts with diverse inputs
- Document prompt design decisions

### Responsible AI
- Implement content filtering and safety measures
- Consider bias and fairness in AI implementations
- Provide clear indicators when content is AI-generated
- Implement user feedback mechanisms
- Set up monitoring for AI system outputs

## Version Control & Commit Practices

### Commit Message Structure
- Use a structured format: `<type>(<scope>): <subject>`
- Keep first line under 72 characters
- Add detailed description after subject when needed
- Reference issue numbers where applicable

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvements
- `test`: Adding or modifying tests
- `chore`: Build process or tooling changes
- `ci`: CI configuration changes
- `revert`: Reverting previous changes

### Scope Guidelines
- Use module/component name when applicable (`auth`, `users`, `ui`, etc.)
- Use `*` for changes spanning multiple modules
- Optional but recommended for clarity

### Commit Message Examples
- `feat(auth): implement OAuth2 login flow`
- `fix(api): correct status code for validation errors`
- `docs(readme): update deployment instructions`
- `refactor(models): simplify user schema`
- `test(endpoints): add tests for profile update`

### Commit Content Best Practices
- Make atomic commits (one logical change per commit)
- Separate refactoring commits from feature commits
- Never commit secrets or sensitive data
- Verify changes before committing (run tests)
- Keep commits small and focused

### Smart Commit Messages
- Include details that reflect code modifications:
  - `feat(database): add migration for user preferences table`
  - `fix(validation): handle null values in email validator`
  - `refactor(services): extract authentication logic to dedicated module`
- Reference performance impacts if applicable:
  - `perf(queries): optimize user search by adding index (50% faster)`

### Branch Naming Conventions
- Use prefixes to indicate branch type:
  - `feature/` for new features
  - `bugfix/` for bug fixes
  - `hotfix/` for urgent production fixes
  - `release/` for release preparation
  - `docs/` for documentation updates
- Include issue number when available:
  - `feature/AUTH-123-oauth-integration`
  - `bugfix/CORE-456-fix-memory-leak`
- Use kebab-case for readability

### Pre-Push Review Checklist
- Run all tests before pushing
- Check code style compliance
- Verify commit messages follow conventions
- Review changed files for accidental inclusions
- Ensure all TODOs have associated tickets

### Code Change Analysis for Commits
- For API changes: `feat(api): add endpoint for user preferences [POST /users/{id}/preferences]`
- For UI changes: `feat(ui): implement responsive navigation menu`
- For dependency updates: `chore(deps): update FastAPI to 0.95.0`
- For schema changes: `feat(models): add email verification fields to User model`
- For bug fixes: `fix(auth): prevent token refresh after password change [CVE-2023-1234]`

## DevOps & Deployment

### Containerization
- Use Docker for consistent environments
- Create optimized multi-stage builds
- Minimize container image size
- Follow the principle of one service per container
- Use docker-compose for local development

### CI/CD
- Implement automated testing in CI pipelines
- Use trunk-based development
- Automate deployments with proper staging environments
- Implement infrastructure as code
- Set up monitoring and alerting

### Security
- Store secrets in environment variables or secure vaults
- Implement proper authentication and authorization
- Regularly update dependencies
- Scan for vulnerabilities
- Follow OWASP security guidelines

## Project Management

### Documentation
- Maintain comprehensive README.md files
- Document system architecture and data flows
- Create API documentation (auto-generated + manual)
- Implement change logs
- Use diagrams for complex systems (C4 model recommended)

### Code Review Process
- Establish code review checklist
- Use pull requests for all changes
- Enforce style guidelines through automation
- Focus reviews on logic and architecture
- Provide constructive feedback

### Knowledge Sharing
- Schedule regular knowledge sharing sessions
- Document architectural decisions (ADRs)
- Create onboarding guides for new team members
- Maintain a technical wiki or knowledge base
- Encourage pair programming for complex features

## Monitoring & Maintenance

### Logging
- Implement structured logging
- Use appropriate log levels
- Include contextual information in logs
- Set up centralized log collection
- Implement log rotation

### Observability
- Set up application metrics collection
- Implement distributed tracing
- Create dashboards for key metrics
- Set up alerts for critical issues
- Monitor API performance and errors

### Database Management
- Use migrations for schema changes
- Implement indexes for frequent queries
- Set up database backups
- Monitor database performance
- Use connection pooling

## Conclusion

These practices provide a foundation for building maintainable, sustainable systems using our tech stack. Adapt these guidelines to your specific project needs while maintaining the core principles of clean code, good documentation, and responsible development practices.