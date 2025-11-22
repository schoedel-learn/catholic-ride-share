# Repository Security Settings Guide

This document provides comprehensive guidance for configuring security settings for the Catholic Ride Share repository. These settings are essential for maintaining a secure, well-organized repository suitable for a non-profit organization.

## Table of Contents

1. [Branch Protection Rules](#branch-protection-rules)
2. [Security Features](#security-features)
3. [Collaborator Access](#collaborator-access)
4. [Repository Settings](#repository-settings)
5. [Actions and Workflows](#actions-and-workflows)
6. [Webhooks and Integrations](#webhooks-and-integrations)
7. [Automated Security Tools](#automated-security-tools)
8. [Compliance and Best Practices](#compliance-and-best-practices)

---

## Branch Protection Rules

Detailed branch protection setup is covered in [BRANCH_PROTECTION_SETUP.md](BRANCH_PROTECTION_SETUP.md).

### Quick Setup Summary

**Main Branch Protection (Required):**
```
Branch name pattern: main
☑ Require pull request before merging (1 approval)
☑ Require status checks to pass
☑ Require conversation resolution
☑ Require linear history
☑ Include administrators
☐ Allow force pushes (DISABLED)
☐ Allow deletions (DISABLED)
```

**Status Checks Required:**
- `test` (from .github/workflows/test.yml)
- `analyze` (from .github/workflows/codeql.yml)

---

## Security Features

### Enable All Security Features

Navigate to: `Settings` → `Security` → `Code security and analysis`

#### Must Enable (Critical):

1. **Dependency Graph** ✅
   - Automatically enabled for public repositories
   - Tracks all dependencies

2. **Dependabot Alerts** ✅
   - Alerts for vulnerable dependencies
   - Configuration: `.github/dependabot.yml` (already added)

3. **Dependabot Security Updates** ✅
   - Automatic PRs to fix vulnerable dependencies
   - Weekly schedule configured

4. **Secret Scanning** ✅
   - Detects accidentally committed secrets
   - Available for public repositories
   - Push protection prevents new secrets

5. **Push Protection** ✅
   - Blocks commits containing secrets
   - **Critical: Enable this immediately**

6. **Code Scanning (CodeQL)** ✅
   - Analyzes code for security vulnerabilities
   - Configuration: `.github/workflows/codeql.yml` (already added)
   - Runs on: push to main/develop, PRs, weekly schedule

7. **Private Vulnerability Reporting** ✅
   - Allows security researchers to report issues privately
   - Better than public issues for security bugs

#### Recommended Scanning Tools:

- **CodeQL**: Default, comprehensive security analysis
- **Semgrep**: Additional static analysis (optional)
- **Snyk**: Dependency and container scanning (optional)

---

## Collaborator Access

### Access Levels

Configure at: `Settings` → `Access` → `Collaborators and teams`

#### Roles and Permissions:

1. **Admin** (Highest - Use Sparingly)
   - Full repository access
   - Can modify settings, add/remove collaborators
   - Can delete repository
   - **Recommended:** Only 1-2 trusted maintainers

2. **Maintain**
   - Manage repository without sensitive access
   - Cannot modify security settings
   - Good for senior contributors

3. **Write**
   - Push to non-protected branches
   - Create and merge pull requests (with approval)
   - **Recommended:** For active contributors

4. **Triage**
   - Manage issues and pull requests
   - Good for community moderators
   - Cannot push code

5. **Read**
   - Clone and view repository
   - Public repositories have this by default

### Current Structure (Recommended):

```
Owner/Admin: @schoedel-learn
Write: Trusted contributors (add as needed)
Triage: Community moderators (future)
```

### Adding Collaborators:

1. Vet contributors before granting write access
2. Start with triage/read for new contributors
3. Promote based on contribution quality and trust
4. Review access quarterly

---

## Repository Settings

### General Settings

Navigate to: `Settings` → `General`

#### Repository Features:

**Enable:**
- ✅ Issues (bug reports, features)
- ✅ Projects (for roadmap tracking)
- ✅ Discussions (community Q&A)
- ✅ Wiki (for extended documentation)

**Disable:**
- ⬜ Allow merge commits (force PR workflow)
- ✅ Allow squash merging (keeps history clean)
- ✅ Allow rebase merging (alternative to squash)
- ⬜ Always suggest updating pull request branches
- ✅ Automatically delete head branches

#### Pull Requests:

```
☑ Allow squash merging
  ☑ Default to pull request title for squash merge commits
☑ Allow rebase merging
☐ Allow merge commits
☑ Automatically delete head branches
```

#### Merge Button:

```
☐ Allow merge commits
☑ Allow squash merging (Recommended)
☑ Allow rebase merging
```

### Danger Zone Settings:

**DO NOT:**
- ⬜ Make repository private (unless necessary)
- ⬜ Transfer ownership (without careful consideration)
- ⬜ Archive repository (only when truly deprecated)
- ⬜ Delete repository (permanent action)

---

## Actions and Workflows

### Workflow Permissions

Navigate to: `Settings` → `Actions` → `General`

#### Recommended Settings:

```
Actions permissions:
☑ Allow all actions and reusable workflows

Workflow permissions:
☑ Read repository contents and packages permissions (Recommended)
☐ Read and write permissions

☑ Allow GitHub Actions to create and approve pull requests
```

#### Why These Settings:

- **Read-only by default**: Prevents workflows from accidentally modifying code
- **Explicit permissions**: Workflows must declare what they need
- **Security**: Limits potential damage from compromised workflows

#### Fork Pull Request Workflows:

```
☑ Require approval for first-time contributors
☐ Require approval for all outside collaborators
```

### Workflow Files in Repository:

1. `.github/workflows/test.yml` - Runs tests on PRs ✅
2. `.github/workflows/codeql.yml` - Security scanning ✅

### Future Workflows (To Add):

- Linting (black, flake8, isort)
- Type checking (mypy)
- Coverage reporting
- Docker image scanning
- Deployment workflows

---

## Webhooks and Integrations

### Recommended Integrations:

1. **Codecov** (Code Coverage)
   - Add webhook for coverage reports
   - Shows test coverage trends

2. **Slack/Discord** (Notifications)
   - Notify team of PRs, releases, security alerts
   - Configure webhook for your communication platform

3. **Linear/Jira** (Project Management) - Optional
   - Link issues to project management tools

### Security Considerations:

- Review all webhook URLs before adding
- Use HTTPS only
- Rotate webhook secrets regularly
- Monitor webhook delivery logs
- Remove unused integrations

---

## Automated Security Tools

### GitHub Native Tools (Already Configured):

1. **Dependabot** ✅
   - Configuration: `.github/dependabot.yml`
   - Checks: pip, Docker, GitHub Actions
   - Schedule: Weekly on Mondays

2. **CodeQL** ✅
   - Configuration: `.github/workflows/codeql.yml`
   - Languages: Python
   - Schedule: Weekly on Mondays

3. **Secret Scanning** ✅
   - Enabled in repository settings
   - Push protection active

### Additional Tools to Consider:

1. **SAST (Static Application Security Testing)**
   - Semgrep (open source)
   - SonarQube (code quality + security)
   - Bandit (Python security linter)

2. **Dependency Scanning**
   - Snyk (comprehensive)
   - Safety (Python-specific)
   - pip-audit (Python package auditing)

3. **Container Scanning**
   - Trivy (comprehensive)
   - Grype (Anchore)
   - Docker Scout

4. **Infrastructure as Code Scanning**
   - Checkov (Terraform, Kubernetes)
   - tfsec (Terraform)
   - Not immediately needed but future consideration

### Implementation Priority:

1. ✅ Dependabot (Done)
2. ✅ CodeQL (Done)
3. ✅ Secret Scanning (Enable in settings)
4. 🔄 Bandit/Safety (Add to CI pipeline)
5. 🔄 Trivy (For Docker images)
6. 📋 SonarQube (When team grows)

---

## Compliance and Best Practices

### For Non-Profit Organizations:

1. **Transparency**
   - Public repository (already public)
   - Clear SECURITY.md and CONTRIBUTING.md ✅
   - Open issue tracking

2. **Governance**
   - CODEOWNERS file ✅
   - Clear contribution guidelines ✅
   - Code review requirements

3. **Data Protection**
   - No sensitive data in repository
   - Environment variables for secrets
   - User data privacy in application

4. **Licensing**
   - Clear LICENSE file ✅
   - Update if needed for non-profit use

### Security Certifications (Future):

As the project grows, consider:
- SOC 2 Type II (if handling significant user data)
- ISO 27001 (information security management)
- GDPR compliance (if serving EU users)
- HIPAA compliance (if handling health data - unlikely)

### Regular Security Audits:

**Monthly:**
- Review open security alerts
- Check for outdated dependencies
- Review access logs

**Quarterly:**
- Full security audit
- Review collaborator access
- Update security documentation
- Test incident response procedures

**Annually:**
- Third-party security assessment
- Update security policies
- Review and update branch protection rules
- Train contributors on security best practices

---

## Implementation Checklist

Use this checklist to ensure all security settings are configured:

### Immediate Actions (Week 1):

- [x] Create SECURITY.md
- [x] Create CODEOWNERS file
- [x] Add Dependabot configuration
- [x] Add CodeQL workflow
- [x] Create PR and issue templates
- [x] Update .gitignore for secrets
- [ ] **Enable branch protection on main** (Requires admin access)
- [ ] **Enable secret scanning push protection** (Requires admin access)
- [ ] **Enable private vulnerability reporting** (Requires admin access)

### Short-term Actions (Month 1):

- [ ] Add linting to CI pipeline
- [ ] Set up code coverage reporting
- [ ] Configure webhooks for notifications
- [ ] Review and update collaborator access
- [ ] Add Docker image scanning
- [ ] Create deployment workflow (when ready)

### Medium-term Actions (Quarter 1):

- [ ] Implement automated security testing
- [ ] Set up staging environment
- [ ] Configure monitoring and alerting
- [ ] Document incident response procedures
- [ ] Conduct first security audit

### Long-term Actions (Year 1):

- [ ] Consider external security assessment
- [ ] Evaluate additional compliance needs
- [ ] Establish security training program
- [ ] Create security metrics dashboard
- [ ] Review and update all security policies

---

## Monitoring and Maintenance

### Daily Monitoring:

- Automated via GitHub notifications
- Review Dependabot PRs
- Check for security alerts

### Weekly Tasks:

- Review open PRs for security issues
- Check CodeQL scan results
- Update dependencies if needed

### Monthly Tasks:

- Review access logs
- Audit collaborator permissions
- Check for configuration drift
- Update documentation

### Quarterly Tasks:

- Full security review
- Update security policies
- Test backup and recovery
- Review incident logs

---

## Emergency Procedures

### Security Incident Response:

1. **Identify**: Detect and confirm the security issue
2. **Contain**: Immediately revoke compromised credentials
3. **Eradicate**: Remove the vulnerability
4. **Recover**: Restore normal operations
5. **Lessons Learned**: Document and improve

### Emergency Contacts:

- Repository Owner: @schoedel-learn
- Backup: [To be assigned]
- GitHub Support: https://support.github.com

### Breach Notification:

If sensitive data is exposed:
1. Assess scope and impact
2. Notify affected users (if applicable)
3. Report to relevant authorities
4. Document incident thoroughly

---

## Resources and References

### GitHub Documentation:

- [Securing Your Repository](https://docs.github.com/en/code-security/getting-started/securing-your-repository)
- [About Protected Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Code Scanning](https://docs.github.com/en/code-security/code-scanning)

### Security Best Practices:

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Non-Profit Resources:

- [GitHub for Good](https://github.com/github-for-good)
- [TechSoup](https://www.techsoup.org/)
- [NTEN (Non-profit Technology Network)](https://www.nten.org/)

---

## Questions and Support

If you have questions about repository security:

1. Review this documentation
2. Check GitHub's official docs
3. Open an issue with the `security` or `question` label
4. Contact repository maintainers

For urgent security matters, follow the process in [SECURITY.md](../SECURITY.md).

---

**Last Updated**: 2025-11-22  
**Next Review**: 2026-02-22 (Quarterly)

*This document should be reviewed and updated quarterly or after any significant security changes.*
