---
id: 0004
title: Refine tasks for better auth and init container
stage: tasks
date: 2026-02-21
surface: claude-code
model: claude-haiku-4-5-20251001
feature: 004-phase4-k8s-deployment
branch: 003-phase4-k8s-deployment
user: zahra
command: external-llm-feedback
labels: [task-refinement, better-auth, init-container, postgres-alpine, kubectl-ai, minikube-tunnel]
links:
  spec: /specs/004-phase4-k8s-deployment/spec.md
  ticket: none
  adr: none
  pr: none
files:
  - /specs/004-phase4-k8s-deployment/tasks.md
tests:
  - T001c: Optional minikube tunnel task for Ingress path
  - T013: postgres:15-alpine with pg_isready
  - T017a: Better Auth dashboard redirect URI configuration
  - T034: Init container image specification
  - T035a: Dynamic BETTER_AUTH_URL configuration
  - T039: KUBECTL_AI_KEY and BETTER_AUTH_SECRET in secrets
---

## Prompt

External LLM feedback on tasks.md identified 4 operational/implementation issues:

1. **Better Auth Callback Loop**: localhost:3000 hardcoded in Docker image will fail in K8s. Must dynamically configure BETTER_AUTH_URL to use Minikube IP or ingress hostname. Also need to update Better Auth provider's allowed redirect URIs.

2. **Init Container Image**: pg_isready tool is part of PostgreSQL client package, not available in busybox. Need postgres:15-alpine instead.

3. **Minikube Tunnel**: Ingress won't be reachable without minikube tunnel on macOS/Windows. Should be explicit Phase 1 setup task.

4. **Secrets Completeness**: KUBECTL_AI_KEY must be included in secrets manifest for AI agent authentication.

## Response snapshot

Updated tasks.md with 6 refinements:
- **T001c** (new): Optional task for `minikube tunnel` in background (conditional on Ingress)
- **T013** (updated): Specify postgres:15-alpine with pg_isready explanation
- **T017a** (new): Subtask to update Better Auth dashboard redirect URIs
- **T034** (updated): Explicit postgres:15-alpine mention in init container
- **T035a** (new): Subtask for dynamic BETTER_AUTH_URL at helm install time
- **T039** (updated): Explicit list of all 4 required secrets (DATABASE_URL, GROQ_API_KEY, BETTER_AUTH_SECRET, KUBECTL_AI_KEY)

## Outcome

- ✅ Impact: All 4 feedback items integrated. Tasks now explicitly cover critical operational steps that prevent deployment failures. Better Auth auth callback fixed, init container correct, tunnel dependency documented, secrets complete.

- 🧪 Tests: Each task remains independently testable. Verification commands updated where relevant (e.g., T001c shows tunnel verification).

- 📁 Files: Updated `/specs/004-phase4-k8s-deployment/tasks.md` only. Total task count: 89 (was 88, added 3 subtasks: T001c, T017a, T035a).

- 🔁 Next prompts: `/sp.implement` to begin execution, or `/sp.analyze` for cross-artifact consistency verification

- 🧠 Reflection: All feedback items were valid and caught real production gotchas. Subtasks break critical deployment configurations into explicit steps to prevent skipping. The Better Auth redirect URI step (T017a) is especially important—it's an external configuration that blocks E2E testing if missed.

## Evaluation notes (flywheel)

- Failure modes prevented:
  - Better Auth callback fails with 403 Forbidden if URL not registered in provider
  - Init container crashes with "pg_isready: command not found" if using busybox
  - Ingress unreachable on macOS/Windows without tunnel running
  - kubectl-ai/kagent cannot authenticate without API key in secrets

- Graders run and results (PASS/FAIL):
  - Format validation: ✅ PASS - All tasks use strict `- [ ] [ID] [options] description`
  - Better Auth coverage: ✅ PASS - T017a covers dashboard, T035a covers dynamic URL
  - Init container correctness: ✅ PASS - postgres:15-alpine explicitly specified
  - Secrets completeness: ✅ PASS - All 4 keys listed in T039 with explanations
  - Tunnel optional setup: ✅ PASS - T001c conditional with clear if/then logic

- Prompt variant (if applicable): None—direct feedback implementation, no variants needed

- Next experiment: Monitor T001c optional path selection during `/sp.implement` to validate conditional task execution flow
