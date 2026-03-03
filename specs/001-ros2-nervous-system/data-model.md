# Data Model: Module 1 - The Robotic Nervous System (ROS 2)

**Feature**: 001-ros2-nervous-system
**Date**: 2026-03-03
**Phase**: Phase 1 - Design & Contracts

## Overview

This document defines the content entities, their structure, validation rules, and relationships for the ROS 2 educational module. While this is educational content (not a software application), treating content as entities ensures consistency, completeness, and testability.

---

## Content Entities

### Chapter

**Description**: A topical section covering a major subject area in the module.

**Fields**:
- `title` (string, required): Chapter heading
- `slug` (string, required): URL-friendly identifier for Docusaurus
- `number` (integer, required): Chapter sequence (1-3)
- `word_count` (integer, required): Actual word count (target: 800-1200)
- `learning_objectives` (array, required): List of 3-5 measurable outcomes
- `prerequisites` (array, optional): List of required prior knowledge
- `content` (markdown, required): Chapter body content
- `code_examples` (array, required): References to code example files
- `summary` (markdown, required): Key takeaways section
- `references` (array, required): Citations to technical sources
- `troubleshooting_tips` (array, required): Common errors and solutions (min 3)

**Validation Rules**:
- Word count MUST be between 800-1200 (to meet 2500-4000 total)
- MUST have at least 3 learning objectives
- MUST have at least 2 code examples
- MUST have at least 3 troubleshooting tips (requirement CR-028)
- All code examples must be referenced with file paths
- All references must be properly formatted

**State Transitions**: Draft → Review → Approved → Published

---

### CodeExample

**Description**: A complete, runnable Python script or URDF file demonstrating a specific ROS 2 concept.

**Fields**:
- `filename` (string, required): Name of code file
- `language` (enum, required): `python` | `xml` (for URDF)
- `chapter` (integer, required): Which chapter includes this example (1-3)
- `concept` (string, required): ROS 2 concept being demonstrated
- `description` (string, required): What the code does and why
- `code` (string, required): Full source code
- `lines_of_code` (integer, required): For complexity management (< 100 lines preferred)
- `dependencies` (array, required): Required ROS 2 packages or Python libraries
- `setup_steps` (array, required): Commands to prepare environment
- `verification_command` (string, optional): How to test the example
- `expected_output` (string, optional): What successful execution looks like

**Validation Rules**:
- MUST follow PEP 8 for Python (requirement CR-027)
- MUST run successfully in ROS 2 Humble environment (requirement CR-017)
- MUST include comments explaining ROS 2 concepts (requirement CR-019)
- MUST use humanoid robot scenarios (requirement CR-020)
- MUST handle initialization errors (requirement CR-012)
- MUST be < 150 lines (preferably < 100) for educational clarity

**State Transitions**: Draft → Tested → Verified → Approved

---

### LearningObjective

**Description**: A measurable skill or knowledge outcome for a chapter.

**Fields**:
- `text` (string, required): Objective statement
- `chapter` (integer, required): Associated chapter (1-3)
- `blooms_level` (enum, required): `remember` | `understand` | `apply` | `analyze` | `evaluate` | `create`
- `measurable` (boolean, required): Can this be assessed?
- `assessment_method` (string, optional): How to verify achievement

**Validation Rules**:
- MUST start with action verb (Define, Implement, Create, Explain)
- MUST be measurable (requirement CR-002)
- MUST map to at least one success criterion in spec

---

### Reference

**Description**: A cited source providing technical authority for content claims.

**Fields**:
- `title` (string, required): Document or paper title
- `authors` (array, optional): List of authors
- `type` (enum, required): `official_docs` | `academic_paper` | `book` | `tutorial`
- `url` (string, required): Link to source
- `publication_date` (date, optional): When published
- `accessed_date` (date, required): When reference was verified
- `chapters` (array, required): Which chapters cite this reference
- `notes` (string, optional): What this reference covers

**Validation Rules**:
- MUST be from official ROS 2/Gazebo docs or peer-reviewed source (requirement CR-022)
- URL MUST be accessible (requirement SC-015)
- MUST be cited in at least one chapter (requirement CR-023)
- Minimum 5 references total (requirement CR-021)

