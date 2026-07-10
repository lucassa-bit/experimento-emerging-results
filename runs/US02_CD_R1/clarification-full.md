Using `speckit-clarify` because the request explicitly invokes the clarify workflow. I’ll read its instructions, then only the allowed local files.

---

The experimental constraints override the normal interactive/write-back parts of the clarify skill. I’m only reading `spec.md` plus the permitted experiment-input files and will return the unresolved questions without answering them.

---

`context.md` exists, so I’m treating it as the only additional context beyond the user story, as requested.

---

1. [NEEDS CLARIFICATION] Should ZIP input accept only 5-digit U.S. ZIP codes, or also ZIP+4 format?

2. [NEEDS CLARIFICATION] What facility details must appear in each result so users can decide which facilities to consider?

3. [NEEDS CLARIFICATION] What should break ties when multiple facilities have the same calculated distance?

4. [NEEDS CLARIFICATION] What user-facing outcome is required when a valid ZIP code cannot be geocoded?

5. [NEEDS CLARIFICATION] What source of truth defines whether a facility is active and verified?