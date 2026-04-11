# Product Roadmap

This project is evolving toward an API where users can submit workflows in JSON or text form and generate clear documentation for non-technical audiences.

## Current Direction

The current foundation already supports:
- authenticated users
- workflow creation and storage
- ownership-based access
- AI-generated documentation for workflows

The next goal is to make the product more reliable, more useful, and more clearly aligned with the core idea.

## Prioritized Features

### 1. JSON Validation and Structured Parsing

Make `input_type="json"` actually validate the submitted workflow payload.

Why it matters:
- directly supports the main product idea
- prevents invalid workflow submissions
- makes the platform feel more intentional and trustworthy

Suggested improvements:
- validate that JSON is well-formed
- reject invalid JSON with a clean API error
- optionally store parsed workflow data in a structured form later

### 2. Multiple Documentation Styles

Allow users to choose the type of documentation they want.

Why it matters:
- makes the AI feature much more useful
- better supports both technical and non-technical audiences
- creates a clearer product differentiator

Suggested output styles:
- `non_technical`
- `technical`
- `summary`
- `step_by_step`

### 3. Structured Documentation Output

Store generated documentation in a cleaner format instead of one long generic text block.

Why it matters:
- improves readability
- makes future frontend work easier
- supports better exports and richer UI later

Suggested structure:
- overview
- step-by-step explanation
- business purpose
- key inputs and outputs
- risks or assumptions

### 4. Workflow Update Endpoint

Let users edit workflows after creation.

Why it matters:
- workflows change often
- users should not need to recreate records for every fix
- makes regeneration of docs much more practical

Suggested endpoint:
- `PUT /workflows/{id}` or `PATCH /workflows/{id}`

### 5. Regenerate Documentation

Allow users to regenerate docs after changing a workflow or selecting a different audience/style.

Why it matters:
- users will iterate on both workflow content and documentation quality
- makes the product feel alive rather than one-time only

Good first version:
- replace the existing documentation with a newly generated version

Better later version:
- keep documentation history

### 6. Better AI Error Handling

Improve responses when generation fails.

Why it matters:
- gives users clearer feedback
- makes production use less frustrating
- improves API quality without major complexity

Suggested cases:
- invalid workflow JSON
- unsupported input format
- model/provider failure
- timeout or empty response

### 7. Workflow Search, Filtering, and Pagination

Make it easier to manage many workflows.

Why it matters:
- improves usability as the project grows
- adds real product polish

Suggested additions:
- pagination
- search by title
- filter by input type
- sort by created date

### 8. Workflow Metadata

Add a few useful metadata fields.

Why it matters:
- increases product realism
- makes workflows easier to organize

Suggested fields:
- description
- tags
- source
- last_generated_at
- status

### 9. Export and Sharing

Let users download generated documentation.

Why it matters:
- makes the output actually usable outside the app
- adds practical value with moderate effort

Suggested formats:
- Markdown
- plain text
- PDF later

### 10. Background Documentation Generation

Move documentation generation into a job-based process.

Why it matters:
- better scalability
- avoids long blocking requests
- looks strong on a resume

Suggested status model:
- `pending`
- `completed`
- `failed`

### 11. Version History

Track changes to workflows and documentation.

Why it matters:
- useful for real users
- strong SaaS signal
- good long-term product feature

This is valuable, but not essential for the next phase.

### 12. Team and Workspace Support

Allow multiple users to collaborate inside shared workspaces.

Why it matters:
- high SaaS value
- strong resume signal
- opens the door to role-based access and B2B use cases

This is a later-stage feature and not necessary right now.

## Best Next 5 Features

If the goal is maximum value without overbuilding the project yet, focus on these first:

1. JSON validation and parsing
2. Multiple documentation styles
3. Structured documentation output
4. Workflow update endpoint
5. Better AI error handling

## Resume Positioning

Once those features are added, the project can be described as:

"An AI-powered API that converts workflow definitions into audience-specific documentation, with authenticated users, workflow storage, validation, and AI-generated explanations for non-technical stakeholders."

## Later SaaS Direction

If this grows into a bigger product, the strongest next steps would be:
- background jobs
- exports and sharing
- version history
- API keys
- team workspaces
