# Tasks: Qdrant Vector Database Integration

**Input**: Design documents from `/specs/002-qdrant-vector-db/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Phase 1: Setup (Project Initialization)

**Purpose**: Create the basic project structure and environment for the Qdrant indexer.

- [X] T001 Create the `backend/` directory at the project root.
- [X] T002 Create the `backend/src/qdrant_indexer/` directory.
- [X] T003 Create `backend/src/qdrant_indexer/__init__.py`.
- [X] T004 Create `backend/requirements.txt` with initial dependencies: `qdrant-client`, `fastembed`, `markdown-it-py`, `python-dotenv`, `typer`.
- [X] T005 Create `backend/.env.example` file with placeholders for Qdrant and Gemini API keys/URLs.

---

## Phase 2: Foundational (Qdrant & Embeddings Services)

**Purpose**: Implement the core services for interacting with Qdrant and generating embeddings.

- [X] T006 Implement `backend/src/qdrant_indexer/qdrant_service.py` with classes/functions for:
    - Initializing Qdrant client from environment variables.
    - Creating/managing Qdrant collections (ensure collection exists with correct vector size).
    - Upserting points (vectors + payload) to the collection.
    - Deleting points/collections.
- [X] T007 Implement `backend/src/qdrant_indexer/text_processor.py` with classes/functions for:
    - Reading Markdown files (`.md`, `.mdx`).
    - Robustly chunking text to preserve semantic context (e.g., based on headings, paragraph breaks).
    - Extracting metadata from Docusaurus file paths and frontmatter (chapter, subchapter, URL).
    - Generating unique `chunk_id` for each chunk.
- [X] T008 Implement embedding generation within `text_processor.py` (or a separate module) using `fastembed` for Google Gemini Embeddings.
    - Handle API key loading.
    - Ensure correct embedding model is used.

---

## Phase 3: User Story 1 - Index Book Content (Priority: P1) 🎯 MVP

**Goal**: Enable initial indexing of all Docusaurus book content into Qdrant.
**Independent Test**: Execute the indexing CLI command, then query Qdrant to confirm content is present and searchable.

### Implementation for User Story 1

- [X] T009 Implement `backend/src/qdrant_indexer/main.py` as the CLI entry point using `typer`.
- [X] T010 Add an `index` command to `main.py` that takes `docs-path` and `collection-name` as arguments.
- [X] T011 Orchestrate the `index` command to:
    - Iterate through Markdown files in `docs-path`.
    - Use `text_processor.py` to chunk content and extract metadata.
    - Generate embeddings for each chunk.
    - Use `qdrant_service.py` to create/update the Qdrant collection and upsert the points.
- [X] T012 Implement robust error handling and logging for the indexing process.

---

## Phase 4: User Story 2 - Re-index Updated Content (Priority: P2)

**Goal**: Allow efficient re-indexing of content when Docusaurus documentation changes.
**Independent Test**: Modify a doc, re-run the indexer, and verify Qdrant reflects the changes correctly without duplicates.

### Implementation for User Story 2

- [X] T013 Ensure `qdrant_service.py`'s upsert logic correctly handles updates for existing `chunk_id`s (Qdrant points IDs).
- [X] T014 Implement logic in `main.py` to identify deleted files/chunks and remove them from Qdrant during re-indexing (optional, but good for cleanup).

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final testing, documentation, and minor improvements.

- [X] T015 Write unit tests for `qdrant_service.py` in `backend/tests/test_qdrant_service.py`.
- [X] T016 Write unit tests for `text_processor.py` in `backend/tests/test_text_processor.py`.
- [X] T017 Write integration tests for `main.py` (e.g., testing the full indexing flow) in `backend/tests/test_main.py`.
- [X] T018 Update `quickstart.md` with any final instructions or best practices discovered during implementation.
- [X] T019 Ensure all sensitive information (API keys) are loaded securely from environment variables.

---

## Dependencies & Execution Order

- **Setup (Phase 1)**: Must be completed first.
- **Foundational (Phase 2)**: Depends on Setup.
- **User Story 1 (Phase 3)**: Depends on Foundational.
- **User Story 2 (Phase 4)**: Depends on Foundational. Can be implemented concurrently with or after Phase 3.
- **Polish (Phase 5)**: Depends on all other phases being complete.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: The indexing script runs and populates Qdrant.

### Incremental Delivery

1. Deliver MVP (basic indexing).
2. Implement Phase 4 (re-indexing for updates).
3. Complete Phase 5 (testing and polish).
