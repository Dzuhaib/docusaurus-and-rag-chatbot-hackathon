# Data Model: Book Content Structure

**Purpose**: To define the structure and entities for the book's content. As this is a static site, this model describes the organization of Markdown files rather than a database schema.

## Core Entities

### 1. Book
- **Description**: Represents the entire collection of the work. It is the root container for all chapters and pages.
- **Attributes**:
    - `title`: The main title of the book.
    - `introduction`: The entry content for the book.
- **Implementation**: Managed via `docusaurus.config.js` and the `docs/intro.md` file.

### 2. Chapter
- **Description**: A top-level section of the book, used to group related sub-chapters.
- **Attributes**:
    - `title`: The title of the chapter (e.g., "The Robotic Nervous System").
    - `position`: The numerical order of the chapter in the sidebar.
- **Implementation**: A directory within `/docs` (e.g., `/docs/chapter1`). The title and position are managed by a `_category_.json` file within the directory.

### 3. Sub-Chapter
- **Description**: A specific content page within a Chapter. This is where the main text of the book resides.
- **Attributes**:
    - `title`: The title of the sub-chapter page.
- **Implementation**: A Markdown file (`.md`) within a chapter directory (e.g., `docs/chapter1/subchapter1.md`).

## Relationships

- A **Book** has one `introduction` and many `Chapters`.
- A **Chapter** has many `Sub-Chapters`.

## Example File Structure

```
docs/
├── intro.md
├── chapter1/
│   ├── _category_.json  # Contains title: "Chapter 1 Title", position: 1
│   ├── subchapter1.md
│   ├── subchapter2.md
│   └── subchapter3.md
└── chapter2/
    ├── _category_.json  # Contains title: "Chapter 2 Title", position: 2
    ├── subchapter1.md
    ...
```
