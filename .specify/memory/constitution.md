<!--
================================================================================
SYNC IMPACT REPORT
================================================================================
Version: 1.0.0 → 1.0.1
Change Type: PATCH (ratification date update + template consistency verification)

Modified Principles: None (principles remain unchanged)

Added Sections: None

Removed Sections: None

Templates Status:
- spec-template.md: ✅ Compatible (prioritizes user stories and acceptance criteria aligned with constitution)
- plan-template.md: ✅ Compatible (Constitution Check section supports Spec-Driven Development principle)
- tasks-template.md: ✅ Compatible (user story grouping aligns with Spec-Kit Plus workflow)
- phr-template.prompt.md: ✅ Compatible (PHR workflow supports constitution governance)
- adr-template.md: ✅ Compatible (ADR process supports architectural decision documentation)

Template Consistency Actions:
- ✅ Verified all templates align with constitution principles
- ✅ Confirmed Spec-Kit Plus workflow is properly embedded in templates
- ✅ Validated security standards reflected in plan template Constitution Check section

Follow-up TODOs: None

================================================================================
-->

# Physical AI & Humanoid Robotics Book with Integrated RAG Chatbot Constitution

## Core Principles

### I. Spec-Driven Development First (NON-NEGOTIABLE)

All features, content, architecture decisions, and implementation work MUST originate from approved specifications following the Spec-Kit Plus workflow:

1. **Specification Required**: Before any implementation begins, a feature specification (`spec.md`) MUST exist and be approved
2. **Architecture Before Code**: Implementation plans (`plan.md`) MUST be created and reviewed before coding
3. **Task Breakdown**: All work MUST be broken into testable tasks (`tasks.md`) with clear acceptance criteria
4. **No Ad-Hoc Changes**: Direct code changes without corresponding spec artifacts are prohibited

**Rationale**: Spec-driven development ensures alignment, prevents scope creep, maintains architectural coherence, and enables predictable delivery. The book and chatbot complexity requires systematic planning to avoid technical debt and ensure all components integrate properly.

### II. Technical Accuracy & Documentation Alignment

All technical content, code examples, and architecture decisions MUST be accurate and aligned with official documentation:

1. **Verify Before Writing**: All technical explanations (Next.js, FastAPI, RAG, OpenAI Agents SDK, Neon, Qdrant, Docusaurus, etc.) MUST be verified against current official documentation
2. **Version Specificity**: All code and configuration MUST specify exact versions
3. **Test All Code**: Every code snippet MUST be tested in a clean environment before inclusion
4. **No Placeholders**: The final version MUST NOT contain placeholder explanations or TODO comments in content

**Rationale**: Technical inaccuracies damage credibility and cause reader frustration. Verified, tested content ensures readers can successfully reproduce implementations.

### III. Developer-Centric Clarity

All content MUST target intermediate-level developers familiar with web development basics:

1. **Prerequisites Clearly Stated**: Each chapter MUST list required knowledge and skills
2. **Learning Objectives**: Every chapter MUST have explicit, measurable learning objectives
3. **Progressive Complexity**: Concepts MUST build logically from foundations to advanced topics
4. **Why Before How**: Explain the reasoning behind architectural decisions, not just mechanics
5. **Common Pitfalls**: Document typical mistakes and how to avoid them

**Rationale**: Clear, well-structured explanations enable developers to understand not just what to do, but why—supporting deeper learning and better problem-solving.

### IV. Reproducibility & Completeness

All setup steps, commands, configurations, and code MUST be complete and reproducible:

1. **Zero Missing Steps**: Every setup command, dependency installation, and configuration MUST be documented
2. **Environment Specification**: All environment variables, configuration files, and system requirements MUST be specified
3. **Tested Instructions**: All procedures MUST be tested in a clean environment
4. **Error Handling**: Document common errors and their resolutions
5. **Verification Steps**: Each section MUST include verification steps to confirm successful completion

**Rationale**: Reproducible builds enable readers to follow along successfully and verify their understanding, maximizing learning outcomes.

### V. Production-Grade Architecture

All architecture decisions MUST follow scalable, secure, and maintainable best practices:

1. **Separation of Concerns**: Frontend (Docusaurus), backend (FastAPI), database (Neon), and vector store (Qdrant) MUST be properly separated
2. **Environment Variables**: ALL secrets and configuration MUST use environment variables (`.env`)
3. **API Security**: API keys MUST NEVER be exposed to frontend; proper CORS and rate limiting required
4. **Modular Design**: Components MUST be modular, testable, and independently maintainable
5. **Error Handling**: Robust error handling with clear user messaging

**Rationale**: Production-grade architecture ensures the chatbot functions reliably in deployment, scales appropriately, and remains maintainable.

### VI. AI-Augmented but Human-Validated

AI may generate content, but structure, validation, and refinement MUST follow strict review standards:

1. **Human Oversight**: ALL AI-generated content MUST be reviewed for accuracy, clarity, and completeness
2. **Fact-Checking**: Technical claims MUST be verified against official sources
3. **Structure Validation**: Content organization MUST align with learning objectives and logical progression
4. **Quality Gates**: Each chapter MUST pass quality checks before publication (accuracy, completeness, reproducibility)
5. **Iterative Refinement**: Content MUST be refined based on feedback and testing

**Rationale**: AI accelerates content creation but human expertise ensures quality, accuracy, and pedagogical effectiveness.

## Technology Standards

### Approved Technology Stack (CONSTRAINT)

ONLY the following technologies are approved for this project:

1. **Book Platform**: Docusaurus (latest stable version)
2. **Backend Framework**: FastAPI (Python)
3. **Database**: Neon Serverless Postgres
4. **Vector Database**: Qdrant Cloud (Free Tier)
5. **AI Layer**: OpenAI Agents SDK / ChatKit SDK
6. **Deployment**: GitHub Pages OR Vercel (for book)

