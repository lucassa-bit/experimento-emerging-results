Using `speckit-clarify` for the clarification-only workflow. I’ll read its instructions, then inspect only the allowed input files.

---

I’ll follow the experimental constraints over the normal interactive parts: no hooks, no prerequisite script, no edits, and no inferred answers. Next I’m reading only `spec.md`, `experiment-input/user-story.md`, and `experiment-input/context.md` if present.

---

1. [NEEDS CLARIFICATION] Is the set of required estimators fixed when the voting round starts, or recalculated dynamically as participants connect/disconnect during the round?

2. [NEEDS CLARIFICATION] If an estimator submits an estimate and then disconnects before reveal, should their stored estimate still be revealed?

3. [NEEDS CLARIFICATION] When the moderator closes voting with zero submitted estimates, should the round enter a revealed/closed state or remain unrevealed?

4. [NEEDS CLARIFICATION] After reveal, should spectators see the revealed estimates, or only active estimators and moderators?

5. [NEEDS CLARIFICATION] Before reveal, may participants see who has submitted without seeing estimate values?