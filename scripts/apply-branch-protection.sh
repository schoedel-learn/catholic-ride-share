#!/bin/bash
# Script to apply branch protection settings to the main branch
# This script uses GitHub CLI (gh) to configure branch protection rules
# 
# Prerequisites:
#   - GitHub CLI installed (https://cli.github.com/)
#   - Authenticated with appropriate permissions (gh auth login)
#   - Repository admin access
#
# Usage:
#   ./scripts/apply-branch-protection.sh

set -e

# Repository details
OWNER="schoedel-learn"
REPO="catholic-ride-share"
BRANCH="main"

echo "Applying branch protection settings to ${OWNER}/${REPO}:${BRANCH}..."

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Please install it from https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    exit 1
fi

# Apply branch protection settings
echo "Configuring branch protection..."

gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/${OWNER}/${REPO}/branches/${BRANCH}/protection" \
  -f required_status_checks='{"strict":true,"contexts":["test"]}' \
  -f enforce_admins=false \
  -f required_pull_request_reviews='{"dismiss_stale_reviews":true,"require_code_owner_reviews":false,"required_approving_review_count":1}' \
  -F allow_force_pushes=false \
  -F allow_deletions=false \
  -F required_linear_history=false \
  -f restrictions=null

echo "✓ Branch protection settings applied successfully!"
echo ""
echo "Main branch is now protected with:"
echo "  - Force pushes disabled"
echo "  - Branch deletion disabled"
echo "  - Required status checks: test"
echo "  - Required approving reviews: 1"
echo "  - Stale review dismissal enabled"
echo ""
echo "View settings at: https://github.com/${OWNER}/${REPO}/settings/branches"
