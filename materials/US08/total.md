# Lexical Context

- An estimate is the value submitted by an estimator for the current item.
- An active estimator is a connected participant who is eligible to estimate in the current round.
- Revealing estimates means making all submitted values visible to every participant.

# Operational Context

- Submitted estimates remain hidden until every active estimator has submitted or the moderator closes voting.
- All stored estimates are revealed in one broadcast event.
- After reveal, estimates cannot be changed unless the moderator starts a new round.

# Decisional Context

- Simultaneous reveal was selected to reduce anchoring and social influence.
- Spectators and disconnected participants are excluded from the completion count.
- The moderator may close voting manually when waiting for every active estimator is no longer appropriate.

# Systemic Context

- The Game Service stores estimates with a hidden status.
- The Presence Service provides the set of active estimators.
- The Realtime Gateway broadcasts the reveal event and all estimates to connected participants.
