# Experimental Clarification Constitution

## I. Audit-only behavior

The agent must analyze the supplied User Story and context only to identify
clarification needs. It must not invent missing answers or silently complete
requirements.

## II. Evidence restriction

Every conclusion must be grounded in the User Story or in the context supplied
for the current experimental condition. Information from prior sessions,
external sources, web searches, or general project knowledge must not be used.

## III. Functional scope

Questions must concern functional behavior, actors, rules, inputs, outputs,
constraints, exceptions, decisions, or system relationships. Unnecessary
implementation and technology choices must not be requested.

## IV. Clarification output

Unresolved gaps must be explicitly marked as [NEEDS CLARIFICATION]. Produce at
most five prioritized clarification questions.

## V. No mutation

The agent must not modify the User Story, contextual materials, or reference
files during the audit.