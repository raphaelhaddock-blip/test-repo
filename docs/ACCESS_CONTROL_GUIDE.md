# Access Control Guide

## Understanding GitHub Permissions

### Permission Levels

#### 1. Read (Triage)
**Can:**
- Clone repository
- View code and history
- Open and comment on issues
- Comment on pull requests
- Fork repository

**Cannot:**
- Push code
- Merge PRs
- Change settings
- Delete anything

**Use For:**
- External auditors
- Clients viewing progress
- Observers/stakeholders
- Job candidates reviewing code

#### 2. Write (Contributor)
**Can:**
- Everything in Read
- Create branches
- Push to branches
- Open pull requests
- Request reviews

**Cannot:**
- Merge to protected branches
- Change settings
- Manage team members

**Use For:**
- Regular developers
- Content creators
- Junior team members
- Contractors

#### 3. Maintain
**Can:**
- Everything in Write
- Merge pull requests
- Manage issues and projects
- Edit wikis

**Cannot:**
- Change repository settings
- Manage webhooks
- Add collaborators

**Use For:**
- Senior developers
- Team leads
- Project managers

#### 4. Admin
**Can:**
- Everything in Maintain
- Change repository settings
- Manage team members
- Delete repository
- Manage security

**Use For:**
- Repository owners
- CTO/Technical leadership
- DevOps leads

## Real-World Access Control Scenarios

### Scenario 1: BJB Law Firm Content Team

**Team Structure:**
- 1 Marketing Director (Admin)
- 3 Content Writers (Write)
- 2 Paralegals (Read)
- 5 Attorneys (Maintain)

**Setup:**
```yaml
Marketing Director:
  - Role: Admin
  - Reason: Manages entire content strategy
  - Access: Full repository control

Content Writers:
  - Role: Write
  - Reason: Create content, cannot publish
  - Access: Create branches, open PRs
  - Workflow: Write → PR → Review → Publish

Paralegals:
  - Role: Read
  - Reason: Reference content, cannot edit
  - Access: View-only

Attorneys:
  - Role: Maintain
  - Reason: Review and approve content
  - Access: Merge approved content
```

**Protection Rules:**
- Main branch: Requires attorney approval
- Publish workflow: Only admins can trigger

### Scenario 2: Dr. Greenthumb Licensing

**Team Structure:**
- 1 B-Real (Admin)
- 2 Attorneys (Maintain)
- 1 Business Development (Write)
- 5 Licensees (Read - specific repos)

**Setup:**
```yaml
B-Real:
  - Role: Admin
  - Access: All repositories
  - Reason: Final decision maker

Attorneys:
  - Role: Maintain
  - Access: Licensing, trademarks, compliance
  - Can: Draft, review, approve agreements
  - Cannot: Delete repositories

Business Development:
  - Role: Write
  - Access: Licensing repository
  - Workflow: Draft deals → Attorney review

Licensees:
  - Role: Read
  - Access: Their specific agreement only
  - Reason: View terms, can't modify
```

**Repository Structure:**
```
dr-greenthumb-licensing/
├── private-master/        # Admin only
├── attorney-workspace/    # Attorneys: Maintain
├── business-dev/          # BD: Write
└── licensee-agreements/   # Specific: Read
    ├── barney-farm/
    ├── canada-partner/
    └── australian-group/
```

### Scenario 3: AscendTech Client Projects

**Team Structure:**
- 2 Founders (Admin)
- 5 Developers (Maintain)
- 3 Designers (Write)
- X Clients (Read - their project only)
- Contractors (Timed Write access)

**Setup:**
```yaml
Founders:
  - Role: Admin
  - Access: All client repositories
  - Reason: Business oversight

Developers:
  - Role: Maintain
  - Access: Assigned client projects
  - Can: Develop, merge, deploy

Designers:
  - Role: Write
  - Access: Assets folders only
  - Can: Upload designs, cannot deploy

Clients:
  - Role: Read
  - Access: Their repository only
  - Can: View progress, comment
  - Cannot: See code, other clients

Contractors:
  - Role: Write (timed)
  - Access: Specific feature branch
  - Duration: Project length only
  - Removed: After project completion
```

**Outside Collaborators:**
```bash
# Add contractor with expiration
gh api repos/ascendtech/client-x/collaborators/contractor \
  -X PUT \
  -f permission='write'

# Set reminder to remove after 90 days
```

## Setting Up Team-Based Access

### Creating Teams

**Via GitHub UI:**
1. Organization → Teams
2. New team
3. Name: "BJB-Attorneys"
4. Description: "Attorney review team"
5. Create team

**Team Hierarchy:**
```
BJB-Organization
├── BJB-Leadership (Admin)
│   └── Brandon, Raphy
├── BJB-Attorneys (Maintain)
│   └── 5 attorneys
├── BJB-Content (Write)
│   └── 3 writers
└── BJB-View-Only (Read)
    └── Paralegals, interns
```

