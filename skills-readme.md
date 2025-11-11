# Claude Code Skills for 3D Print MVP

This directory contains AI-assisted development skills for use with Claude Code. These skills provide best practices, common patterns, and expert knowledge for key technologies in the project.

## Available Skills

### 1. [trellis-expert.md](trellis-expert.md)
Expert knowledge for Microsoft TRELLIS (Image-to-3D generation)
- Model loading and configuration
- Single vs multi-image processing
- Output format handling
- Performance optimization
- Memory management

### 2. [medusa-ecommerce.md](medusa-ecommerce.md)
Medusa.js e-commerce backend expertise
- Custom module creation
- Product and order management
- Payment integration
- Subscription handling
- Admin customization

### 3. [security-expert.md](security-expert.md)
Zero-trust security implementation
- Encryption best practices
- Rate limiting strategies
- Input validation
- Audit logging
- Watermarking techniques

### 4. [testing-expert.md](testing-expert.md)
Comprehensive testing strategies
- Unit test patterns
- Integration testing
- E2E test scenarios
- Performance benchmarking
- Security testing

## How to Use

### With Claude Code Desktop

1. Place these files in `.claude/skills/` directory
2. Claude Code will automatically load them
3. Reference skills in your prompts:
   ```
   "Using the TRELLIS expert skill, help me optimize memory usage"
   ```

### With Claude.ai Web

1. Copy skill content into your conversation
2. Reference when asking questions:
   ```
   "Based on the Medusa ecommerce patterns, how should I structure custom modules?"
   ```

### With Archon MCP

```bash
# Index skills as knowledge base
archon index-dir .claude/skills

# Query skills
archon query "TRELLIS multi-image processing pattern"
archon query "Medusa custom service implementation"
```

## Skill Format

Each skill follows this structure:

```markdown
---
name: Skill Name
description: Brief description
technologies: [tech1, tech2]
---

## Overview
General introduction

## Common Patterns
Frequently used code patterns

## Best Practices
Recommended approaches

## Common Issues
Known pitfalls and solutions

## Example Usage
Real-world examples
```

## Creating New Skills

To add a new skill:

1. Create file: `.claude/skills/your-skill-name.md`
2. Use the template above
3. Include:
   - Code examples
   - Common patterns
   - Error handling
   - Best practices
4. Test with Claude Code

## Updating Skills

When technologies update:
1. Review official documentation
2. Update code examples
3. Add new patterns discovered
4. Remove deprecated approaches
5. Test changes

## Skill Priorities

### High Priority (Essential)
- ✅ trellis-expert.md
- ✅ medusa-ecommerce.md
- ✅ security-expert.md
- ✅ testing-expert.md

### Medium Priority (Helpful)
- 🔄 fastapi-patterns.md
- 🔄 runpod-deployment.md
- 🔄 nextjs-optimization.md

### Future Additions
- 📋 gsplat-integration.md (Phase 2)
- 📋 sugar-refinement.md (Phase 2)
- 📋 freecad-advanced.md (Phase 3)

## Best Practices for Skill Usage

1. **Be Specific**: Reference exact skill sections
   ```
   ❌ "Help with TRELLIS"
   ✅ "Using TRELLIS expert skill, implement multi-image processing with VRAM optimization"
   ```

2. **Combine Skills**: Use multiple skills together
   ```
   "Using TRELLIS expert and security expert skills, implement encrypted model loading"
   ```

3. **Update Context**: Keep Claude informed of changes
   ```
   "I modified the TRELLIS pipeline based on your suggestion. Here's what changed..."
   ```

4. **Validate Examples**: Always test generated code
   ```
   "Can you verify this code against TRELLIS expert best practices?"
   ```

## Skill Maintenance Schedule

- **Weekly**: Review for quick fixes
- **Monthly**: Update with new patterns
- **Quarterly**: Major version updates
- **Annually**: Complete skill audit

## Contributing to Skills

When you discover new patterns:

1. Document the pattern with example
2. Add to appropriate skill file
3. Include context (when to use)
4. Add error handling notes
5. Test with Claude Code

## Troubleshooting

### Skill Not Loading
```bash
# Check file location
ls -la .claude/skills/

# Verify file format
head .claude/skills/trellis-expert.md

# Check Claude Code settings
# Settings > Features > Custom Skills
```

### Skill Not Working
1. Check YAML front matter syntax
2. Ensure proper markdown formatting
3. Validate code examples
4. Test with simple query

### Conflicts Between Skills
If skills contradict:
1. Newer pattern takes precedence
2. More specific beats general
3. Document exceptions
4. Update both skills for consistency

## Skill Templates

### Basic Skill Template
```markdown
---
name: Technology Name Expert
description: Expert knowledge for [Technology]
technologies: [tech1, tech2]
version: 1.0.0
last_updated: 2025-11-08
---

## Quick Start
[Essential code to get started]

## Common Patterns
[Frequently used patterns]

## Best Practices
[Recommended approaches]

## Common Issues
[Known pitfalls]

## Examples
[Real-world examples]
```

### Advanced Skill Template
```markdown
---
name: Advanced [Technology] Patterns
description: Advanced patterns for [Technology]
technologies: [tech1, tech2]
difficulty: advanced
prerequisites: [basic-skill]
version: 1.0.0
---

## Advanced Patterns
[Complex implementations]

## Performance Optimization
[Optimization techniques]

## Edge Cases
[Unusual scenarios]

## Production Considerations
[Deployment notes]
```

---

## Quick Reference

| Skill | Use For | Key Sections |
|-------|---------|--------------|
| **trellis-expert** | TRELLIS API usage | Model loading, inference, memory |
| **medusa-ecommerce** | Medusa customization | Modules, services, products |
| **security-expert** | Security implementation | Encryption, validation, auditing |
| **testing-expert** | Test writing | Unit, integration, E2E tests |

---

*For questions or improvements, update this README and commit changes.*
