1. [NEEDS CLARIFICATION] If an active estimator submits an estimate and then disconnects before reveal, should their stored estimate be included in the reveal?
   - A: Yes, reveal all stored estimates
   - B: No, exclude disconnected estimators’ estimates

2. [NEEDS CLARIFICATION] When the moderator closes voting before any estimates have been submitted, what should participants see?
   - A: An empty reveal state
   - B: A “no estimates submitted” message
   - C: Voting remains open until at least one estimate exists

3. [NEEDS CLARIFICATION] After estimates are revealed, who should be able to view revealed estimates?
   - A: Only currently connected participants
   - B: Any participant who later reconnects to the round
   - C: Only active estimators and moderator

4. [NEEDS CLARIFICATION] If the active estimator set changes during a voting round, when is the required completion count determined?
   - A: Dynamically from current active estimators
   - B: Fixed when the round starts
   - C: Updated only by moderator action

5. [NEEDS CLARIFICATION] If the reveal broadcast fails for some connected participants, what behavior is required?
   - A: Participants receive revealed state on reconnect/refresh
   - B: System retries the reveal event
   - C: No explicit recovery required