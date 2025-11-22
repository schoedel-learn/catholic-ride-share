# Security Policy

## Overview

Catholic Ride Share is committed to ensuring the security and privacy of our users, especially given our mission to serve the Catholic community. We take security vulnerabilities seriously and appreciate your efforts to responsibly disclose your findings.

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

As the project is in active development, we recommend always using the latest version from the main branch.

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please follow these steps:

### 1. Private Disclosure

Send an email to the repository maintainers with:
- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (if applicable)

### 2. Response Timeline

- **Initial Response**: We aim to acknowledge receipt within 48 hours
- **Status Updates**: We will provide updates on our progress within 7 days
- **Resolution**: We aim to resolve critical vulnerabilities within 30 days

### 3. Coordinated Disclosure

- We request that you do not publicly disclose the vulnerability until we have had a chance to address it
- Once fixed, we will coordinate with you on the timing of public disclosure
- We are happy to credit you for the discovery (unless you prefer to remain anonymous)

## Security Best Practices for Contributors

### Code Security

1. **Never commit secrets**: API keys, passwords, tokens, or any sensitive data
2. **Use environment variables**: All secrets must be stored in `.env` files (which are gitignored)
3. **Input validation**: Always validate and sanitize user inputs
4. **SQL injection prevention**: Use SQLAlchemy ORM properly, avoid raw SQL queries
5. **XSS prevention**: Sanitize all user-generated content before display
6. **Authentication**: Implement proper JWT token validation and expiration
7. **Password security**: Always hash passwords using bcrypt (never store plaintext)

### Dependencies

1. **Keep dependencies updated**: Regularly update to patch known vulnerabilities
2. **Review new dependencies**: Vet third-party packages before adding them
3. **Use Dependabot**: We use automated dependency updates to stay current
4. **Monitor security advisories**: Check GitHub Security Advisories regularly

### Data Protection

1. **User privacy**: Minimize data collection to only what is necessary
2. **Data encryption**: Use TLS/SSL for all data in transit
3. **Database security**: Encrypt sensitive data at rest
4. **Access control**: Implement proper authorization checks
5. **Audit logging**: Log security-relevant events

### API Security

1. **Rate limiting**: Implement rate limits to prevent abuse
2. **CORS configuration**: Properly configure allowed origins
3. **Authentication**: Require authentication for sensitive endpoints
4. **Error messages**: Avoid exposing sensitive information in error messages

## Security Features

### Implemented

- ✅ JWT-based authentication with access and refresh tokens
- ✅ Bcrypt password hashing
- ✅ Email verification for new accounts
- ✅ Secure password reset flow with single-use tokens
- ✅ Input validation using Pydantic
- ✅ SQL injection protection via SQLAlchemy ORM
- ✅ CORS configuration
- ✅ Environment variable management
- ✅ Secure file upload handling with size limits

### Planned

- 🔄 Rate limiting on authentication endpoints
- 🔄 Two-factor authentication (2FA)
- 🔄 Driver background checks via Checkr API
- 🔄 IP-based security monitoring
- 🔄 Automated security scanning in CI/CD
- 🔄 CSP (Content Security Policy) headers
- 🔄 Advanced audit logging

## Known Security Considerations

### Email Enumeration Protection

Our authentication endpoints are designed to prevent email enumeration attacks:
- Forgot password always returns success (doesn't reveal if email exists)
- Registration errors are generic when possible
- Rate limiting prevents brute force attempts

### Geolocation Privacy

- User locations are optional and only stored as approximate coordinates
- Exact addresses are only shared between matched riders and drivers
- Location data is never publicly exposed

### Payment Security

- We use Stripe for payment processing (PCI DSS compliant)
- We never store credit card information
- All payment data is handled by Stripe's secure infrastructure

## Compliance

This project follows security best practices including:

- **OWASP Top 10**: Mitigation strategies for common web vulnerabilities
- **CWE/SANS Top 25**: Addressing most dangerous software weaknesses
- **GDPR considerations**: Privacy-first design (though full compliance depends on deployment)
- **Non-profit best practices**: Appropriate security for community-driven projects

## Security Tools

We use the following tools to maintain security:

- **Dependabot**: Automated dependency updates
- **CodeQL**: Code scanning for vulnerabilities
- **pytest**: Comprehensive test coverage including security tests
- **GitHub Secret Scanning**: Automatic detection of committed secrets
- **Pre-commit hooks**: Local validation before commits (recommended)

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Questions?

If you have questions about security practices in this project, please open a GitHub issue with the "security" label or contact the maintainers directly.

---

Thank you for helping keep Catholic Ride Share and our community safe!
