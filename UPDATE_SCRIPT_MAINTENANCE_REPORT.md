## Update Script Maintenance Report

Date: 2026-03-04

- Root cause: workflow relied on push-trigger coupling and did not declare content-write permissions.
- Fixes made: kept scheduled/manual execution, removed unnecessary push trigger, upgraded checkout action, and added `permissions: contents: write`.
- Validation: reviewed update and validation jobs plus guarded commit behavior.
- Known blockers: dataset updates still depend on valid `IUCNREDLIST_TOKEN` secret availability.