### Assigning Team to Repository

**Via GitHub UI:**
1. Repository → Settings
2. Collaborators and teams
3. Add team
4. Select team: "BJB-Attorneys"
5. Choose role: "Maintain"
6. Add team

**Via Claude MCP:**
```
"Add the BJB-Attorneys team to the 
bjb-marketing-repo with Maintain access"
```

## Branch-Level Permissions

### Protected Branches

**Main Branch Rules:**
```yaml
Branch: main

Require:
  - Pull request before merging: ✓
  - Approvals: 1
  - Status checks: ✓
  - Conversation resolution: ✓
  - Up to date before merge: ✓

Restrictions:
  - Restrict pushes: Admins only
  - Allow force pushes: ✗
  - Allow deletions: ✗

Who can merge:
  - Team: BJB-Attorneys
  - Role: Maintain or higher
```

**Develop Branch Rules:**
```yaml
Branch: develop

Require:
  - Pull request: ✓
  - Status checks: ✓

Who can merge:
  - Team: BJB-Content
  - Role: Write or higher
```

### CODEOWNERS File

**Purpose:** Auto-assign reviewers based on file changes

**Create `.github/CODEOWNERS`:**
```
# Global owners
* @raphaelhaddock-blip

# Marketing content
/content/ @bjb-attorneys
/blog/ @bjb-content

# Legal documents
/contracts/ @bjb-attorneys @legal-team
/compliance/ @bjb-attorneys

# Technical
/workflows/ @raphy @devops-team
/.github/ @raphy

# Specific files
README.md @bjb-leadership
SECURITY.md @security-team
```

**How it works:**
1. PR touches `/contracts/new-agreement.md`
2. Auto-requests review from @bjb-attorneys
3. Requires their approval to merge

## Environment-Based Access

### Environments

**Use Case:** Different rules for staging vs production

**Create Environment:**
1. Settings → Environments
2. New environment: "production"
3. Configure:
   - Required reviewers: @bjb-leadership
   - Wait timer: 5 minutes
   - Deployment branches: main only

**Workflow Usage:**
```yaml
jobs:
  deploy:
    environment: production
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ./deploy.sh
```

**Result:**
- Deployment to production requires approval
- Only from main branch
- 5-minute cooldown period

## Audit and Monitoring

### Who Has Access?

**Check Current Access:**
```bash
# List all collaborators
gh api repos/raphaelhaddock-blip/test-repo/collaborators

# List teams
gh api repos/raphaelhaddock-blip/test-repo/teams
```

**Regular Access Review:**
- Monthly: Review all team members
- Quarterly: Audit outside collaborators
- Annually: Review all permissions
- On departure: Immediate removal

### Access Logs

**View Recent Activity:**
1. Settings → Security → Audit log
2. Filter: `action:repo.access`
3. Export CSV for compliance

**Key Events to Monitor:**
- `repo.add_member` - New collaborator
- `repo.remove_member` - Removed collaborator
- `protected_branch.update` - Protection changed
- `repo.access_granted` - Permission elevated

## Best Practices

### 1. Principle of Least Privilege
- Give minimum access needed
- Use time-limited access for contractors
- Regular permission audits

### 2. Team-Based, Not Individual
- Manage teams, not individuals
- Easier to maintain
- Better for onboarding/offboarding

### 3. Separate by Function
```
Good:
- content-writers
- legal-reviewers
- technical-admins

Bad:
- everyone-team
- all-access
```

### 4. Document Everything
- Why each team exists
- What each role can do
- Approval process for changes

### 5. Automate Offboarding
```yaml
# Checklist when someone leaves:
- [ ] Remove from all teams
- [ ] Revoke personal access tokens
- [ ] Review their recent commits
- [ ] Transfer repository ownership
- [ ] Rotate shared secrets they accessed
- [ ] Document in audit log
```

## Emergency Access

### Break Glass Procedure

**When:** Critical production issue, normal approvers unavailable

**Process:**
1. Use emergency admin account
2. Document reason in commit message
3. Create incident report
4. Notify team within 1 hour
5. Post-mortem within 24 hours

**Emergency Admin Account:**
- Separate from personal accounts
- Requires 2FA
- Logged and monitored
- Used only for emergencies

## Compliance

### For Legal Firms (BJB)
- **Requirement:** Attorney-client privilege
- **Solution:** Read-only for non-attorneys
- **Audit:** Quarterly access review

### For Cannabis (Dr. Greenthumb)
- **Requirement:** Regulatory compliance
- **Solution:** Audit trails for all changes
- **Retention:** 7-year document retention

### For Tech (AscendTech)
- **Requirement:** Client data protection
- **Solution:** Client-specific repositories
- **Audit:** Monthly access review

---

**Key Takeaway:** Good access control is invisible when working, but critical when something goes wrong. Set it up properly from the start.