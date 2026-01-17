# COREcare-access Project Guidelines

## Engineering Committee ("eng-committee")

When asked to "convene the eng committee", assemble the following expert personas to provide a critical review (pros/cons/recommendations):

### Committee Members

1. **Senior SRE** (15 years): Expert in reliability, error budgets (SLIs/SLOs), and automated toil reduction via K8s/Terraform.

2. **Senior Software Engineer** (15 years): Expert in distributed systems, clean code, and API integrity.

3. **System Architect** (15 years): Expert in microservices, event-driven design, and the CAP theorem.

4. **UX Designer** (15 years): Accessibility expert (WCAG) and reducing user cognitive load.

5. **Principal Application Security Engineer** (15 years): Expert in "shifting left," threat modeling, and pragmatic risk mitigation.

6. **Principal AI/ML Engineer** (15 years): Expert in RAG, model latency, and managing the nondeterministic nature of GenAI.

7. **Principal Data Engineer** (15 years): Expert in schema evolution, ETL pipelines, and data observability.

### The Judge (Principal Engineer)

A 20-year veteran who has occupied every seat at this table. Expert in systems thinking and Total Cost of Ownership (TCO). They synthesize the committee's feedback to resolve multidimensional conflicts (e.g., "Model Accuracy vs. Inference Latency" or "Data Depth vs. Privacy Compliance"). Their final plan moves beyond technical "correctness" to prioritize business outcomes, operational sustainability, and the mitigation of technical debt.

### Process

1. Each committee member provides their critical review
2. The Judge synthesizes all feedback into a final, unified plan
3. The plan balances technical elegance with business impact, TCO, and long-term maintainability

## Available MCP Servers

The following MCP (Model Context Protocol) servers are configured and available for all AI models working on this project:

### Render MCP Server
- **URL**: `https://mcp.render.com/mcp`
- **Status**: ✓ Connected
- **Use Cases**:
  - Check deployment status of commits
  - Monitor production environment health
  - Trigger redeployments when needed
  - View build logs and error details
  - Query environment variables and configuration

**Example Usage**:
```bash
# Check if a specific commit is deployed in production
# Check deployment status and logs
# Trigger a redeploy after pushing changes
```

All AI models should leverage this MCP server when working on deployment-related tasks, debugging production issues, or verifying that code changes have been successfully deployed.

### GitHub MCP Server
- **URL**: `https://api.githubcopilot.com/mcp`
- **Status**: ✓ Connected
- **Use Cases**:
  - Create, read, and manage GitHub issues
  - Manage pull requests (create, review, merge)
  - Search repositories and code
  - Manage GitHub projects and milestones
  - View repository information and commits
  - Manage issue labels, assignments, and projects
  - Access repository workflows and actions

**Example Usage**:
```bash
# Search for issues across the repository
# Create or update issues programmatically
# Fetch PR details and manage review workflows
# Query commit history and branch information
```

All AI models should leverage this MCP server when working with GitHub issues, pull requests, project management, and code search tasks. This enables automated issue creation, PR reviews, and project tracking directly from AI agents.

## How MCP Servers Work

MCP (Model Context Protocol) servers are **automatically discovered and invoked by Claude Code** when an AI model needs access to their capabilities. You don't need to manually call MCP tools—instead:

1. **Claude Code discovers available MCP tools** at startup from configured servers
2. **When an AI model asks for information** that a tool can provide (e.g., "check deployment status"), Claude Code automatically invokes the appropriate tool
3. **Results are returned transparently** to the AI model without requiring explicit tool calls

### MCP Tool Discovery
- Tools are discovered from servers listed in `claude mcp list`
- Available tools depend on the MCP server's implementation
- Tools are invoked transparently when the AI model's request matches what they provide

### Render MCP Server Available Tools
Key tools available from Render MCP include:
- `list_deploys` - Retrieve deployment history and status
- `get_deploy` - Get details for a specific deployment
- `list_services` - View all services
- `get_metrics` - Retrieve CPU, memory, and HTTP metrics
- `list_logs` - Access logs with filters by time, level, type
- `list_postgres_instances` - View all databases

### GitHub MCP Server Available Tools
Key tools available from GitHub MCP include:
- `list_issues` - Search and filter issues in the repository
- `create_issue` - Automatically create issues with title, body, labels
- `get_pull_request` - Retrieve PR details
- `list_pull_requests` - Search PRs by status, author, reviewer
- `create_pull_request` - Programmatically create PRs

### How to Use MCP Tools
Simply request what you need in natural language:
- "Check the deployment status of the latest commit"
- "Create an issue for the bug we discussed"
- "List all open PRs waiting for review"
- "Get the CPU metrics for the last hour"

Claude Code will automatically locate and invoke the appropriate MCP tool to fulfill the request.
