# Finding Ticket Integration

## Purpose

Turn confirmed CASA findings into actionable engineering work without making external ticket creation an uncontrolled side effect of an assessment.

## Default behavior

Every full/retest assessment should generate a structured ticket queue from open findings.

Default: `queue`.

Do **not** create external GitHub Issues, Jira tickets or other work items unless the user has explicitly authorized ticket creation for that run or has configured an approved automation in the target project.

## Supported modes

- `off`: no queue and no external tickets.
- `queue`: generate local ticket queue only. Default.
- `github`: create/update GitHub Issues when authorized and a writable GitHub connection exists.
- `jira`: create/update Jira tickets when authorized and a Jira/Atlassian connector exists.
- `auto`: use the target project's configured provider, but only where prior explicit authorization exists.

## Ticket content

Each ticket should include:

- finding ID and deterministic `regression_key`;
- severity and status;
- CASA requirement(s);
- CWE/CVSS where applicable;
- affected component(s);
- concise finding description;
- risk and implication;
- remediation;
- implementation guidance;
- retest criteria;
- assessment commit;
- evidence IDs/links where safe;
- report/reference path.

Never paste secrets, tokens, customer data or unsafe exploit payloads into an external ticket.

## Deduplication

Before creating a ticket, search for an existing open ticket containing the same finding ID or regression key.

If found, update/comment on the existing work item rather than creating a duplicate, when the connector supports it.

## Priority mapping

Recommended default mapping:

- Critical -> highest/urgent
- High -> high
- Medium -> normal
- Low -> low
- Observation -> backlog/informational

Do not imply that ticket priority changes the CASA control result.

## Closure

Closing an issue/ticket is not evidence that a finding is fixed. CASA closure requires the retest process in `SKILL.md`.

## Portable queue

Use `scripts/export_ticket_queue.py` to generate:

- `13-finding-ticket-queue.json`
- `13-finding-ticket-queue.md`

An AI agent with an authorized GitHub/Jira connector can then execute the queue.
