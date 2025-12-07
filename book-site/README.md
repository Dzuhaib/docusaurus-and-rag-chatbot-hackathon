# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
yarn
```

## FastAPI Backend

To run the FastAPI backend, navigate to the `backend` directory and execute the following commands. The backend serves the RAG functionality and the Chatkit integration endpoints.

```bash
cd ../backend
uvicorn src.qdrant_indexer.api:app --reload
```

This command starts the FastAPI server. Ensure you have the required Python packages installed (`pip install -r requirements.txt`).

## Local Development (Docusaurus Frontend with Chatkit)

First, ensure the FastAPI backend is running as described above.

Then, to start the Docusaurus frontend:

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server. The OpenAI Chatkit widget should appear as a floating icon on the bottom right of the pages. Interact with it to query the RAG backend.


## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
