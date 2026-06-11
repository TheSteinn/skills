---
name: acli
description: Reference for the Atlassian CLI (acli) covering Jira and Confluence Cloud. Use whenever running acli commands or doing anything with Jira from the terminal — JQL searches, viewing/creating/editing work items (issues, tickets, bugs, stories, epics), transitions, comments, assignments, sprints, boards, filters, or Confluence pages and spaces. Trigger on mentions of "acli", "Jira CLI", "JQL", issue keys like PROJ-123, or any request to query, update, comment on, or transition Jira tickets.
---

# Atlassian CLI (acli)

`acli` is Atlassian's official CLI for Jira Cloud and Confluence Cloud. Top-level groups: `jira` (the bulk of functionality), `confluence`, `auth`, `admin`, `config`, `rovodev`.

Verified against acli 1.3.19-stable. The CLI evolves quickly — when a command here doesn't behave as documented, trust `acli <command> --help` over this file.

## Before you start

```bash
acli --version              # confirm installed
acli jira auth status       # confirm authenticated for Jira
```

If `acli` is not installed, stop and tell the user — do not install it yourself.

If not authenticated, ask the user to log in (both methods need their involvement):

```bash
acli jira auth login --web                                   # browser OAuth
# API token (https://id.atlassian.com/manage-profile/security/api-tokens).
# --token is a boolean flag that reads the token from STDIN — there is no --token <value> form:
echo "$TOKEN" | acli jira auth login --site "mysite.atlassian.net" --email "user@example.com" --token
```

Unauthenticated commands fail with `✗ Error: unauthorized` or `failed to retrieve authenticated status`.

`~/.config/acli/org-setup.md` records this org's site, project keys, board IDs, and workflow statuses — read it before working with any of those, and ask the user when something you need isn't recorded there. If the file doesn't exist, offer to create it from [references/org-setup-template.md](references/org-setup-template.md); it lives outside the skill directory so skill re-installs can't overwrite it.

## Rules that prevent broken commands

1. **Always use long-form flags.** Short flags change meaning between subcommands: `-j` is `--jql` on `workitem search` but `--json` on `project view`; `-l` is `--limit` on search but `--labels` on edit; `-f` is `--fields` on search but `--from-file` on assign/delete.
2. **Pass `--yes` on bulk or destructive commands** (edit, transition, assign, delete, clone with multiple targets). They prompt for confirmation otherwise, which hangs a non-interactive shell.
3. **Never use `--editor` or `-e`** flags — they open an interactive editor. Use `--body`/`--body-file`/`--description-file` instead.
4. **`workitem view` takes the key as a positional argument** (`view KEY-123`); nearly everything else uses `--key`.
5. **Default to `--json` on every command.** The default table output is styled, truncated, and limited to a small field set — unreliable to parse. On reads, pair `--json` with an explicit `--fields` list to keep output small; on mutations, `--json` returns a structured per-key result so you can verify a batch actually succeeded. `--json` is per-command, not global; `--csv` exists only on some search/list commands.
6. **Bulk targeting is interchangeable**: most work item commands accept `--key "KEY-1,KEY-2"`, `--jql "<query>"`, or `--filter <id>`. Add `--ignore-errors` to continue a batch past individual failures.

## Work items

Jira's CLI calls issues "work items" — the commands live under `acli jira workitem`.

### Search

```bash
acli jira workitem search --jql "project = TEAM AND assignee = currentUser() AND resolution = Unresolved"
acli jira workitem search --jql "project = TEAM" --fields "key,status,summary" --json
acli jira workitem search --jql "project = TEAM" --limit 50      # or --paginate for all results
acli jira workitem search --jql "project = TEAM" --count         # just the number
acli jira workitem search --filter 10001 --web                   # saved filter; open in browser
```

Default fields are `issuetype,key,assignee,priority,status,summary` — request anything else explicitly via `--fields`.

### View

```bash
acli jira workitem view KEY-123
acli jira workitem view KEY-123 --fields "summary,description,status,comment"
acli jira workitem view KEY-123 --fields "*all" --json
```

`--fields` accepts `*all`, `*navigable`, and minus-prefixed exclusions (`*navigable,-comment`).

### Create

```bash
acli jira workitem create --summary "New task" --project "TEAM" --type "Task"
acli jira workitem create --summary "Bug title" --project "TEAM" --type "Bug" \
  --description "Plain text or ADF" --assignee "@me" --label "bug,cli" --parent "TEAM-100"
```

