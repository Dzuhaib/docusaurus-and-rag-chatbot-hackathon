# Quickstart: Docusaurus Book Site

**Purpose**: This guide provides instructions on how to set up the development environment and run the Docusaurus project locally.

## Prerequisites

- **Node.js**: Version 18.x or higher. You can download it from [nodejs.org](https://nodejs.org/).
- **npm**: Comes bundled with Node.js.

## Setup & Installation

1.  **Navigate to the project directory**:
    ```bash
    cd book-site
    ```

2.  **Install dependencies**:
    This command will download and install all the necessary packages defined in `package.json`.
    ```bash
    npm install
    ```

## Running the Development Server

1.  **Start the local server**:
    This command starts a local development server with hot-reloading.
    ```bash
    npm run start
    ```

2.  **View the site**:
    Open your web browser and navigate to **http://localhost:3000**.

The site will automatically reload if you make changes to the source files.

## Building the Static Site

To create a production-ready static build of the website, run the following command:

```bash
npm run build
```

The output will be placed in the `book-site/build` directory. This is the directory that will be deployed to GitHub Pages.
