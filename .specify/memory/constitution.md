<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- List of modified principles:
  - PRINCIPLE_1: Content-First Approach
  - PRINCIPLE_2: Adherence to Docusaurus Conventions
  - PRINCIPLE_3: Continuous Deployment via GitHub Pages
  - PRINCIPLE_4: Markdown as the Source of Truth
  - PRINCIPLE_5: Structure Follows Outline
- Added sections: Development Workflow, Governance
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (No changes needed, constitution check is generic)
  - ✅ .specify/templates/spec-template.md (No changes needed, requirements are generic)
  - ✅ .specify/templates/tasks-template.md (No changes needed, task structure is generic)
- Follow-up TODOs: None
-->
# Docusaurus Book Generation Constitution

## Core Principles

### I. Content-First Approach
The primary focus is on creating high-quality, clear, and accurate book content. The technology and tools, including Docusaurus, are secondary to the quality of the written material. All technical decisions must support the goal of delivering excellent content.

### II. Adherence to Docusaurus Conventions
The project must follow idiomatic Docusaurus practices for site structure, file-based routing, MDX components, and versioning. This ensures maintainability and avoids "fighting the framework." Customizations should be minimal and well-justified.

### III. Continuous Deployment via GitHub Pages
All content and configuration changes merged into the `main` branch must be automatically built and deployed to GitHub Pages. This ensures the publicly accessible book is always synchronized with the source of truth.

### IV. Markdown as the Source of Truth
All book content, including chapters, subchapters, and documentation, must be written and stored in Markdown (`.md` or `.mdx`) files. This ensures content is portable, version-controllable, and easy to edit by writers and developers.

### V. Structure Follows Outline
The Docusaurus sidebar navigation and document structure must precisely reflect the agreed-upon book outline. Any changes to the book's chapter or subchapter organization must be approved and updated in the outline first.

## Development Workflow

All changes, whether content or code, must be introduced through Pull Requests. Each PR must be reviewed and approved by at least one other team member before merging. The CI/CD pipeline must pass successfully for a PR to be merged.

## Governance

This constitution is the authoritative guide for the Docusaurus book generation project. All project-related activities must comply with these principles. Amendments to this constitution require a PR, documented justification, and team approval, after which the version will be updated according to semantic versioning rules.

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06