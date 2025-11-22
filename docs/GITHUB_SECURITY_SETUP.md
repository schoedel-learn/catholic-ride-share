# GitHub Security Features Setup Guide

This guide explains how to enable and configure GitHub's security features for the Catholic Ride Share repository.

## Prerequisites

- Repository admin access
- GitHub Advanced Security license (for private repositories)
- GitHub Pro, Team, or Enterprise account (for private repo advanced security)

## Enabling Security Features

### 1. Enable Dependency Graph

The dependency graph shows the packages your project depends on and the repositories that depend on it.

**Steps:**
1. Navigate to repository **Settings**
2. Click **Code security and analysis** (left sidebar)
3. Find **Dependency graph** section
4. Click **Enable** button

**Note**: For public repositories, this is enabled by default. For private repositories, you need GitHub Advanced Security.

**Verification:**
- Go to **Insights** tab → **Dependency graph**
- You should see a list of dependencies from `backend/requirements.txt`

### 2. Enable Dependabot Alerts

Dependabot alerts notify you when vulnerabilities are found in your dependencies.

**Steps:**
1. Go to **Settings** → **Code security and analysis**
2. Find **Dependabot alerts** section
3. Click **Enable** button

**Configuration:**
- Alerts are sent to repository admins by default
- Configure notification preferences in your personal settings
- The `.github/dependabot.yml` file is already configured

**Verification:**
- Go to **Security** tab → **Dependabot alerts**
- You should see alert status (hopefully zero alerts!)

### 3. Enable Dependabot Security Updates

Automatically create pull requests to update vulnerable dependencies.

**Steps:**
1. Go to **Settings** → **Code security and analysis**
2. Find **Dependabot security updates** section
3. Click **Enable** button

**What this does:**
- Automatically creates PRs when security vulnerabilities are detected
- PRs include changelog and commit information
- Tests are run automatically via GitHub Actions

**Verification:**
- When a vulnerability is found, a PR will be created automatically
- PRs are labeled with "dependencies" and "security"

### 4. Enable GitHub Advanced Security (Private Repositories)

GitHub Advanced Security provides additional security features for private repositories.

**Requirements:**
- GitHub Enterprise Cloud or GitHub Enterprise Server
- Or GitHub Team with Advanced Security add-on
- Repository must be private

**Steps:**
1. Organization owner must enable GHAS for the organization
2. Go to **Settings** → **Code security and analysis**
3. Find **GitHub Advanced Security** section
4. Click **Enable** button
5. Confirm the action (may impact billing)

**What's included:**
- Code scanning with CodeQL
- Secret scanning
- Dependency review

### 5. Enable Code Scanning (CodeQL)

Code scanning analyzes code to find security vulnerabilities and coding errors.

**Steps:**
1. Go to **Settings** → **Code security and analysis**
2. Find **Code scanning** section
3. Click **Set up** → **Advanced**
4. The `.github/workflows/codeql-analysis.yml` file is already configured
5. CodeQL will run automatically on push and PR

**Alternative Setup:**
1. Go to **Security** tab → **Code scanning**
2. Click **Set up code scanning**
3. Choose **CodeQL Analysis**
4. Select default setup or use the existing workflow

**Verification:**
- Go to **Security** tab → **Code scanning**
- After first workflow run, you'll see scan results
- Any vulnerabilities will be listed with severity ratings

### 6. Enable Secret Scanning

Scans repository for accidentally committed secrets (API keys, tokens, etc.).

**Steps:**
1. Go to **Settings** → **Code security and analysis**
2. Find **Secret scanning** section
3. Click **Enable** button

**For private repositories:**
- Requires GitHub Advanced Security
- Scans all branches and commits

**For public repositories:**
- Enabled by default
- Cannot be disabled

**Verification:**
- Go to **Security** tab → **Secret scanning**
- Ideally shows "No secrets detected"
- If secrets found, revoke and remove them immediately

### 7. Enable Push Protection

Prevents secrets from being pushed to the repository.

**Steps:**
1. Go to **Settings** → **Code security and analysis**
2. Find **Push protection** section (under Secret scanning)
3. Click **Enable** button

**What this does:**
- Blocks pushes containing secrets
- Provides immediate feedback to developers
- Reduces risk of exposing credentials

## Security Configuration Files

This repository includes pre-configured files:

### `.github/dependabot.yml`
Configures Dependabot to:
- Check Python dependencies weekly
- Check Docker images weekly
- Check GitHub Actions weekly
- Group related updates together
- Auto-label PRs with "dependencies" and "security"

