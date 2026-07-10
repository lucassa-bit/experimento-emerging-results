Using `speckit-clarify` for this turn because the request explicitly invokes the clarification workflow. I’ll read its instructions, then only inspect the allowed local files.

---

The skill’s normal flow would update the spec interactively, but your experimental constraints override that: I’ll produce only unresolved clarification questions and won’t write files or use other project metadata.

---

1. [NEEDS CLARIFICATION] Is the required estimator set fixed when a voting round starts, or recalculated from the Presence Service at reveal time?

2. [NEEDS CLARIFICATION] If an estimator disconnects before submitting, should their missing estimate immediately stop blocking reveal, or only after the moderator closes voting?

3. [NEEDS CLARIFICATION] Before reveal, may an estimator change or replace their hidden submitted estimate?

4. [NEEDS CLARIFICATION] When the moderator closes voting with zero submitted estimates, should the system reveal an empty result set or leave the round unrevealed?

5. [NEEDS CLARIFICATION] Should participants who reconnect or join after reveal see the already revealed estimates for that round?