# Repository Settings and Branch Protection

This document describes the repository settings and branch protection rules for the Catholic Ride Share project.

## Overview

The repository uses branch protection rules to ensure code quality, prevent accidental changes, and maintain a stable main branch.

## Branch Protection Rules

### Main Branch (`main`)

The `main` branch is the production branch and is protected with the following rules:

#### Protection Settings

1. **Prevent Force Pushes**
   - Force pushes to `main` are disabled
   - This preserves commit history and prevents accidental overwrites
   - Developers must use proper Git workflows (revert, merge, etc.)

2. **Prevent Branch Deletion**
   - The `main` branch cannot be deleted
   - This protects the primary branch from accidental removal

3. **Require Status Checks Before Merging**
   - All CI/CD tests must pass before code can be merged
   - Required checks include:
     - **test**: Backend and frontend test suite (Python + npm tests)
   - Status checks must be up-to-date with the base branch (strict mode)

4. **Require Pull Request Reviews**
   - At least 1 approving review is required before merging
   - Reviews are automatically dismissed when new commits are pushed
   - This ensures code review happens for all changes

5. **Administrator Enforcement**
   - Administrators can bypass these rules in emergency situations
   - However, following the rules is strongly recommended even for admins

## Configuration File

Branch protection settings are documented in `.github/settings.yml`. This file can be used with GitHub Apps like:

- **Probot Settings**: Automatically syncs repository settings from the YAML file
- **Terraform GitHub Provider**: Infrastructure-as-code for GitHub settings
- **GitHub CLI**: Manual application of settings

## How to Apply Settings

### Using Probot Settings App

1. Install the [Probot Settings App](https://probot.github.io/apps/settings/) on your repository
2. The app will automatically apply settings from `.github/settings.yml`
3. Any updates to the file will be applied automatically

### Using GitHub CLI

A helper script is provided to apply branch protection settings automatically:

```bash
# Run the script from the repository root
./scripts/apply-branch-protection.sh
```

Or manually using GitHub CLI:

```bash
# Enable branch protection with required checks
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["test"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null
```

### Manual Configuration

1. Go to repository **Settings** → **Branches**
2. Add branch protection rule for `main`
3. Enable the following options:
   - ✅ Require a pull request before merging
     - ✅ Require approvals (1)
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require status checks to pass before merging
     - ✅ Require branches to be up to date before merging
     - Add required check: `test`
   - ✅ Do not allow bypassing the above settings (optional)
   - ✅ Restrict who can push to matching branches (optional)
   - ✅ Do not allow force pushes
   - ✅ Do not allow deletions

## Workflow Requirements

### For Contributors

1. **Always work in a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Push your branch and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Ensure all tests pass**
   - CI will automatically run tests
   - Fix any failures before requesting review

4. **Request review from maintainers**
   - At least one approval is required
   - Address any feedback or requested changes

5. **Keep your branch up to date**
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-feature-name
   git merge main
   ```

### For Maintainers

1. **Review pull requests thoroughly**
   - Check code quality and adherence to style guidelines
   - Verify tests are passing
   - Ensure documentation is updated

2. **Merge using appropriate strategy**
   - Squash and merge: For small features (keeps history clean)
   - Merge commit: For larger features (preserves individual commits)
   - Rebase and merge: For linear history (use carefully)

3. **Never force push to main**
   - Use `git revert` to undo changes
   - Create fix commits rather than rewriting history

## Emergency Procedures

In rare cases where branch protection needs to be bypassed:

1. **Assess the emergency**
   - Is this truly an emergency that can't wait for normal process?
   - Could waiting cause significant harm or downtime?

2. **Document the bypass**
   - Create an issue documenting why normal process was bypassed
   - Include what was changed and why
   - Tag as `emergency` or `hotfix`

3. **Follow up with proper PR**
   - Create a retroactive PR showing the changes
   - Get review and approval post-facto
   - Document lessons learned

## CI/CD Integration

The branch protection rules integrate with GitHub Actions workflows:

- **test.yml**: Runs on all pushes and pull requests
  - Backend tests (pytest)
  - Frontend tests (npm test)
  - Linting (black, isort, flake8, eslint)
  
- **deploy.yml**: Runs on pushes to main
  - Builds Docker images
  - Deploys to production VPS

Status checks from these workflows are required before merging to `main`.

## Benefits

Branch protection provides several benefits:

1. **Code Quality**: Ensures all code is reviewed and tested
2. **Stability**: Prevents breaking changes from reaching production
3. **Collaboration**: Encourages discussion and knowledge sharing
4. **Audit Trail**: Maintains clear history of all changes
5. **Security**: Prevents unauthorized or accidental changes

## Troubleshooting

### "Required status check is failing"
- Check the CI logs for specific failures
- Fix the issues in your branch
- Push the fixes and wait for CI to re-run

### "Pull request is out of date"
- Merge the latest `main` into your branch
- Resolve any conflicts
- Push the updated branch

### "Need approval before merging"
- Request review from project maintainers
- Address any requested changes
- Wait for approval

## Related Documentation

- [CONTRIBUTING.md](../CONTRIBUTING.md): Contributing guidelines
- [.github/workflows/test.yml](workflows/test.yml): CI test workflow
- [.github/workflows/deploy.yml](workflows/deploy.yml): Deployment workflow

## Questions?

If you have questions about branch protection or repository settings, please:
- Open an issue with the `question` label
- Contact project maintainers
- Check GitHub's [branch protection documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
