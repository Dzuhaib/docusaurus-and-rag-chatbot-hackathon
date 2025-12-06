# Quickstart: Docusaurus Authentication with Netlify Identity

**Purpose**: This guide provides instructions on how to set up Netlify Identity and configure your Docusaurus site for authentication.

## Prerequisites

- **Netlify Account**: You need a Netlify account and a site deployed on Netlify.
- **Netlify Identity Enabled**: Identity must be enabled for your Netlify site.
- **Docusaurus Project**: Your `book-site` project deployed to Netlify.

## Setup & Configuration

### 1. Enable Netlify Identity in your Netlify Site

1.  Go to your site in the Netlify UI.
2.  Navigate to **Site settings > Identity**.
3.  Click **Enable Identity**.
4.  Under **Registration**, choose "Open" or "Invite only" based on your preference.
5.  Optionally, configure external providers (Google, GitHub, etc.) if desired.

### 2. Add Netlify Identity Widget to Docusaurus

1.  **Install Netlify Identity Widget**:
    ```bash
    cd book-site
    npm install netlify-identity-widget
    ```

2.  **Create a Docusaurus Plugin (or use a theme component override)**:
    A common way to integrate client-side scripts is via a custom Docusaurus plugin or by injecting a script. For Netlify Identity, the widget needs to initialize globally.

    *   **Option A: Custom Plugin (Recommended for cleaner code)**:
        Create `book-site/plugins/netlify-identity.js`:
        ```javascript
        // book-site/plugins/netlify-identity.js
        module.exports = function (context, options) {
          return {
            name: 'netlify-identity-plugin',
            injectHtmlTags() {
              return {
                headTags: [
                  {
                    tagName: 'script',
                    attributes: {
                      src: 'https://identity.netlify.com/v1/netlify-identity-widget.js',
                    },
                  },
                ],
                postBodyTags: [
                  {
                    tagName: 'script',
                    innerHTML: `
                      if (window.netlifyIdentity) {
                        window.netlifyIdentity.on("init", user => {
                          if (!user) {
                            window.netlifyIdentity.on("login", () => {
                              document.location.href = "/admin/";
                            });
                          }
                        });
                      }
                    `,
                  },
                ],
              };
            },
          };
        };
        ```
        Then, add this plugin to `book-site/docusaurus.config.js`:
        ```javascript
        // docusaurus.config.js
        plugins: [
          // ... other plugins
          './plugins/netlify-identity',
        ],
        ```

    *   **Option B: Direct Script in `docusaurus.config.js` (Less ideal for complex logic)**:
        Add the script tag directly to `headTags` in `docusaurus.config.js`.

### 3. Implement Login/Logout UI

You'll typically create a custom Navbar item to display login/logout buttons or user status.
*   Override `book-site/src/theme/Navbar/Content/index.js` (or a similar component) to add Netlify Identity buttons.

### 4. Protect Content

Mark pages as restricted in their frontmatter, then use a component override (e.g., `AuthWrapper.js`) in your theme to check authentication status.
*   **Example page frontmatter**:
    ```markdown
    ---
    title: Restricted Page
    restricted: true
    ---
    ```
*   Implement `AuthWrapper.js` to:
    - Check `window.netlifyIdentity.currentUser()` for authentication status.
    - If unauthenticated, redirect or display a message.

### 5. Netlify Identity Admin UI (Optional)

If you need a Netlify Identity admin dashboard:
1.  Create `book-site/static/admin/` directory.
2.  Create `book-site/static/admin/index.html` with a basic HTML file that loads the Netlify Identity widget.
    ```html
    <!DOCTYPE html>
    <html>
    <head>
      <title>Netlify Identity</title>
      <script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
    </head>
    <body>
      <script>
        if (window.netlifyIdentity) {
          window.netlifyIdentity.on("init", user => {
            if (!user) {
              window.netlifyIdentity.on("login", () => {
                document.location.href = "/admin/";
              });
            }
          });
        }
      </script>
    </body>
    </html>
    ```

## Deployment

Deploy your Docusaurus site to Netlify. Netlify Identity will automatically detect the widget and manage the authentication backend.
