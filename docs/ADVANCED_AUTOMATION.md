# Advanced Automation Guide

## Multi-Environment Deployments

### The Problem

You don't want to deploy untested code directly to production. You need:
- **Development** - Test new features
- **Staging** - Final testing before production
- **Production** - Live customer-facing system

### The Solution

**Branch Strategy:**
```
feature/* → Development environment
develop → Staging environment  
main → Production environment
```

**Workflow:**
1. Developer creates `feature/new-calculator`
2. Auto-deploys to dev.yourcompany.com
3. Merge to `develop` → Auto-deploys to staging
4. Test on staging
5. Merge to `main` → Requires approval → Deploys to production

### Implementation

**Environment Configuration:**
```yaml
# In repository settings:
Environments:
  - development (no protection)
  - staging (require tests pass)
  - production (require approval + tests)
```

**Secrets Per Environment:**
```
Development:
  DATABASE_URL: dev-database-url
  API_KEY: dev-api-key

Staging:
  DATABASE_URL: staging-database-url
  API_KEY: staging-api-key

Production:
  DATABASE_URL: prod-database-url
  API_KEY: prod-api-key
```

### Real-World Example: BJB Marketing System

**Development:**
- Writers test content formatting
- Preview how it will look
- No impact on live site

**Staging:**
- Marketing director reviews
- Legal approves messaging
- Final checks before publishing

**Production:**
- Requires Brandon's approval
- Publishes to bjb.com
- Tracked in analytics

## Scheduled Automation

### Weekly Tasks

**Use Cases:**
- Generate weekly reports
- Clean up old data
- Update dependencies
- Send reminders

**Example: Dr. Greenthumb Trademark Renewals**

```yaml
Schedule: Every Monday 9am

Tasks:
1. Check trademark renewal dates
2. Flag any due within 90 days
3. Create issues for renewals needed
4. Email legal team summary
5. Update tracking dashboard
```

**Business Impact:**
- Never miss $7,800+ renewal deadlines
- Proactive vs reactive
- Automated compliance

### Daily Tasks

**Use Cases:**
- Sync external data
- Backup critical files
- Monitor compliance
- Generate reports

**Example: AscendTech Client Analytics**

```yaml
Schedule: Every day at midnight

Tasks:
1. Pull analytics from all client funnels
2. Calculate conversion rates
3. Generate performance reports
4. Create alerts for anomalies
5. Update client dashboards
```

**Business Impact:**
- Automated client reporting
- Proactive optimization alerts
- No manual data collection

### Monthly Tasks

**Use Cases:**
- Compliance reports
- Financial summaries
- Team metrics
- Archive old data

**Example: BJB Office Performance**

```yaml
Schedule: 1st of every month

Tasks:
1. Calculate cases per office
2. Track revenue by location
3. Identify underperforming offices
4. Generate expansion recommendations
5. Create board presentation
```

## Database Migrations

### Why This Matters

Changing database structure is dangerous:
- Can lose data
- Can break application
- Hard to rollback

### Safe Migration Process

**Step 1: Create Migration**
```sql
-- migrations/001_add_user_preferences.sql
ALTER TABLE users ADD COLUMN preferences JSONB;
CREATE INDEX idx_user_preferences ON users(preferences);
```

**Step 2: Test Automatically**
```yaml
On PR:
  1. Create test database
  2. Apply migration
  3. Verify schema
  4. Test rollback
  5. Run application tests
```

**Step 3: Apply Safely**
```yaml
On merge to main:
  1. Backup production database
  2. Apply migration during low-traffic window
  3. Verify success
  4. Monitor for issues
  5. Keep backup for 7 days
```

### Real-World: AscendTech Client Database

**Scenario:** Adding new analytics table

**Without automation:**
- Manual SQL on production 😰
- Hope nothing breaks
- No rollback plan
- Potential downtime

**With automation:**
- Test on dev database ✅
- Review migration in PR ✅
- Auto-backup before applying ✅
- Rollback ready ✅
- Zero downtime ✅

## Notification Systems

### When to Notify

**Critical:**
- Production deployment fails
- Security vulnerability found
- Test failures on main branch
- Data breach detected

**Important:**
- PR ready for review
- Release published
- Scheduled task fails
- Resource limits reached

**Info:**
- New issue created
- Weekly reports ready
- Successful deployments

### Notification Channels

**Email:**
- Good for: Compliance, documentation
- Bad for: Urgent issues (delayed)

**Slack:**
- Good for: Team collaboration, urgent alerts
- Bad for: Long-term records

**SMS:**
- Good for: Critical production issues
- Bad for: Everything else (expensive, intrusive)

**GitHub Issues:**
- Good for: Trackable tasks, reports
- Bad for: Urgent notifications

### Example: BJB Alert System

**Critical (SMS + Slack):**
- Website down
- Security breach
- Database failure

**Important (Slack):**
- Content ready for attorney review
- New case intake submitted
- Marketing campaign deployed

**Info (GitHub Issues):**
- Weekly performance report
- Dependency updates available
- Monthly analytics summary