**State Transitions**: Identified → Verified → Approved

---

### TroubleshootingTip

**Description**: A common error and its solution for a specific chapter.

**Fields**:
- `error` (string, required): What goes wrong
- `symptoms` (string, required): What the learner sees
- `cause` (string, required): Why it happens
- `solution` (string, required): How to fix it
- `chapter` (integer, required): Associated chapter (1-3)
- `prevention` (string, optional): How to avoid this error

**Validation Rules**:
- MUST be specific and actionable
- MUST relate to chapter content
- Minimum 3 per chapter (requirement CR-028)

---

## Entity Relationships

```
Chapter (1) ──┬──> (3-5) LearningObjective
              │
              ├──> (2-4) CodeExample
              │
              ├──> (3+) TroubleshootingTip
              │
              └──> (1+) Reference

CodeExample (N) ──> Chapter (1)

Reference (N) ──> Chapter (M)  [many-to-many]

TroubleshootingTip (N) ──> Chapter (1)
```

**Relationship Rules**:
- A CodeExample belongs to exactly one Chapter
- A Reference can be cited by multiple Chapters
- TroubleshootingTips are chapter-specific
- All entities must trace to at least one requirement (CR-001 through CR-028)

---

## Content Structure

### Module Organization

```
Module 1: The Robotic Nervous System (ROS 2)
│
├── Chapter 1: ROS 2 Fundamentals (US1 - P1)
│   ├── Learning Objectives: 4-5
│   ├── Code Examples: 3-4 (hello node, publisher, subscriber, service)
│   ├── Troubleshooting Tips: 3-4
│   └── References: 2-3
│
├── Chapter 2: Python Agent Integration (US2 - P2)
│   ├── Learning Objectives: 4-5
│   ├── Code Examples: 2-3 (controller, state subscriber, error handling)
│   ├── Troubleshooting Tips: 3-4
│   └── References: 2-3
│
└── Chapter 3: Humanoid Robot URDF (US3 - P3)
    ├── Learning Objectives: 4-5
    ├── Code Examples: 1-2 (URDF file, validation script)
    ├── Troubleshooting Tips: 3-4
    └── References: 1-2
```

**Validation**:
- Total word count: 2500-4000 (requirement CR-003)
- Each chapter follows template (requirement CR-002)
- Progressive difficulty (constitution principle III)
- All chapters use humanoid examples (requirement CR-020)

---

## Data Flow

### Content Creation Workflow

```
1. Chapter Draft
   ├── Write learning objectives (measurable, action-oriented)
   ├── Draft content with concepts and explanations
   ├── Create code examples (test in ROS 2 Humble)
   ├── Add troubleshooting tips (based on testing)
   ├── Collect references (official/peer-reviewed)
   └── Review against requirements (CR-001 through CR-028)

2. Code Example Testing
   ├── Run in clean ROS 2 Humble environment
   ├── Verify output matches documentation
   ├── Test error handling paths
   ├── Validate comments are clear
   └── Check PEP 8 compliance

3. Chapter Review
   ├── Verify word count (800-1200)
   ├── Check all required sections present
   ├── Validate references accessible
   ├── Ensure humanoid-only examples
   └── Confirm troubleshooting tips cover common errors

4. Module Integration
   ├── Verify total word count (2500-4000)
   ├── Check chapter progression
   ├── Validate cross-references
   └── Test all code examples in sequence
```

---

## Validation Summary

**Entity Completeness**:
- ✅ All content entities defined with required fields
- ✅ Validation rules ensure requirement compliance
- ✅ Relationships support progressive learning

**Testability**:
- ✅ Each entity has measurable validation criteria
- ✅ Code examples have explicit verification steps
- ✅ Learning objectives map to success criteria

**Traceability**:
- ✅ Each entity maps to functional requirements (CR-*)
- ✅ Each chapter maps to user stories (US1-US3)
- ✅ Each reference supports technical accuracy (CR-023)

**Ready for**: contracts/ generation and quickstart.md creation
