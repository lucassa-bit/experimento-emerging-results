Using `speckit-clarify` because the request is specifically for the clarification workflow. I’ll read its instructions, then inspect only the allowed inputs.

---

I found `spec.md` and `experiment-input/user-story.md`; there is no `experiment-input/context.md`, so I’ll treat the story as having no extra context as requested.

---

1. [NEEDS CLARIFICATION] When is the required estimator set fixed for a voting round: at round start, dynamically based on currently connected estimators, or only after each participant’s role is confirmed?

2. [NEEDS CLARIFICATION] If an active estimator disconnects before submitting, should their absence immediately reduce the completion count and possibly trigger reveal?

3. [NEEDS CLARIFICATION] Are spectators allowed to see revealed estimates once the reveal condition is met, or only active estimators and the moderator?

4. [NEEDS CLARIFICATION] If the moderator closes voting when no estimates have been submitted, should the round enter a revealed/closed state with no estimates, or remain unrevealed?

5. [NEEDS CLARIFICATION] After estimates are revealed, may late-joining or reconnected participants see the revealed estimates for that round?