# Skills vs Agent SDK Analysis Prompt

Copy and paste this entire prompt into Claude Code on your local machine where your /mnt/skills/ directory exists.

---

## PROMPT START

I need you to perform a comprehensive analysis of my custom skills setup and compare it against the Claude Agent SDK capabilities. I have 28 custom skills built for various business functions.

### TASK 1: CURRENT STATE ANALYSIS

**1.1 Directory Structure Analysis**
- Explore `/mnt/skills/` completely
- List every skill directory found
- Document the folder structure and organization pattern
- Identify any shared utilities, configs, or common files

**1.2 SKILL.md File Analysis**
For each skill found, analyze:
- The YAML frontmatter (name, description, triggers)
- The instruction structure and format
- Workflow steps and their complexity
- Dependencies on other skills or external systems
- Input/output expectations

**1.3 Agent Pattern Detection**
Look for any existing patterns that resemble multi-agent systems:
- Orchestration skills that delegate to others
- Skills that reference or call other skills
- Coordination mechanisms between skills
- State management or context passing patterns

**1.4 Categorize All Skills**
Group skills by type:
- Orchestrators/Coordinators
- Domain Specialists (legal, cannabis, music, etc.)
- Research/Analysis skills
- Operational/Administrative skills
- Integration skills (external services)

---

### TASK 2: CLAUDE AGENT SDK COMPARISON

Compare my skills against these SDK capabilities:

**2.1 Built-in Tools**
| Tool | Purpose |
|------|---------|
| Read, Write, Edit | File operations |
| Bash | Terminal commands |
| Glob, Grep | File finding/searching |
| WebSearch, WebFetch | Web access |
| Task | Subagent delegation |
| TodoWrite | Task tracking |

**2.2 Key SDK Features**
- **Agent Loop**: gather context → take action → verify work → repeat
- **Structured Output**: JSON schemas with validation
- **Subagents**: Spawn specialized agents with different models (Opus $15/M, Sonnet $3/M, Haiku $0.25/M)
- **Model Selection**: Use cheap models for simple tasks, expensive for complex
- **Session Management**: Multi-turn conversations with persistence
- **Permission Hooks**: Custom tool blocking and audit logging
- **MCP Integration**: Custom tool servers
- **Parallel Execution**: Multiple subagents running simultaneously
- **Independent Contexts**: Each subagent gets fresh context (solves context overflow)

**2.3 Agent Patterns the SDK Enables**
- Multi-agent orchestration (coordinator + specialists)
- Parallel research with result aggregation
- Structured code review with JSON feedback
- Autonomous file analysis with verification loops
- Cost-optimized pipelines (Haiku for search, Opus for synthesis)
- Resumable long-running tasks

---

### TASK 3: GAP ANALYSIS

Create a detailed comparison table for each skill:

```
| Skill Name | Current Capability | SDK Improvement | Priority |
|------------|-------------------|-----------------|----------|
| [skill]    | [what it does]    | [what SDK adds] | HIGH/MED/LOW |
```

Specifically identify:

**3.1 What my skills do that SDK does BETTER:**
- Single-context limitations vs multi-agent fresh contexts
- Sequential execution vs parallel subagents
- Flat cost model vs tiered model selection
- Unstructured output vs JSON schema validation
- Manual verification vs agent loop verification

**3.2 What my skills do that SDK DOESN'T cover:**
- Domain-specific knowledge and terminology
- Business-specific workflows and procedures
- Industry expertise encoded in prompts
- Custom integrations unique to my setup

**3.3 Where SDK adds capabilities I DON'T have:**
- True delegation to independent agents
- Cost optimization through model selection
- Parallel execution with result aggregation
- Structured output enforcement
- Session persistence and resumption
- Context overflow solutions

---

### TASK 4: SPECIFIC SKILL EVALUATION

Analyze these skills in detail (if they exist):

**4.1 cypress-hill-orchestrator** (master coordination)
- Current coordination mechanism
- How it delegates to other skills
- Context management approach
- SDK orchestrator replacement potential

**4.2 touring-manager & vegas-residency-strategy**
- Business logic complexity
- External data dependencies
- Parallelization opportunities
- Model tier recommendations

**4.3 cannabis-licensing-specialist**
- Regulatory research needs
- Compliance tracking requirements
- Structured output benefits (JSON checklists)
- Multi-jurisdiction handling

**4.4 bjb-legal-opinions & super-lawyer**
- Reasoning complexity
- Research depth requirements
- Multi-stage analysis benefits
- Structured legal output schemas

**4.5 deep-research-analyst**
- Current context limitations
- Parallel search opportunities
- Cost optimization potential (Haiku for searches)
- Synthesis quality improvements

For each, provide:
- Current limitation score (1-10)
- SDK improvement potential (1-10)
- Implementation complexity (1-10)
- Recommended approach

---

### TASK 5: ARCHITECTURE RECOMMENDATION

**5.1 Proposed Multi-Agent Architecture**
Design a new architecture diagram showing:
```
MASTER ORCHESTRATOR (model: ?)
├── Specialist Agent 1 (model: ?)
├── Specialist Agent 2 (model: ?)
├── Research Pool (model: ?)
└── [etc.]
```

**5.2 Migration Priority Matrix**
| Skill | Effort | Impact | Priority | Approach |
|-------|--------|--------|----------|----------|
| [name] | LOW/MED/HIGH | LOW/MED/HIGH | 1-10 | Rebuild/Wrap/Keep |

**5.3 Hybrid Approach Design**
Show how to:
- Keep SKILL.md files as agent system prompts
- Wrap existing skills in SDK agent structure
- Build new SDK orchestrator layer
- Implement model tiering strategy

**5.4 Cost Analysis**
Estimate cost differences:
- Current: All queries at [model] pricing
- SDK: Tiered approach with Haiku/Sonnet/Opus mix
- Projected savings percentage

---

### TASK 6: IMPLEMENTATION ROADMAP

**Phase 1: Foundation**
- [ ] Convert orchestrator to SDK agent
- [ ] Implement model tiering
- [ ] Create shared prompt library from SKILL.md files

**Phase 2: High-Value Conversions**
- [ ] Deep research → parallel search agents
- [ ] Legal analysis → structured output pipeline
- [ ] [Other high-impact skills]

**Phase 3: Full Integration**
- [ ] All specialists as subagents
- [ ] Cross-skill coordination
- [ ] Session persistence implementation

---

### OUTPUT FORMAT

Provide your analysis in these sections:

1. **Executive Summary** (2-3 paragraphs)
2. **Skills Inventory** (complete list with categories)
3. **Gap Analysis Table** (all skills compared)
4. **Detailed Evaluations** (for key skills)
5. **Recommended Architecture** (diagram + explanation)
6. **Migration Roadmap** (prioritized action items)
7. **Bottom Line** (clear YES/NO/PARTIAL recommendation with reasoning)

---

### CRITICAL QUESTIONS TO ANSWER

1. Is rebuilding with the Agent SDK worth the effort?
2. Which skills should be converted first for maximum ROI?
3. Which skills should stay as-is?
4. What's the estimated cost savings from model tiering?
5. What capabilities would I gain that I don't have today?
6. What's the realistic implementation timeline?

Be direct and honest. If my current approach is sufficient, say so. If the SDK offers major advantages, be specific about where and why.

## PROMPT END

---

*Save this file and paste the content between "PROMPT START" and "PROMPT END" into Claude Code on your local machine.*
