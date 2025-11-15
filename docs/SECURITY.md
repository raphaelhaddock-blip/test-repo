# Security Policy

## Overview

This document outlines our security practices, vulnerability reporting, and access control policies.

## 🔒 Security Measures

### 1. Automated Security Scanning

We run multiple security scans automatically:

#### Dependency Scanning
- **Tool**: Safety (Python)
- **Frequency**: Every push + weekly
- **Purpose**: Detect vulnerable dependencies
- **Action**: Auto-creates issues for CVEs

#### Code Analysis
- **Tool**: Bandit
- **Frequency**: Every push
- **Purpose**: Detect security issues in code
- **Checks**: SQL injection, XSS, hardcoded secrets

#### Secret Detection
- **Tool**: TruffleHog
- **Frequency**: Every push
- **Purpose**: Prevent committed secrets
- **Scans**: API keys, passwords, tokens

#### Advanced Analysis
- **Tool**: GitHub CodeQL
- **Frequency**: Weekly + on PR
- **Purpose**: Deep semantic analysis
- **Coverage**: 100+ security patterns

### 2. Branch Protection Rules

#### Main Branch Protection

**Required:**
- ✅ Pull request before merging
- ✅ At least 1 approval
- ✅ All status checks must pass
- ✅ Branch must be up to date
- ✅ No force pushes
- ✅ No deletions

**Optional (Recommended):**
- Code owner review
- Signed commits
- Linear history

**To Enable:**
1. Go to Settings → Branches
2. Add rule for `main`
3. Check all required options
4. Save

#### Develop Branch Protection

**Required:**
- ✅ Pull request before merging
- ✅ Status checks must pass

### 3. Access Control

#### Team Roles

**Admin**
- Full repository access
- Manage settings
- Manage team members
- **Who**: Repository owners only

**Maintainer**
- Merge pull requests
- Manage issues/projects
- Cannot change settings
- **Who**: Senior developers

**Write**
- Create branches
- Push to non-protected branches
- Open/comment on issues
- **Who**: Active contributors

**Read**
- Clone repository
- View code
- Comment on issues
- **Who**: Observers, auditors

#### Setting Team Permissions

```bash
# Via GitHub CLI
gh api repos/raphaelhaddock-blip/test-repo/collaborators/USERNAME \
  -X PUT \
  -f permission='write'

# Permissions: read, write, admin, maintain
```

**Via GitHub UI:**
1. Settings → Collaborators and teams
2. Add person/team
3. Choose role
4. Send invitation

### 4. Secret Management

#### Never Commit Secrets

**Bad:**
```python
API_KEY = "sk_live_123456789"  # ❌ NEVER DO THIS
DB_PASSWORD = "mypassword123"   # ❌ NEVER DO THIS
```

**Good:**
```python
import os
API_KEY = os.environ.get('API_KEY')  # ✅ Use environment variables
DB_PASSWORD = os.environ.get('DB_PASSWORD')  # ✅ From secrets
```

#### GitHub Secrets

**Repository Secrets:**
1. Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `API_KEY`
4. Value: Your secret
5. Add secret

**Using in Workflows:**
```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
      DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
    run: ./deploy.sh
```

**Environment Secrets:**
For production/staging separation:
1. Settings → Environments
2. New environment: "production"
3. Add environment secrets
4. Set protection rules

#### Secret Scanning Protection

**Enable:**
1. Settings → Code security and analysis
2. Enable "Secret scanning"
3. Enable "Push protection"

**What it does:**
- Scans all commits
- Blocks pushes with secrets
- Alerts on detected secrets
- Partners with token providers

### 5. Dependency Security

#### Dependabot Alerts

**Enable:**
1. Settings → Code security
2. Enable "Dependabot alerts"
3. Enable "Dependabot security updates"

**What it does:**
- Monitors dependencies
- Alerts on vulnerabilities
- Auto-creates PRs for fixes
- Weekly digest emails

#### Security Updates

**Auto-merge security patches:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
```

### 6. Code Signing

#### Require Signed Commits

**Why:** Proves commits are from verified authors

**Setup GPG:**
```bash
# Generate key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format=long

# Export public key
gpg --armor --export YOUR_KEY_ID

# Add to GitHub
# Settings → SSH and GPG keys → New GPG key

# Configure Git
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
```

**Verify commits:**
```bash
git log --show-signature
```

### 7. Audit Logging

#### What Gets Logged

**Automatic:**
- All commits (who, when, what)
- PR reviews and approvals
- Branch protections changes
- Team member changes
- Settings modifications

**Viewing Audit Log:**
1. Settings → Security → Audit log
2. Filter by action, actor, date
3. Export for compliance

#### Important Events

- `repo.access` - Access granted/revoked
- `protected_branch.update` - Protection changed
- `repo.create` - Repository created
- `repo.destroy` - Repository deleted
- `team.add_member` - Member added

### 8. Security Checklist

**Repository Setup:**
- [ ] Enable branch protection on `main`
- [ ] Require PR reviews
- [ ] Enable status checks
- [ ] Set up team permissions
- [ ] Configure GitHub Secrets
- [ ] Enable Dependabot alerts
- [ ] Enable secret scanning
- [ ] Enable CodeQL analysis

**Ongoing:**
- [ ] Review security alerts weekly
- [ ] Update dependencies monthly
- [ ] Audit team access quarterly
- [ ] Review audit logs monthly
- [ ] Rotate secrets quarterly
- [ ] Test backup/recovery annually

## 🚨 Vulnerability Reporting

### How to Report

**For Internal Team:**
1. Create **private** security advisory
2. Go to Security → Advisories
3. New draft security advisory
4. Describe vulnerability
5. Assess severity
6. Notify maintainers

**For External Reporters:**
Email: security@yourcompany.com

**Include:**
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Critical**: 24 hours
- **High**: 72 hours
- **Medium**: 1 week
- **Low**: 2 weeks

### Disclosure Policy

1. Private notification received
2. Confirm vulnerability (24-72h)
3. Develop and test fix
4. Release patch
5. Public disclosure (after 90 days or patch)

## 🏢 Business-Specific Security

### For BJB Law Firm

**Sensitive Data:**
- Client information
- Case details
- Attorney work product

**Access Control:**
- Attorneys: Read/Write
- Paralegals: Read
- Marketing: Specific folders only

**Compliance:**
- Attorney-client privilege
- State bar requirements
- Data retention policies

### For Dr. Greenthumb

**Sensitive Data:**
- Licensing agreements
- Royalty information
- Trademark filings

**Access Control:**
- B-Real: Admin
- Legal team: Write
- Business development: Read

**Compliance:**
- Cannabis regulations
- International treaties
- IP protection

### For AscendTech

**Sensitive Data:**
- Client code
- API credentials
- Customer data

**Access Control:**
- Developers: Write
- Clients: Read (specific repos)
- Contractors: Timed access

**Compliance:**
- Client NDAs
- Data protection (GDPR/CCPA)
- SOC 2 (if applicable)

## 📚 Security Resources

**GitHub Security:**
- [Security Best Practices](https://docs.github.com/en/code-security)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)

**Python Security:**
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Bandit Documentation](https://bandit.readthedocs.io/)

**General:**
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

**Remember:** Security is not a one-time setup. It's an ongoing process of monitoring, updating, and improving.