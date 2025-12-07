# Tasks: Create Docusaurus Book

**Input**: Design documents from `/specs/001-create-docusaurus-book/`
**Prerequisites**: plan.md, spec.md

## Phase 1: Setup

**Purpose**: Initialize the Docusaurus project structure.

- [X] T001 Initialize a new Docusaurus site named `book-site` using `npx create-docusaurus@latest book-site classic`.
- [X] T002 Navigate into the new `book-site` directory.
- [X] T003 Install all dependencies by running `npm install`.

---

## Phase 2: Foundational (Theming & Configuration)

**Purpose**: Configure the basic look and feel and metadata of the site. This must be done before adding content.

- [X] T004 [P] Update the site title, tagline, and URL in `book-site/docusaurus.config.js`.
- [X] T005 [P] Create the custom CSS file at `book-site/src/css/custom.css`.
- [X] T006 Implement the dark theme with electric blue accents in `book-site/src/css/custom.css` by overriding Docusaurus's default CSS variables.
- [X] T007 [P] Remove the default Docusaurus content from the `docs` and `blog` directories.

---

## Phase 3: User Story 1 - Landing Page (Priority: P1) 🎯 MVP

**Goal**: Create a custom, visually appealing landing page that introduces the book.
**Independent Test**: The root URL (e.g., `http://localhost:3000`) renders the new landing page instead of the default Docusaurus page.

### Implementation for User Story 1

- [X] T008 [US1] Create a new React component for the hero section in `book-site/src/components/HeroSection.js`.
- [X] T009 [US1] Create the custom landing page at `book-site/src/pages/index.js`, replacing the default.
- [X] T010 [US1] Integrate the `HeroSection` component into the `book-site/src/pages/index.js` landing page.
- [X] T011 [US1] Add a section to the landing page that will later contain links to the book chapters.

---

## Phase 4: User Story 2 & 3 - Book Content (Priority: P2)

**Goal**: Create the book's structure and populate it with placeholder content.
**Independent Test**: The "Docs" section of the website shows a sidebar with 3 chapters, each containing 3 sub-chapters, and all pages are accessible.

### Implementation for User Story 2 & 3

- [X] T012 [P] [US2] Create the main introduction file at `book-site/docs/intro.md` with content from the book outline summary.
- [X] T013 [P] [US2] Create the directory structure for 3 chapters inside `book-site/docs/` (e.g., `chapter1`, `chapter2`, `chapter3`).
- [X] T014 [P] [US2] Within each chapter directory, create 3 sub-chapter markdown files (e.g., `subchapter1.md`, etc.).
- [X] T015 [P] [US2] Add a `_category_.json` file to each of the 3 chapter directories.
- [X] T016 [US2] Configure each `_category_.json` file to set the chapter's title and `position` in the sidebar.
- [X] T017 [US2] Populate all sub-chapter markdown files with placeholder titles and content based on the book outline.
- [X] T018 [US2] Update `docusaurus.config.js` to ensure the sidebar is correctly generated from the `docs` directory structure.
- [X] T019 [US3] Add the links to the 3 main chapters to the landing page created in `T011`.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, cleanup, and deployment setup.

- [X] T020 [P] Verify that all internal links, including those on the homepage and in the sidebar, are working correctly.
- [X] T021 [P] Create a GitHub Actions workflow file at `.github/workflows/deploy.yml` to build and deploy the Docusaurus site to GitHub Pages.
- [X] T022 Review the entire site for any style inconsistencies or layout issues.

---

## Dependencies & Execution Order

- **Setup (Phase 1)**: Must be completed first.
- **Foundational (Phase 2)**: Depends on Setup.
- **User Story 1 (Phase 3)**: Depends on Foundational.
- **User Story 2 & 3 (Phase 4)**: Depends on Foundational. Can be worked on in parallel with US1, but the final linking task `T019` depends on `T011`.
- **Polish (Phase 5)**: Depends on all other phases being complete.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: The custom landing page is functional. The site can be deployed to show the initial landing page.

### Incremental Delivery

1. Deliver MVP.
2. Complete Phase 4 to add all the book content.
3. Complete Phase 5 to set up automated deployment.