### Technology Selection Rules

1. **No Unauthorized Additions**: New dependencies or technologies MUST be justified and documented in an ADR
2. **Version Pinning**: ALL dependencies MUST have pinned versions in documentation
3. **Minimal Dependencies**: Prefer fewer, well-maintained dependencies over many specialized ones
4. **Long-Term Viability**: Prefer technologies with strong community support and long-term stability

**Rationale**: A constrained, well-defined stack reduces complexity, ensures compatibility, and simplifies maintenance.

## Content Quality Standards

### Book Structure Requirements

1. **Logical Hierarchy**: Introduction → Core Concepts → Implementation → Deployment → Advanced Topics
2. **Chapter Components**: Each chapter MUST include:
   - Clear learning objectives (measurable outcomes)
   - Concept explanation (what and why)
   - Code examples (complete and runnable)
   - Practical implementation steps (reproducible)
   - Summary section (key takeaways)
3. **Code Formatting**: All code MUST be properly formatted with syntax highlighting
4. **Cross-References**: Link to related concepts and earlier/later chapters

### RAG Chatbot Quality Requirements

1. **Retrieval Accuracy**:
   - Use embeddings stored in Qdrant
   - Support semantic search
   - Restrict answers to book content only
2. **Supported Features**:
   - Full-book Q&A
   - Context-limited Q&A (answer based only on user-selected text)
3. **Response Quality**:
   - Avoid hallucinations (clearly state when information not found)
   - Cite source sections when possible
   - Provide accurate, contextually relevant answers
4. **User Experience**:
   - Clear indication of answer confidence
   - Graceful handling of out-of-scope questions
   - Fast response times (<3 seconds for typical queries)

**Rationale**: Quality standards ensure the book teaches effectively and the chatbot provides reliable assistance.

## Security & Privacy Standards

### Data Security

1. **Environment Variables**: ALL secrets (API keys, database credentials) MUST use environment variables
2. **No Hardcoded Secrets**: NEVER commit secrets to version control
3. **API Key Protection**: API keys MUST NEVER be exposed to frontend code
4. **Secure Communication**: All API communication MUST use HTTPS

### Backend Security

1. **Rate Limiting**: Implement rate limiting on all public endpoints
2. **Input Validation**: Validate and sanitize all user inputs
3. **CORS Configuration**: Properly configure CORS for production domains only
4. **Error Messages**: Generic error messages to users; detailed errors logged securely
5. **Dependency Scanning**: Regularly scan for vulnerabilities in dependencies

**Rationale**: Security best practices protect user data, prevent abuse, and ensure production reliability.

## Development Workflow

### Spec-Kit Plus Workflow

All development MUST follow this sequence:

1. **Specify**: Create feature specification with user stories, requirements, and acceptance criteria
2. **Plan**: Design architecture with technical decisions, data model, and API contracts
3. **Task Generation**: Break down implementation into testable tasks organized by user story
4. **Implement**: Build following task order (setup → foundational → user stories → polish)
5. **Validate**: Test against acceptance criteria and success metrics
6. **Document**: Update documentation and create PHR records

### Code Quality Standards

1. **Modular Architecture**: Clear separation of concerns (models, services, API routes)
2. **Folder Structure**: Organized, intuitive directory structure
3. **Type Safety**: Use type hints (Python) or TypeScript where applicable
4. **Comments**: Clear comments for complex logic; obvious code needs no comments
5. **REST Best Practices**: Follow REST principles for API design

### Testing Standards

1. **Reproducibility Tests**: All code snippets MUST be tested in clean environments
2. **Integration Tests**: Chatbot MUST be tested end-to-end (local and deployed)
3. **Retrieval Accuracy**: Test RAG retrieval against known questions
4. **Build Verification**: Book MUST build successfully with no errors or warnings

**Rationale**: Structured workflow and quality standards ensure reliable, maintainable, and production-ready code.

## Governance

### Constitution Authority

This constitution is the authoritative source for all development practices and standards. In case of conflict between this document and other practices, this constitution prevails.

### Amendment Process

1. **Proposal**: Amendments MUST be proposed with clear rationale and impact analysis
2. **Documentation**: Significant changes MUST be documented in an Architecture Decision Record (ADR)
3. **Review**: Amendments require review and approval
4. **Migration Plan**: Backward-incompatible changes MUST include migration guidance
5. **Version Bumping**: Follow semantic versioning:
   - MAJOR: Backward-incompatible governance/principle changes
   - MINOR: New principles or materially expanded guidance
   - PATCH: Clarifications, wording improvements, non-semantic changes

### Compliance Verification

1. **Pre-Implementation**: All features MUST verify constitution compliance during planning phase
2. **Code Review**: Pull requests MUST check for adherence to principles and standards
3. **Quality Gates**: Features cannot merge without passing constitution checks
4. **Regular Audits**: Periodic review of codebase for constitution compliance

### Complexity Justification

Any deviation from core principles (especially adding complexity beyond approved stack) MUST:

1. **Document the Need**: Explain why the deviation is necessary
2. **Consider Alternatives**: Demonstrate that simpler approaches were evaluated and rejected
3. **Approve**: Get explicit approval for the exception
4. **Document**: Create an ADR explaining the decision

### Runtime Development Guidance

For detailed execution workflows and command usage, refer to:
- `CLAUDE.md`: Agent-specific development guidelines and execution contract
- `.specify/templates/`: Templates for spec, plan, tasks, and ADR creation
- `.claude/commands/`: Slash command definitions for Spec-Kit Plus workflow

**Version**: 1.0.1 | **Ratified**: 2026-03-03 | **Last Amended**: 2026-03-03
