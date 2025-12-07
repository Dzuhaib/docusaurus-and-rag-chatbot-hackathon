# Tasks: Docusaurus Authentication

**Input**: Design documents from `/specs/003-docusaurus-auth/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Phase 1: Setup (Netlify Identity Integration)

**Purpose**: Integrate Netlify Identity widget and prepare Docusaurus for authentication.

- [X] T001 Install `netlify-identity-widget` in `book-site/`: `npm install netlify-identity-widget`.
- [X] T002 Create `book-site/plugins/netlify-identity.js` to inject the Netlify Identity widget script.
- [X] T003 Configure `book-site/docusaurus.config.js` to register the `netlify-identity.js` plugin.
- [X] T004 Create `book-site/static/admin/index.html` for Netlify Identity admin UI.
- [X] T005 Set up Netlify Identity service on Netlify site (manual step, document in quickstart).

---

## Phase 2: Foundational (Authentication UI & Logic)

**Purpose**: Implement the core UI elements and client-side logic for authentication.

- [X] T006 Create `book-site/src/theme/Navbar/Content/index.js` to override Docusaurus Navbar.
- [X] T007 Implement login/logout buttons and user status display in `book-site/src/theme/Navbar/Content/index.js` using `netlify-identity-widget`.
- [X] T008 Create `book-site/src/components/AuthWrapper.js` component to handle content protection logic.
- [X] T009 Implement logic in `AuthWrapper.js` to check user authentication status using `netlify-identity-widget.currentUser()`.
- [X] T010 Implement client-side redirection to a login page or display a restricted message in `AuthWrapper.js` if unauthenticated.
- [X] T011 Create `book-site/src/pages/login.js` as a simple page that triggers the Netlify Identity widget's login modal.

---

## Phase 3: User Story 1 - Restrict Content Access (Priority: P1) 🎯 MVP

**Goal**: Enable marking and protecting specific Docusaurus content.
**Independent Test**: Verify unauthenticated users are blocked from restricted pages, and authenticated users can access them.

### Implementation for User Story 1

- [X] T012 Update Docusaurus docs to include `restricted: true` in the frontmatter of a sample page (e.g., `book-site/docs/chapter1/subchapter1.md`).
- [X] T013 Integrate `AuthWrapper.js` around the content of the restricted page, or implement a Docusaurus-specific way to apply the wrapper globally based on frontmatter. (This might involve overriding theme components or creating a custom DocItem wrapper).
- [X] T014 Ensure `AuthWrapper.js` correctly reads the `restricted` frontmatter from the page context.

---

## Phase 4: User Story 2 & 3 - Login/Logout Functionality (Priority: P1)

**Goal**: Provide functional user login and logout mechanisms.
**Independent Test**: Users can successfully log in and log out, and their authentication state is correctly reflected.

### Implementation for User Story 2 & 3

- [X] T015 Ensure login button in Navbar `T007` triggers `netlify-identity-widget.open()`.
- [X] T016 Ensure logout button in Navbar `T007` triggers `netlify-identity-widget.logout()`.
- [X] T017 Implement logic to update Navbar UI (e.g., show "Welcome, [User]" and a logout button) on Netlify Identity events (login, logout, init).

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final testing, documentation, and minor improvements.

- [X] T018 Update `book-site/src/css/custom.css` with styling for login/logout buttons and restricted content messages.
- [X] T019 Update `quickstart.md` with detailed instructions on setting up Netlify Identity, deploying to Netlify, and managing users.
- [X] T020 Manual testing of login, logout, and restricted content access flows.

---

## Dependencies & Execution Order

- **Setup (Phase 1)**: Must be completed first.
- **Foundational (Phase 2)**: Depends on Setup.
- **User Story 1 (Phase 3)**: Depends on Foundational.
- **User Story 2 & 3 (Phase 4)**: Depends on Foundational.
- **Polish (Phase 5)**: Depends on all other phases being complete.

## Implementation Strategy

### MVP First (User Story 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2 & 3 (Login/Logout)
5. **STOP and VALIDATE**: Core authentication (login, logout, restricted content access) is functional.

### Incremental Delivery

1. Deliver MVP (basic login/logout, content restriction).
2. Complete Phase 5 (testing and polish).
