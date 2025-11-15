# Project Template Guide

## Creating New Projects from This Template

This repository can serve as a template for future projects. Here's how to use it:

### Method 1: GitHub UI
1. Go to https://github.com/raphaelhaddock-blip/test-repo
2. Click "Use this template"
3. Name your new repository
4. Click "Create repository from template"

### Method 2: GitHub CLI
```bash
gh repo create my-new-project --template raphaelhaddock-blip/test-repo --public
```

### Method 3: Via Claude with GitHub MCP
Just ask Claude:
"Create a new repository based on my test-repo template called 'project-name'"

## What's Included in This Template

### Structure
```
.
├── .github/
│   ├── workflows/          # CI/CD automation
│   ├── ISSUE_TEMPLATE/     # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/                   # Documentation
├── web_app/                # Flask application
├── tests/                  # Test files
├── .gitignore
└── README.md
```

### Features
- ✅ GitHub Actions for CI/CD
- ✅ Issue and PR templates
- ✅ Professional .gitignore
- ✅ Documentation structure
- ✅ Testing framework
- ✅ Flask web app boilerplate

## Customizing Your New Project

### Step 1: Update README.md
- Change project name
- Update description
- Modify installation instructions
- Update screenshots/demos

### Step 2: Customize Workflows
Edit `.github/workflows/` files:
- Change Python version
- Add/remove test commands
- Modify deployment targets

### Step 3: Configure Issue Templates
Edit `.github/ISSUE_TEMPLATE/`:
- Add project-specific fields
- Modify labels
- Change assignees

### Step 4: Set Up Branch Protection
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Require:
   - Pull request reviews
   - Status checks to pass
   - Branch to be up to date

## Real-World Use Cases

### For BJB Law Firm
**Content Management System:**
```
bjb-content-system/
├── templates/          # Marketing templates
├── campaigns/          # Campaign tracking
├── analytics/          # Performance data
└── workflows/          # Auto-publishing
```

**Document Automation:**
```
bjb-doc-automation/
├── contracts/          # Legal templates
├── intake_forms/       # Client forms
├── reports/            # Case reports
└── workflows/          # Auto-generation
```

### For Dr. Greenthumb
**Licensing Tracker:**
```
dr-greenthumb-licensing/
├── licenses/           # License agreements
├── trademarks/         # TM filings
├── compliance/         # Regulatory docs
└── workflows/          # Renewal reminders
```

**Brand Management:**
```
dr-greenthumb-brand/
├── assets/             # Brand assets
├── guidelines/         # Brand guidelines
├── campaigns/          # Marketing campaigns
└── analytics/          # Performance tracking
```

### For AscendTech
**Client Projects:**
```
ascendtech-client-[name]/
├── frontend/           # Client-facing code
├── backend/            # API/server
├── tests/              # Automated tests
└── workflows/          # Deploy to client
```

## Advanced Templates

### Multi-Environment Setup
```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging
on:
  push:
    branches: [ develop ]

# .github/workflows/deploy-production.yml
name: Deploy to Production
on:
  push:
    branches: [ main ]
```

### Scheduled Tasks
```yaml
name: Weekly Report
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday 9am
jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - name: Generate report
        run: python generate_report.py
```

### Notifications
```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
  with:
    slack-message: 'Deployment complete!'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Best Practices

### 1. Keep Templates Generic
- Remove project-specific code
- Use placeholders for names
- Document customization points

### 2. Version Your Templates
- Tag stable versions: `v1.0.0`
- Document breaking changes
- Maintain upgrade guides

### 3. Document Everything
- README for setup
- CONTRIBUTING for contributors
- CODE_OF_CONDUCT for community
- LICENSE for legal

### 4. Test Templates
- Create test projects
- Verify all workflows run
- Check all links work

## Quick Start Commands

### Create from Template
```bash
# Clone the template
git clone https://github.com/raphaelhaddock-blip/test-repo my-project
cd my-project

# Remove git history
rm -rf .git
git init

# Make it yours
git add .
git commit -m "Initial commit from template"
```

### Automate with Claude
```
"Create a new BJB marketing automation project 
using my test-repo template, customize it for 
tracking social media campaigns, and set up 
automated posting workflows"
```

## Resources

- [GitHub Templates Documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Awesome README](https://github.com/matiassingers/awesome-readme)
- [Choose a License](https://choosealicense.com/)

---

**Remember:** A good template saves hours of setup for every new project!