Ask the user for the project key if it isn't known or recorded in `~/.config/acli/org-setup.md`. Assignee accepts an email, account ID, `@me`, or `default`. Note it's `--label` (singular) here but `--labels` on edit.

Only summary, project, type, description, assignee, labels, and parent are exposed as flags. **For priority, components, fix versions, reporter, or custom fields**, use the JSON path (`--generate-json` prints the full template):

```bash
acli jira workitem create --from-json workitem.json
```

```json
{
  "projectKey": "TEAM",
  "type": "Task",
  "summary": "Title",
  "description": {"type": "doc", "version": 1, "content": [
    {"type": "paragraph", "content": [{"type": "text", "text": "Description"}]}
  ]},
  "labels": ["feature"],
  "assignee": "user@example.com",
  "additionalAttributes": {
    "customfield_10089": {"value": "Select-field option"},
    "customfield_10001": 50,
    "customfield_10002": "plain string value"
  }
}
```

In JSON, `description` **must be ADF** — plain text is rejected. `type` is case-sensitive. Custom fields go under `additionalAttributes` keyed by field ID, with values shaped per field type: `{"value": ...}` for selects, bare numbers, bare strings. `reporter` and `parentIssueId` (sub-tasks) are also JSON-only.

For many items at once: `acli jira workitem create-bulk --from-json items.json` (array of objects) or `--from-csv items.csv` (columns: summary, projectKey, issueType, description, label, parentIssueId, assignee). Both support `--generate-json` to print an example.

### Edit

```bash
acli jira workitem edit --key "KEY-1" --summary "New title" --yes
acli jira workitem edit --key "KEY-1,KEY-2" --assignee "user@example.com" --yes
acli jira workitem edit --key "KEY-1" --description-file desc.txt --yes
acli jira workitem edit --key "KEY-1" --labels "bug,urgent" --remove-labels "wontfix" --yes
acli jira workitem edit --jql "project = TEAM AND labels = old" --labels "new" --yes
acli jira workitem edit --key "KEY-1" --remove-assignee --yes
```

`edit --from-json` (template via `edit --generate-json`) targets `"issues": [keys]` and supports `labelsToAdd`/`labelsToRemove`, but has no `additionalAttributes` — **custom fields can only be set at create time**.

### Assign

```bash
acli jira workitem assign --key "KEY-1" --assignee "@me" --yes
acli jira workitem assign --jql "project = TEAM AND assignee IS EMPTY" --assignee "default" --yes
```

### Transition

```bash
acli jira workitem transition --key "KEY-1" --status "In Progress" --yes
acli jira workitem transition --key "KEY-1,KEY-2" --status "Done" --yes
acli jira workitem transition --jql "project = TEAM AND labels = ready" --status "Done" --yes
```

`--status` is the target status **name** (not the transition name). There is no flag for setting resolution or other screen fields during the transition.

Workflows are org-specific and **acli has no command to list available transitions**. Check `~/.config/acli/org-setup.md` for this org's documented statuses; if the target isn't recorded there, ask the user to confirm the exact status name — don't guess, enumerate, or probe with trial transitions. Once confirmed, suggest the user adds it to org-setup.md.

### Comments

```bash
acli jira workitem comment create --key "KEY-1" --body "Comment text"
acli jira workitem comment create --key "KEY-1" --body-file comment.txt
acli jira workitem comment create --key "KEY-1" --edit-last --body "Replaces my last comment"
acli jira workitem comment list --key KEY-1 --json            # --order created|updated, --paginate
acli jira workitem comment update --key KEY-1 --id 10001 --body "Updated text"
acli jira workitem comment delete --key KEY-1 --id 10023
```

Pitfalls in acli's own help text: the `comment create` examples omit the `create` subcommand, and the `comment delete` example shows `--issue` — the real flag is `--key`. Visibility flags (`--visibility-role`, `--visibility-group`, `--notify`) exist only on `comment update`; `create` uses the project default. `comment visibility` lists the available roles/groups.

### Links

```bash
acli jira workitem link create --out KEY-123 --in KEY-456 --type Blocks --yes
acli jira workitem link list --key KEY-123 --json
acli jira workitem link type --json                   # available link types
acli jira workitem link delete --id <link-id> --yes
```

