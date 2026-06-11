# acli — extended command reference

Verified against acli 1.3.19-stable. Flags listed are the useful subset; `--help` on any command shows the full set. The agent rules from SKILL.md (long-form flags, `--yes` on destructive commands, `--json` for parsing) apply throughout.

## Jira projects

```bash
acli jira project list --recent              # up to 20 recently viewed
acli jira project list --paginate --json     # all projects (--limit ignored with --paginate)
acli jira project view --key "TEAM" --json
```

Create clones an existing **company-managed** project or builds from JSON (no template flag exists):

```bash
acli jira project create --from-project "TEAM" --key "NEWTEAM" --name "New Project" \
  --description "..." --url "https://example.com" --lead-email "user@example.com"
acli jira project create --generate-json && acli jira project create --from-json project.json
```

Update targets the project with `--project-key`; `--key` sets a NEW key (rename):

```bash
acli jira project update --project-key "TEAM" --name "Renamed" --lead-email "user@example.com"
acli jira project archive --key "TEAM"       # also: restore, delete (permanent)
```

## Jira boards

```bash
acli jira board search --project "TEAM" --json         # also --name, --type scrum|kanban|simple,
                                                       # --filter <id>, --limit, --paginate, --csv
acli jira board view --id <boardId> --json
acli jira board list-projects --id <boardId> --json
acli jira board list-sprints --id <boardId> --state active --json   # states: future, active, closed (comma-separated)
acli jira board create --name "My Board" --type "scrum" --filter-id 10040 --location-type "project" --project "TEAM"
acli jira board delete --id "<id1>,<id2>" --yes
```

Board IDs are numeric — find them via `board search`. `--location-type user` creates a personal board (omit `--project`).

## Jira sprints

```bash
acli jira sprint create --board <boardId> --name "Sprint 43" --goal "Ship the thing" \
  --start 2026-06-15 --end 2026-06-29 --json          # dates ISO 8601
acli jira sprint view --id <sprintId> --json
acli jira sprint update --id <sprintId> --state active            # future|active|closed; also --name, --goal, --start, --end
acli jira sprint list-workitems --board <boardId> --sprint <sprintId> --json   # both IDs required
acli jira sprint list-workitems --board <boardId> --sprint <sprintId> --jql "type = Bug" --fields "key,summary,status"
acli jira sprint delete --id <sprintId> --yes
```

Starting or closing a sprint = `sprint update --state active|closed`. There is no command to move work items into a sprint — set the sprint on the work item instead (custom field via `workitem edit --from-json`) or ask the user to do it in the UI.

## Jira filters

```bash
acli jira filter list --my                   # or --favourite
acli jira filter search --name "report" --owner user@example.com --json   # also --limit, --paginate, --csv
acli jira filter view --id 12345 --json      # --web opens the filter's search in browser
acli jira filter update --id 12345 ...       # see --help; edits name/jql/description
acli jira filter add-favourite --id 12345
acli jira filter change-owner --id 12345 ...
acli jira filter list-columns --id 12345     # and reset-columns
```

Saved filter IDs plug into work item commands via `--filter <id>`.

## Jira dashboards and fields

```bash
acli jira dashboard search --name "team" --owner user@example.com --json   # search is the only dashboard command
acli jira field create ...                   # custom fields: create, update, delete (to trash), restore
```

Field commands are admin-ish and rarely needed — check `--help` before use.

## Confluence

Confluence coverage is thin compared to Jira. Pages are **read-only** (view only — no page create/edit):

```bash
acli confluence page view --id <pageId> --json --body-format storage   # storage | atlas_doc_format | view
acli confluence space list --json            # --keys, --type global|personal, --status current|archived
acli confluence space view --id <spaceId> --include-all --json
acli confluence blog list --space-id <id> --json     # cursor pagination: --cursor <token from previous page>
acli confluence blog view --id <blogId> --json
acli confluence blog create --space-id <id> --title "Post" --body "<p>XHTML storage format</p>"
```

`blog create --body` takes Confluence storage format (XHTML), not ADF or Markdown; `--from-file` accepts plain text or HTML. Space create/update/archive/restore also exist.

Confluence auth is separate from Jira: `acli confluence auth status` / `login`.

## Auth, admin, config

```bash
acli auth status                             # global OAuth status across products
acli auth login                              # global OAuth (browser; no flags)
acli auth switch --site mysite.atlassian.net --email user@example.com
```

Per-product auth (`acli jira auth ...`, `acli confluence auth ...`) supports `--web` OAuth or site/email/token — `--token` reads from STDIN (see SKILL.md).

Admin commands manage org users and need an admin API key (admin.atlassian.com → Settings → API keys):

```bash
echo "$ADMIN_KEY" | acli admin auth login --email admin@example.com --token
acli admin user activate|deactivate|delete|cancel-delete ...
```

`acli config gov-cloud --enable|--status` toggles Atlassian Government Cloud mode. `acli rovodev` (Rovo Dev AI agent, Beta) requires its own scoped token via `acli rovodev auth login`; all its commands error until then.
