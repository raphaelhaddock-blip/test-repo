# Security Setup Checklist

Use this checklist when setting up a new repository or conducting security audits.

## Initial Setup

### Repository Security
- [ ] Enable branch protection on `main`
  - [ ] Require pull request reviews (minimum 1)
  - [ ] Require status checks to pass
  - [ ] Require branches to be up to date
  - [ ] Restrict who can push
  - [ ] Prohibit force pushes
  - [ ] Prohibit deletions

- [ ] Enable branch protection on `develop` (if used)
  - [ ] Require status checks
  - [ ] Allow team members to merge

- [ ] Create CODEOWNERS file
  - [ ] Assign owners for critical paths
  - [ ] Test auto-review assignment

### Access Control
- [ ] Set up teams
  - [ ] Admin team (2-3 people max)
  - [ ] Maintainer team
  - [ ] Contributor team
  - [ ] Read-only team

- [ ] Assign team permissions
  - [ ] Verify each team's access level
  - [ ] Document why each team has access

- [ ] Configure environments
  - [ ] Create "production" environment
  - [ ] Require approvals for production
  - [ ] Set deployment branch restrictions

### Secret Management
- [ ] Enable secret scanning
- [ ] Enable push protection
- [ ] Add necessary repository secrets
  - [ ] API keys
  - [ ] Database credentials
  - [ ] Deployment tokens
- [ ] Document which secrets exist (not values!)
- [ ] Set secret rotation schedule

### Dependency Security
- [ ] Enable Dependabot alerts
- [ ] Enable Dependabot security updates
- [ ] Configure Dependabot (dependabot.yml)
- [ ] Review and merge initial dependency updates

### Code Security
- [ ] Enable CodeQL analysis
  - [ ] Configure for your languages
  - [ ] Set scan schedule (weekly recommended)

- [ ] Add security scanning workflow
  - [ ] Dependency scanning (Safety/npm audit)
  - [ ] Code scanning (Bandit/ESLint)
  - [ ] Secret scanning (TruffleHog)

### Documentation
- [ ] Create SECURITY.md
  - [ ] Vulnerability reporting process
  - [ ] Response timeline
  - [ ] Disclosure policy

- [ ] Create security section in README
  - [ ] Link to SECURITY.md
  - [ ] Security badges (if applicable)

- [ ] Document access control policy
  - [ ] Who has access
  - [ ] Why they have access
  - [ ] Review schedule

## Ongoing Maintenance

### Daily
- [ ] Review security alerts (if critical)
- [ ] Check failed security scans

### Weekly
- [ ] Review Dependabot PRs
- [ ] Check security scan results
- [ ] Review access logs for anomalies

### Monthly
- [ ] Review team access
  - [ ] Remove inactive members
  - [ ] Verify permissions are correct

- [ ] Update dependencies
  - [ ] Review and test updates
  - [ ] Merge security patches

- [ ] Review audit logs
  - [ ] Check for unusual activity
  - [ ] Document any incidents

### Quarterly
- [ ] Full access audit
  - [ ] Review all collaborators
  - [ ] Review all teams
  - [ ] Remove unnecessary access

- [ ] Rotate secrets
  - [ ] API keys
  - [ ] Service account passwords
  - [ ] Deployment tokens

- [ ] Review branch protection rules
  - [ ] Still appropriate?
  - [ ] Need updates?

- [ ] Security training
  - [ ] Update team on new threats
  - [ ] Review security procedures

### Annually
- [ ] Full security assessment
- [ ] Penetration testing (if applicable)
- [ ] Compliance audit
- [ ] Disaster recovery drill
- [ ] Update security documentation

## Incident Response

### When Security Alert Fires
- [ ] Assess severity (Critical/High/Medium/Low)
- [ ] Notify appropriate team members
- [ ] Create private security advisory
- [ ] Investigate scope of vulnerability
- [ ] Develop fix
- [ ] Test fix thoroughly
- [ ] Deploy fix
- [ ] Update dependencies
- [ ] Document incident
- [ ] Post-mortem (if critical/high)

### When Secret Leaked
- [ ] Immediately revoke the secret
- [ ] Generate new secret
- [ ] Update in GitHub Secrets
- [ ] Redeploy affected services
- [ ] Scan for unauthorized usage
- [ ] Document incident
- [ ] Review how it happened
- [ ] Implement prevention

### When Unauthorized Access Detected
- [ ] Immediately revoke access
- [ ] Review what they accessed
- [ ] Check for data exfiltration
- [ ] Review all recent changes
- [ ] Notify affected parties
- [ ] Document incident
- [ ] Update access controls

## Compliance Checks

### For Legal (BJB)
- [ ] Attorney-client privilege maintained
  - [ ] No client data in public repos
  - [ ] Appropriate access controls
  - [ ] Audit trail enabled

- [ ] Document retention policy followed
  - [ ] 7-year retention minimum
  - [ ] Secure deletion after retention

### For Cannabis (Dr. Greenthumb)
- [ ] Regulatory compliance
  - [ ] All licenses documented
  - [ ] Renewal dates tracked
  - [ ] Audit trail for changes

- [ ] IP protection
  - [ ] Trademarks properly filed
  - [ ] Trade secrets protected
  - [ ] Licensing agreements secured

### For Tech (AscendTech)
- [ ] Client data protection
  - [ ] Separate repos per client
  - [ ] Client can't see other clients
  - [ ] NDAs enforced through access control

- [ ] SOC 2 compliance (if applicable)
  - [ ] Access controls documented
  - [ ] Change management process
  - [ ] Incident response plan

## Pre-Launch Checklist

Before deploying to production:

- [ ] All security scans passing
- [ ] No known vulnerabilities
- [ ] All secrets in GitHub Secrets (not code)
- [ ] Branch protection enabled
- [ ] Required reviewers configured
- [ ] Deployment requires approval
- [ ] Monitoring/alerting configured
- [ ] Backup/recovery tested
- [ ] Incident response plan documented
- [ ] Team trained on security procedures

## Emergency Contacts

```yaml
Security Lead: Raphy Haddock
Email: raphael.haddock@gmail.com

Backup: [Name]
Email: [Email]

GitHub Support: https://support.github.com/
Emergency: [Emergency contact number]
```

---

**Last Updated:** [Date]
**Next Review:** [Date + 90 days]
**Reviewed By:** [Name]