## Advanced Patterns

### Matrix Builds

**Test across multiple versions:**
```yaml
strategy:
  matrix:
    python: [3.9, 3.10, 3.11, 3.12]
    os: [ubuntu-latest, macos-latest, windows-latest]
```

**Use Case:**
- Ensure compatibility
- Find platform-specific bugs
- Support multiple environments

### Conditional Workflows

**Run different steps based on conditions:**
```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: ./deploy-prod.sh

- name: Deploy to staging
  if: github.ref == 'refs/heads/develop'
  run: ./deploy-staging.sh
```

### Composite Actions

**Reuse common steps:**
```yaml
# .github/actions/setup-python/action.yml
name: Setup Python Environment
runs:
  steps:
    - uses: actions/setup-python@v4
    - run: pip install -r requirements.txt
    - run: pip install pytest
```

**Then use it:**
```yaml
steps:
  - uses: ./.github/actions/setup-python
  - run: pytest
```

### Workflow Reuse

**Call one workflow from another:**
```yaml
jobs:
  call-tests:
    uses: ./.github/workflows/test.yml
  
  deploy:
    needs: call-tests
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

## Business Automation Examples

### BJB: Content Publishing Pipeline

**Flow:**
```
1. Writer creates content → Opens PR
2. Auto-check: grammar, links, formatting
3. Assign to attorney for review
4. Attorney approves → Merge to staging
5. Marketing director reviews staging
6. Approve → Deploy to production
7. Auto-post to social media
8. Track engagement
9. Weekly report to Brandon
```

**Automation:**
- Grammar checking
- Link validation
- Auto-assignment
- Staging deployment
- Social media posting
- Analytics tracking
- Report generation

**Manual:**
- Attorney review
- Marketing director approval

### Dr. Greenthumb: License Management

**Flow:**
```
1. Business dev creates deal → Opens PR
2. Auto-check: template compliance
3. Verify territory availability
4. Assign to legal team
5. Legal reviews and modifies
6. B-Real approves → Merge
7. Generate executed agreement
8. Track royalty payments
9. Set renewal reminders
10. Monthly royalty report
```

**Automation:**
- Template validation
- Territory checking
- Document generation
- Payment tracking
- Renewal reminders
- Royalty reports

**Manual:**
- Legal review
- B-Real approval
- Negotiation

### AscendTech: Client Delivery

**Flow:**
```
1. Developer commits code → Auto-test
2. Pass → Deploy to dev environment
3. Create PR → Request review
4. Senior dev reviews
5. Approve → Deploy to staging
6. Run client acceptance tests
7. Client approves → Deploy to production
8. Monitor performance
9. Auto-generate client report
10. Invoice client automatically
```

**Automation:**
- Testing
- Dev/staging deployment
- Acceptance tests
- Production deployment
- Performance monitoring
- Client reporting
- Invoicing

**Manual:**
- Code review
- Client approval

## Cost Optimization

### GitHub Actions is Free for Public Repos

**Private repos get:**
- 2,000 minutes/month (free tier)
- 3,000 minutes/month (Pro - $4/user)
- 50,000 minutes/month (Team - $4/user)

### Optimization Strategies

**1. Cache Dependencies**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```
**Saves:** 30-60 seconds per run

**2. Run in Parallel**
```yaml
jobs:
  test-unit:
    runs-on: ubuntu-latest
  test-integration:
    runs-on: ubuntu-latest
```
**Saves:** 50% time (runs simultaneously)

**3. Skip Unnecessary Runs**
```yaml
on:
  pull_request:
    paths-ignore:
      - '**.md'
      - 'docs/**'
```
**Saves:** Don't run on documentation changes

## Monitoring & Debugging

### Workflow Logs

**Access:**
1. Actions tab
2. Click workflow run
3. Click job
4. View step logs

**Download:**
```bash
gh run download <run-id>
```

### Common Issues

**Issue: Workflow not triggering**
- Check branch name matches trigger
- Verify file is in `.github/workflows/`
- Ensure YAML is valid

**Issue: Secret not found**
- Verify secret name matches exactly
- Check environment (prod vs staging)
- Ensure secret is set in settings

**Issue: Tests failing in CI but pass locally**
- Check Python version
- Verify dependencies
- Check environment variables
- Look for timing issues

### Debug Mode

**Enable:**
```yaml
- name: Debug
  run: echo "::debug::This is a debug message"
```

**Set secret:**
`ACTIONS_STEP_DEBUG = true`

## Best Practices

### 1. Keep Workflows Simple
- One workflow = one purpose
- Easy to understand
- Easy to debug

### 2. Use Environments
- Separate dev/staging/prod
- Different secrets per environment
- Require approvals for production

### 3. Cache Aggressively
- Dependencies
- Build artifacts
- Test data

### 4. Monitor Costs
- Track minute usage
- Optimize slow workflows
- Use self-hosted runners for heavy workloads

### 5. Document Everything
- What each workflow does
- When it runs
- Who to contact for issues

---

**Remember:** Automation should make life easier, not more complex. Start simple, add complexity only when needed.