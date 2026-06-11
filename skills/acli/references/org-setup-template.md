# Org-specific Jira/Confluence setup — template

Template for `~/.config/acli/org-setup.md`: the user-maintained record of this org's Atlassian specifics — things acli cannot discover (workflow statuses, conventions) or that are tedious to re-look-up (board IDs, project keys). The real file lives outside the skill directory so skill re-installs never touch it, while this template ships with the skill and may evolve — when updating the org file, check whether the template has gained sections worth adopting.

Agents: if `~/.config/acli/org-setup.md` doesn't exist, offer to create it from this template, filled only with values the user provides or confirms. Read it for ground truth; when you learn something that belongs in it (e.g. the user confirms a transition status), suggest adding it.

If a value you need isn't recorded there, ask the user — do not guess or probe.

## Site

- Site: `<mysite.atlassian.net>`

## Projects

| Key | Name | Notes |
|---|---|---|
| `<KEY>` | `<name>` | `<e.g. main team project>` |

## Boards and sprints

| Board ID | Name | Project | Type |
|---|---|---|---|
| `<id>` | `<name>` | `<KEY>` | scrum/kanban |

## Workflow statuses

Valid transition statuses per project (use these exact names with `workitem transition --status`):

| Project | Work item type | Statuses (in workflow order) |
|---|---|---|
| `<KEY>` | `<all / Story / Bug>` | `<To Do → In Progress → In Review → Done>` |

## Link types in use

`<e.g. Blocks, Relates, Duplicates — from acli jira workitem link type>`

## Conventions

- `<e.g. always comment when transitioning to Done>`
- `<e.g. labels taxonomy, required fields on Bugs>`
