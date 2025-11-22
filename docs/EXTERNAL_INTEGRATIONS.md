# External Integrations and App Access

This document explains how to enable external applications and services to access this GitHub repository.

## Overview

External tools like BrainGrid, IDEs, AI assistants, and other GitHub Apps need proper configuration to access repository files. This guide helps ensure smooth integration.

## File Access Configuration

### GitHub Copilot Instructions

The repository includes `.github/copilot-instructions.md` which provides context and guidelines to GitHub Copilot. This file:

- Explains the project's tech stack and architecture
- Defines code style standards and best practices
- Provides common patterns and examples
- Helps Copilot generate context-aware code suggestions
- Improves code completion accuracy and relevance

**Location**: `.github/copilot-instructions.md`

GitHub Copilot automatically reads this file to understand project conventions and provide better suggestions.

### .gitattributes File

The repository includes a `.gitattributes` file that helps external tools properly understand file types, encodings, and line endings. This file ensures:

- Consistent line endings across platforms (LF for text files)
- Proper detection of binary vs. text files
- Correct diff and merge behavior for different file types
- Language-specific handling (e.g., Python, SQL, Markdown)

If you're experiencing file access issues with external tools, verify that `.gitattributes` is present in the repository root.

## Enabling GitHub App Access

### For Repository Administrators

To grant access to GitHub Apps like BrainGrid:

1. **Check Your Permissions**
   - You need **Admin** or **Owner** access to install GitHub Apps
   - Organization owners may need to approve app installations

2. **Install the GitHub App**
   - Go to repository **Settings** → **Integrations** → **GitHub Apps**
   - Or visit the app's installation page (e.g., https://github.com/apps/braingrid)
   - Click **Install** or **Configure**

3. **Grant Repository Access**
   - Choose specific repositories or "All repositories"
   - Review and approve the requested permissions:
     - **Read** access to code and metadata
     - **Write** access to issues and pull requests (if needed)
     - **Read** access to workflows (if needed)

4. **Verify Installation**
   - Check Settings → Integrations → Installed GitHub Apps
   - Confirm the app appears with access to your repository

### Required Permissions for Common Apps

Different apps require different permission levels:

| App Type | Typical Permissions Needed |
|----------|---------------------------|
| BrainGrid | Read: code, metadata; Write: issues, PRs |
| Code Analysis | Read: code, metadata |
| CI/CD Tools | Read: code; Write: checks, deployments |
| Project Management | Read: code; Write: issues, PRs, projects |

## Troubleshooting Access Issues

### "Resource not accessible by integration"

This error typically occurs when:

1. **Insufficient Permissions**: The app doesn't have required access levels
   - Solution: Reinstall the app with correct permissions

2. **Token Scope Issues**: For GitHub Actions or API access
   - Solution: Update workflow permissions in `.github/workflows/*.yml`
   ```yaml
   permissions:
     contents: read
     issues: write
     pull-requests: write
   ```

3. **Organization Restrictions**: Org settings block app installation
   - Solution: Contact organization admin to approve the app

### File Access Problems

If external tools can't read specific files:

1. **Check File Encoding**
   - Ensure files use UTF-8 encoding
   - Verify `.gitattributes` properly declares file types

2. **Binary File Handling**
   - Confirm binary files are marked as `binary` in `.gitattributes`
   - Some tools can't read binary files directly

3. **Large File Issues**
   - GitHub has file size limits (100MB default)
   - Use Git LFS for large files

4. **Branch Protection**
   - Some apps may be blocked by branch protection rules
   - Review Settings → Branches → Branch protection rules

### Testing File Accessibility

To verify files are accessible to external tools:

```bash
# Check if .gitattributes is applied
git check-attr -a <filename>

# Verify file is tracked and not ignored
git ls-files <filename>

# Check file encoding
file <filename>
```

## Best Practices

1. **Use .gitattributes**: Always include this file for consistency
2. **Minimal Permissions**: Grant only necessary app permissions
3. **Regular Audits**: Periodically review installed apps and their access
4. **Documentation**: Document any custom integration requirements
5. **Testing**: Test integrations in feature branches before main

## Security Considerations

- **Review App Permissions**: Carefully check what access each app requests
- **Revoke Unused Apps**: Remove integrations you no longer use
- **Monitor Activity**: Check app activity in repository audit logs
- **Sensitive Data**: Never commit secrets or credentials
- **Private Repositories**: Be extra cautious with private repo access

## Common External Tools

### Development Tools

#### GitHub Copilot
GitHub Copilot is an AI pair programmer that helps write code faster.

**Setup**:
1. Install GitHub Copilot extension in VS Code or JetBrains IDE
2. Sign in with your GitHub account (requires Copilot subscription)
3. Trust the workspace when prompted
4. Copilot automatically reads `.github/copilot-instructions.md` for context

**Features**:
- Code completion and suggestions
- Inline code explanations
- Generate entire functions from comments
- Context-aware based on `.github/copilot-instructions.md`

**Best Practices**:
- Review all suggestions before accepting
- Use descriptive comments to get better suggestions
- Keep `.github/copilot-instructions.md` updated with project conventions

#### Other Tools
- **JetBrains IDEs**: Configure GitHub integration in Settings
- **BrainGrid**: Requires GitHub App installation with repo access

### CI/CD
- **GitHub Actions**: Uses built-in GITHUB_TOKEN with workflow permissions
- **CircleCI**: Add repository in CircleCI dashboard
- **Travis CI**: Enable repository in Travis settings

### Project Management
- **ZenHub**: Install browser extension and GitHub App
- **Linear**: Connect via GitHub integration settings
- **Jira**: Install Jira GitHub integration

## Getting Help

If you continue to experience access issues:

1. Check the specific tool's documentation
2. Review GitHub's [Troubleshooting guide](https://docs.github.com/en/apps)
3. Open an issue in this repository describing:
   - The external tool you're trying to use
   - Specific error messages
   - Steps you've already tried
   - Your permission level on the repository

## References

- [GitHub Apps Documentation](https://docs.github.com/en/apps)
- [Managing access to GitHub Apps](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/managing-access-to-your-organizations-repositories)
- [Git Attributes Documentation](https://git-scm.com/docs/gitattributes)
- [Repository Permissions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository)
