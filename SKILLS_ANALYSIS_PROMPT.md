Analyze my custom skills setup and compare it against the Claude Agent SDK capabilities. I have custom skills built for various business functions.

## TASK 1: CURRENT STATE ANALYSIS

Explore my skills directory completely (check /mnt/skills/, ~/.claude/skills/, and any .claude/projects/ directories). For each skill found:
- Document the folder structure and organization
- Analyze SKILL.md files: YAML frontmatter, instruction structure, workflow steps, dependencies
- Identify orchestration patterns: skills that delegate to others, coordination mechanisms, state management
- Categorize all skills: Orchestrators, Domain Specialists (legal, cannabis, music), Research/Analysis, Operational, Integration

## TASK 2: CLAUDE AGENT SDK COMPARISON

Compare my skills against these SDK capabilities:

**Built-in Tools:** Read, Write, Edit (files) | Bash (terminal) | Glob, Grep (search) | WebSearch, WebFetch (web) | Task (subagent delegation) | TodoWrite (tracking)

**Key Features:**
- Agent Loop: gather context → take action → verify work → repeat
- Structured Output: JSON schemas with validation
- Subagents: Spawn specialists with different models (Opus $15/M, Sonnet $3/M, Haiku $0.25/M)
- Model Selection: Cheap models for simple tasks, expensive for complex
- Session Management: Multi-turn with persistence
- Permission Hooks: Custom tool blocking and audit logging
- MCP Integration: Custom tool servers
- Parallel Execution: Multiple subagents simultaneously
- Independent Contexts: Each subagent gets fresh context (solves context overflow)

**Agent Patterns:** Multi-agent orchestration | Parallel research with aggregation | Structured output with JSON schemas | Autonomous verification loops | Cost-optimized pipelines | Resumable tasks

## TASK 3: GAP ANALYSIS

Create a comparison table for EACH skill found:

| Skill Name | Current Capability | SDK Improvement | Priority |
|------------|-------------------|-----------------|----------|

Identify:
- What SDK does BETTER: fresh contexts vs single-context, parallel vs sequential, tiered costs vs flat, structured vs unstructured output
- What SDK DOESN'T cover: domain knowledge, business workflows, industry expertise, custom integrations
- What SDK ADDS: true delegation, cost optimization, parallel execution, structured enforcement, session persistence

## TASK 4: KEY SKILL DEEP DIVE

For any orchestrator/coordinator skills, legal skills, research skills, and business-specific skills, analyze:
- Current mechanism and limitations
- SDK replacement potential
- Parallelization opportunities
- Model tier recommendations (Haiku/Sonnet/Opus)

Score each: Current limitation (1-10) | SDK improvement potential (1-10) | Implementation complexity (1-10)

## TASK 5: ARCHITECTURE RECOMMENDATION

**5.1 Design multi-agent architecture:**
```
MASTER ORCHESTRATOR (model: ?)
├── Specialist Agent 1 (model: ?)
├── Specialist Agent 2 (model: ?)
├── Research Pool (model: ?)
└── [etc based on my actual skills]
```

**5.2 Migration Priority Matrix:**
| Skill | Effort | Impact | Priority | Approach |
|-------|--------|--------|----------|----------|
| [name] | LOW/MED/HIGH | LOW/MED/HIGH | 1-10 | Rebuild/Wrap/Keep |

**5.3 Hybrid Approach:** How to keep SKILL.md as agent prompts, wrap skills in SDK structure, build orchestrator layer, implement model tiering

**5.4 Cost Analysis:** Current pricing vs SDK tiered approach, projected savings

## TASK 6: IMPLEMENTATION ROADMAP

Phase 1 (Foundation): Convert orchestrator, implement model tiering, create prompt library from SKILL.md files
Phase 2 (High-Value): Research → parallel agents, Legal → structured pipelines, other high-impact
Phase 3 (Full Integration): All specialists as subagents, cross-skill coordination, session persistence

## OUTPUT FORMAT

1. **Executive Summary** (2-3 paragraphs)
2. **Skills Inventory** (complete categorized list)
3. **Gap Analysis Table** (all skills)
4. **Detailed Evaluations** (key skills)
5. **Recommended Architecture** (diagram + explanation)
6. **Migration Roadmap** (prioritized actions)
7. **Bottom Line** (YES/NO/PARTIAL with reasoning)

## ANSWER THESE QUESTIONS

1. Is rebuilding with Agent SDK worth the effort?
2. Which skills convert first for maximum ROI?
3. Which skills stay as-is?
4. Estimated cost savings from model tiering?
5. What capabilities would I gain?
6. Realistic implementation approach?

Be direct. If my current approach is sufficient, say so. If SDK offers major advantages, be specific about where and why.