### `.github/workflows/codeql-analysis.yml`
Configures CodeQL to:
- Scan on push to main/develop
- Scan on pull requests
- Run weekly scheduled scans
- Use security-extended queries
- Analyze Python code

### `SECURITY.md`
Provides:
- Vulnerability reporting instructions
- Supported versions
- Security best practices
- Compliance information

## Post-Setup Actions

After enabling security features:

### 1. Review Initial Alerts
```bash
# Check for any existing vulnerabilities
- Go to Security tab
- Review Dependabot alerts
- Review CodeQL alerts
- Review Secret scanning alerts
```

### 2. Configure Notifications
```bash
# Personal notification settings
- GitHub Profile → Settings → Notifications
- Configure for: Security alerts, Dependabot, CodeQL
```

### 3. Set Up Team Notifications
```bash
# Organization level
- Organization → Settings → Code security and analysis
- Configure team assignments for security alerts
```

### 4. Establish Security Workflow
- Assign someone to review security alerts weekly
- Create process for responding to vulnerabilities
- Document security incident response plan

## Monitoring and Maintenance

### Weekly Tasks
- [ ] Review new Dependabot alerts
- [ ] Review new CodeQL findings
- [ ] Merge Dependabot security PRs after testing
- [ ] Check secret scanning alerts

### Monthly Tasks
- [ ] Review security policy
- [ ] Audit dependency versions
- [ ] Review access permissions
- [ ] Update security documentation

### Quarterly Tasks
- [ ] Security audit of entire codebase
- [ ] Review and update security practices
- [ ] Team security training
- [ ] Penetration testing (if applicable)

## Troubleshooting

### Dependency Graph Not Showing Dependencies
1. Ensure `requirements.txt` is in correct location
2. Check file format (should be standard pip format)
3. Wait a few minutes for GitHub to parse the file
4. Try pushing a commit to trigger re-parsing

### CodeQL Workflow Failing
1. Check workflow logs in Actions tab
2. Ensure Python dependencies install correctly
3. Verify Python version matches project requirements
4. Check for syntax errors in Python code

### Dependabot PRs Not Created
1. Verify Dependabot is enabled
2. Check `.github/dependabot.yml` syntax
3. Look for error messages in Security → Dependabot
4. Ensure dependency files are in correct locations

### Secret Scanning False Positives
1. Review the detected "secret"
2. If it's not a real secret, you can dismiss the alert
3. Add patterns to `.gitignore` if needed
4. Consider using placeholder values in examples

## Cost Considerations

### Public Repositories
- All security features are **FREE**
- No limits on code scanning
- Unlimited secret scanning

### Private Repositories
- Dependency graph: FREE
- Dependabot alerts: FREE
- Dependabot security updates: FREE
- **GitHub Advanced Security: PAID** (required for):
  - Code scanning (CodeQL)
  - Secret scanning
  - Dependency review

### Billing
- GHAS is billed per active committer
- Check with your organization admin for budget
- Consider making repository public to get free GHAS

## Best Practices

1. **Enable all features**: Don't skip any security features
2. **Act quickly**: Address security alerts within 7 days
3. **Automate updates**: Let Dependabot handle routine updates
4. **Regular audits**: Review security posture monthly
5. **Train team**: Ensure everyone understands security tools
6. **Document process**: Keep security procedures up to date
7. **Test thoroughly**: Don't merge Dependabot PRs without testing
8. **Monitor actively**: Don't ignore security notifications

## Additional Resources

- [GitHub Security Documentation](https://docs.github.com/en/code-security)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Secret Scanning Documentation](https://docs.github.com/en/code-security/secret-scanning)

## Support

If you encounter issues:
1. Check GitHub Status: https://www.githubstatus.com/
2. GitHub Community Forum: https://github.community/
3. Contact GitHub Support (for Enterprise users)
4. Open an issue in this repository (for setup questions)

## Checklist

Use this checklist to ensure all features are enabled:

- [ ] Dependency graph enabled
- [ ] Dependabot alerts enabled
- [ ] Dependabot security updates enabled
- [ ] GitHub Advanced Security enabled (if private repo)
- [ ] Code scanning (CodeQL) enabled
- [ ] Secret scanning enabled
- [ ] Push protection enabled
- [ ] Notifications configured
- [ ] Team members notified of new process
- [ ] Security policy (`SECURITY.md`) reviewed
- [ ] Initial security alerts addressed
- [ ] Weekly review process established
