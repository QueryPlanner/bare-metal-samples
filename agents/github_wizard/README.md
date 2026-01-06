# GitHub Wizard Agent

The **GitHub Wizard** is a specialized agent designed to assist with GitHub-related tasks using the Model Context Protocol (MCP).

## Features

- **GitHub Integration**: Connects to GitHub using the GitHub Copilot MCP server.
- **Task Assistance**: Helps answer questions and perform actions related to GitHub repositories, issues, and pull requests.

## Configuration

To use this agent, you must provide a valid GitHub token.

1.  Obtain a GitHub Personal Access Token (PAT) with appropriate permissions.
2.  Set the `GITHUB_TOKEN` environment variable in your `.env` file or environment.

```env
GITHUB_TOKEN=your_github_token_here
```

## Tools

- **GitHub MCP Tools**: Automatically loaded if `GITHUB_TOKEN` is present.
