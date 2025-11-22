# Branch Protection Rules Configuration

This document provides step-by-step instructions for setting up branch protection rules for the Catholic Ride Share repository. These settings help ensure code quality, security, and proper review processes.

## Why Branch Protection Matters

Branch protection rules are essential for:
- **Code Quality**: Ensuring all changes are reviewed before merging
- **Security**: Preventing unauthorized or untested code from reaching production
- **Collaboration**: Maintaining a clean and stable codebase
- **Non-profit Standards**: Meeting governance requirements for community-driven projects

## Recommended Settings for Main Branch

### Prerequisites

- You must have admin access to the repository
- Navigate to: `Settings` → `Branches` → `Branch protection rules` → `Add rule`

### Configuration Steps

#### 1. Branch Name Pattern

```
main
```

#### 2. Protection Settings

**Protect matching branches**

Enable the following rules:

##### Required Pull Request Reviews
- ✅ **Require a pull request before merging**
  - ✅ **Require approvals**: `1` (at least one approval)
  - ✅ **Dismiss stale pull request approvals when new commits are pushed**
  - ✅ **Require review from Code Owners** (if you have multiple maintainers)
  - ⬜ **Require approval of the most recent reviewable push**
  
##### Status Checks
- ✅ **Require status checks to pass before merging**
  - ✅ **Require branches to be up to date before merging**
  - Select required status checks:
    - `test` (from test.yml workflow)
    - `analyze` (from codeql.yml workflow, once it runs)

##### Additional Settings
- ✅ **Require conversation resolution before merging**
- ✅ **Require signed commits** (recommended but optional)
- ✅ **Require linear history** (keeps git history clean)
- ✅ **Require deployments to succeed before merging** (if using deployment environments)

##### Rules Applied to Everyone
- ✅ **Include administrators** (admins must follow the same rules)
- ⬜ **Allow force pushes** (should be DISABLED)
- ⬜ **Allow deletions** (should be DISABLED)

#### 3. Optional Advanced Settings

**Restrict who can push to matching branches**
- Only enable if you have multiple teams
- Add specific users or teams who can push directly

**Restrict who can dismiss pull request reviews**
- Recommended: Only repository admins

**Lock branch**
- Not recommended for main development branch
- Consider for release branches only

## Recommended Settings for Develop Branch

If using a `develop` branch for active development:

#### Branch Name Pattern
```
develop
```

#### Protection Settings
- ✅ **Require a pull request before merging**
  - Require approvals: `1`
- ✅ **Require status checks to pass before merging**
  - `test` workflow must pass
- ✅ **Require conversation resolution before merging**
- ⬜ **Require linear history** (optional for develop)
- ⬜ **Include administrators** (optional - allows admins to push hotfixes)

## Recommended Settings for Release Branches

For branches matching pattern `release/*`:

#### Branch Name Pattern
```
release/*
```

#### Protection Settings
- ✅ **Require a pull request before merging**
  - Require approvals: `2` (higher for releases)
  - ✅ **Dismiss stale pull request approvals when new commits are pushed**
- ✅ **Require status checks to pass before merging**
- ✅ **Require conversation resolution before merging**
- ✅ **Lock branch** (after release is finalized)
- ✅ **Include administrators**

## Tag Protection Rules

To protect release tags from unauthorized deletion or modification:

1. Navigate to: `Settings` → `Tags` → `Protected tags` → `Add rule`
2. Pattern: `v*` (protects all version tags like v1.0.0)
3. ✅ **Restrict who can create and delete matching tags**
   - Select: Repository admins only

## Verifying Protection Rules

After setting up, verify the rules are working:

1. Try to push directly to main (should fail):
   ```bash
   git checkout main
   git commit --allow-empty -m "Test direct push"
   git push origin main
   # Should be rejected
   ```

2. Create a PR and verify:
   - Status checks are required
   - At least one approval is needed
   - Cannot merge until checks pass

3. Check branch protection status:
   - Repository home page should show a shield icon on protected branches
   - Branch selector shows protected branches with a badge

## Additional Security Settings

### 1. Enable Secret Scanning

1. Go to: `Settings` → `Security` → `Code security and analysis`
2. Enable:
   - ✅ **Dependency graph** (should be enabled by default)
   - ✅ **Dependabot alerts**
   - ✅ **Dependabot security updates**
   - ✅ **Secret scanning** (available for public repos)
   - ✅ **Push protection** (prevents committing secrets)

### 2. Enable Code Scanning

1. Go to: `Settings` → `Security` → `Code security and analysis`
2. Enable:
   - ✅ **Code scanning** → **Set up** → Use the CodeQL workflow
   - Note: We've already added `.github/workflows/codeql.yml`

### 3. Enable Private Vulnerability Reporting

1. Go to: `Settings` → `Security` → `Code security and analysis`
2. Enable:
   - ✅ **Private vulnerability reporting**
   - This allows security researchers to privately report vulnerabilities

### 4. Security Policy

We've already added `SECURITY.md` which will appear in the Security tab.

## Notifications

Configure notifications for security alerts:

1. Go to: `Settings` → `Notifications`
2. Enable email notifications for:
   - Dependabot alerts
   - Code scanning alerts
   - Secret scanning alerts

## Team Access (If Multiple Maintainers)

If you add more maintainers:

1. Go to: `Settings` → `Collaborators and teams`
2. Add collaborators with appropriate roles:
   - **Admin**: Full access (use sparingly)
   - **Maintain**: Manage repository settings without sensitive access
   - **Write**: Push to non-protected branches, create PRs
   - **Triage**: Manage issues and PRs
   - **Read**: Clone and view repository

## Enforcement Timeline

After implementing these rules:

- **Week 1**: Monitor for issues, adjust if needed
- **Week 2**: Ensure all contributors understand the workflow
- **Month 1**: Review and optimize based on team feedback
- **Ongoing**: Audit quarterly and update as needed

## Emergency Procedures

In case of critical hotfixes:

1. **Don't disable protection rules**
2. Instead:
   - Create an emergency branch
   - Fast-track the PR review
   - Use admin override if absolutely necessary (log the decision)
   - Document the incident

## Troubleshooting

### "Required status check is not passing"
- Ensure CI/CD workflows are running
- Check workflow logs for errors
- Verify test.yml and codeql.yml are configured correctly

### "Cannot push to protected branch"
- Create a feature branch instead
- Open a pull request
- Request review from a maintainer

### "Need admin to change protection rules"
- Only repository admins can modify these settings
- Contact @schoedel-learn if you need changes

## References

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security/getting-started/securing-your-repository)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## Questions?

If you have questions about branch protection rules, please:
1. Review this document thoroughly
2. Check GitHub's official documentation
3. Open an issue with the `question` label
4. Contact repository maintainers

---

**Note**: These settings must be configured through the GitHub web interface - they cannot be set via code or API without special permissions. This document serves as the reference for proper configuration.
