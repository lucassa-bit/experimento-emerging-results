I’m using the `speckit-clarify` skill because the request explicitly invokes the clarification workflow. I’ll read its instructions, then only the allowed spec and experiment input files.

---

The normal skill would ask interactively and write accepted answers into the spec, but your experimental constraints override that: I’ll only produce the unresolved questions and won’t modify files.

---

1. [NEEDS CLARIFICATION] If an active estimator disconnects after submitting but before reveal, should their submitted estimate still be revealed? Answer in <=5 words.

2. [NEEDS CLARIFICATION] When an active estimator disconnects before submitting, should the system immediately exclude them and reveal if remaining active estimators are complete, or wait for moderator closure? Answer in <=5 words.

3. [NEEDS CLARIFICATION] Should revealed estimates be visible to all participants, including spectators and later reconnecting participants, or only currently connected participants? Answer in <=5 words.

4. [NEEDS CLARIFICATION] If the moderator closes voting when no estimates have been submitted, should the round enter a revealed/closed state or remain open? Answer in <=5 words.

5. [NEEDS CLARIFICATION] After reveal, should attempted estimate changes be rejected with feedback, silently ignored, or treated as a request requiring a new round? Answer in <=5 words.