`--type` accepts the outward description, so `--out A --in B --type Blocks` means "A blocks B". Bulk linking: `--from-json` with `[{"outwardIssue": "A-1", "inwardIssue": "B-2", "type": "Blocks"}]` or `--from-csv` (columns: outward, inward, type).

### Attachments, watchers, lifecycle

```bash
acli jira workitem attachment list --key KEY-123 --json
acli jira workitem attachment delete --id 12345        # attachment ID from list; no --key
acli jira workitem list-watchers --key KEY-123 --json
acli jira workitem watcher remove --key KEY-123 --user <accountId>   # account ID, not email
acli jira workitem clone --key "KEY-1" --to-project "OTHER" --yes    # --to-site for cross-site
acli jira workitem archive --key "KEY-1" --yes         # and unarchive
acli jira workitem delete --key "KEY-1" --yes          # permanent; prefer archive
```

There is no attachment upload/download command, and no `watcher add` — adding watchers isn't supported.

## JQL quick reference

Wrap the JQL in double quotes for the shell; single-quote values with spaces inside it.

- Operators: `=`, `!=`, `AND`, `OR`, `NOT`, `IN`, `IS`, `IS NOT`, `~` (contains), `ORDER BY`
- Functions: `currentUser()`, `now()`, `startOfDay()`, `endOfWeek()`, relative dates like `-7d`
- `statusCategory` (`To Do`, `In Progress`, `Done`) is workflow-agnostic — prefer it over exact status names when the workflow is unknown
- If the shell mangles `!` (interactive history expansion), use `NOT x = y` instead of `x != y`

```sql
project = TEAM AND assignee = currentUser() AND resolution = Unresolved
project = TEAM AND statusCategory = 'In Progress'
project = TEAM AND updated >= -7d ORDER BY updated DESC
project = TEAM AND Sprint = 'Sprint 42'
project = TEAM AND summary ~ 'login' AND type = Bug
project = TEAM AND priority IN (High, Highest) AND status != Done
project = TEAM AND type = Bug AND created >= startOfWeek()
```

## Descriptions, comments, and ADF

`--description`, `--body`, and their `-file` variants accept plain text or Atlassian Document Format (ADF JSON) — the CLI auto-detects which. Markdown is **not** supported and will appear as literal text.

For multi-paragraph or structured content, use ADF:

```json
{"version":1,"type":"doc","content":[
  {"type":"paragraph","content":[{"type":"text","text":"First paragraph"}]},
  {"type":"bulletList","content":[{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"Item one"}]}]}]},
  {"type":"codeBlock","attrs":{"language":"python"},"content":[{"type":"text","text":"def hello():\n    print('hi')"}]}
]}
```

```bash
acli jira workitem comment create --key KEY-1 --body-file comment.json
```

Reported limitations (third-party observation, not in official docs — verify if it matters): plain-text `\n` may not render as paragraph breaks, and some ADF nodes (headings, bold/italic marks, code-block syntax highlighting) may be stripped or rejected. Paragraphs, lists, and plain code blocks are safe.

## Other command groups

Projects, boards, sprints, filters, dashboards, fields, Confluence, and admin commands are covered in [references/extended-commands.md](references/extended-commands.md) — read it when the task involves those. The most common ones:

```bash
acli jira project list --recent                # or --paginate for all
acli jira project view --key "TEAM" --json
acli jira board search --project "TEAM" --json
acli jira board list-sprints --id <boardId> --state active --json
acli jira sprint list-workitems --board <boardId> --sprint <sprintId> --json
```

## Deprecated commands — do not use

Deprecated 2026-05-13, removal scheduled 2026-12-01:

| Deprecated | Use instead |
|---|---|
| `jira board get` | `jira board view` |
| `jira workitem watcher list` | `jira workitem list-watchers` |
| `jira filter get` | `jira filter view` |
| `jira filter get-columns` | `jira filter list-columns` |
| `jira field cancel-delete` | `jira field restore` |

## Error handling

- `unauthorized` → run `acli jira auth status`; have the user log in (see Before you start)
- JQL errors → check quoting and field names; test the query with `--count` first
- Transition errors → target status not reachable from current status in the workflow
- Batch partially failing → add `--ignore-errors` to process the rest, then report which failed
- Unsure of exact syntax → `acli <command> --help` is always available offline
