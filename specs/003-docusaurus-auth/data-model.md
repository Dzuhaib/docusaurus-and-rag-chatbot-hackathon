# Data Model: Docusaurus Authentication

**Purpose**: To define the data structures and concepts related to user authentication and content restriction within the Docusaurus site.

## Core Entities

### 1. User
- **Description**: An authenticated individual who can access restricted content. Netlify Identity manages user profiles.
- **Attributes**:
    - `id`: Unique identifier for the user (from Netlify Identity).
    - `email`: User's email address.
    - `jwt`: JSON Web Token, used to prove authentication and maintain session. Stored securely in browser local storage by Netlify Identity.
    - `roles`: (Optional) User roles for fine-grained access control (managed by Netlify Identity or custom claims).
- **Implementation**: Managed externally by Netlify Identity. Docusaurus will interact with the `netlify-identity-widget` and `netlify-identity-client` to retrieve current user status.

### 2. Restricted Content
- **Description**: Any Docusaurus page, chapter, or section designated to be accessible only by authenticated users.
- **Attributes**:
    - `path`: The Docusaurus URL path of the restricted content (e.g., `/docs/chapter1/subchapter1`).
    - `access_level`: (Optional) Defines which roles can access this content (e.g., `authenticated`, `admin`).
- **Implementation**: Marked within Docusaurus Markdown frontmatter (e.g., `restricted: true`) or configured via Docusaurus plugins/components that intercept routing. Protection will be client-side.

## Interaction Flow (High-Level)

1.  **User attempts to access `restricted_page.md`**.
2.  Docusaurus `AuthWrapper` component (or similar logic) checks authentication status using `netlify-identity-client`.
3.  **If authenticated**: Content is rendered.
4.  **If unauthenticated**: User is redirected to a login page/widget, or an access denied message is shown.
5.  **Login/Logout**: Handled by the Netlify Identity widget.

## Data Flow

- User credentials are sent directly to Netlify Identity.
- Netlify Identity returns a JWT.
- JWT is stored by `netlify-identity-widget` in browser's local storage.
- Docusaurus client-side code reads JWT/user status from local storage via `netlify-identity-widget` methods.
