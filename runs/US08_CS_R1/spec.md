# Feature Specification: Simultaneous Estimate Reveal

**Feature Branch**: `[002-simultaneous-estimate-reveal]`

**Created**: 2026-07-08

**Status**: Draft

**Input**: User description: "As a participant, I want all estimates to be revealed simultaneously after every estimator has submitted so that individual estimates remain independent."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reveal estimates after all active estimators submit (Priority: P1)

A participant sees all submitted estimates revealed at the same time only after every active estimator has submitted, preserving estimate independence.

**Why this priority**: Simultaneous reveal is the core behavior needed to avoid anchoring and social influence.

**Independent Test**: Can be fully tested by having all active estimators submit estimates and verifying that no estimate is visible before completion and all estimates become visible in one reveal.

**Acceptance Scenarios**:

1. **Given** active estimators are submitting estimates for the current round, **When** fewer than all active estimators have submitted, **Then** submitted estimates remain hidden from participants.
2. **Given** every active estimator has submitted an estimate, **When** the final required estimate is stored, **Then** all stored estimates are revealed to connected participants in one event.
3. **Given** estimates have been revealed for the round, **When** a participant views the round, **Then** all submitted estimates are visible.

### User Story 2 - Moderator closes voting before all active estimators submit (Priority: P2)

A moderator can close voting manually when waiting for every active estimator is no longer appropriate, causing submitted estimates to be revealed together.

**Why this priority**: Manual closure handles practical situations such as stalled rounds while preserving simultaneous reveal for stored estimates.

**Independent Test**: Can be fully tested by starting a round with active estimators, leaving at least one estimate unsubmitted, closing voting as moderator, and verifying that submitted estimates are revealed together.

**Acceptance Scenarios**:

1. **Given** at least one active estimator has not submitted, **When** the moderator closes voting, **Then** all stored estimates for the round are revealed in one event.
2. **Given** a disconnected participant or spectator exists, **When** determining whether all required estimates are submitted, **Then** that participant is excluded from the completion count.

### Edge Cases

- An estimator disconnects before submitting an estimate.
- A spectator is connected during a voting round.
- The moderator closes voting when no estimates have been submitted.
- A participant attempts to change an estimate after reveal.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST store submitted estimates as hidden until the reveal condition is met.
- **FR-002**: System MUST determine the completion count using active estimators only.
- **FR-003**: System MUST exclude spectators from the completion count.
- **FR-004**: System MUST exclude disconnected participants from the completion count.
- **FR-005**: System MUST reveal all stored estimates simultaneously after every active estimator has submitted.
- **FR-006**: System MUST allow a moderator to close voting manually before every active estimator has submitted.
- **FR-007**: System MUST reveal all stored estimates simultaneously when the moderator closes voting.
- **FR-008**: System MUST prevent estimate changes after reveal unless the moderator starts a new round.
- **FR-009**: System MUST make revealed estimates visible to connected participants.

### Key Entities

- **Estimate**: Value submitted by an estimator for the current item, hidden until reveal.
- **Active Estimator**: Connected participant eligible to estimate in the current round.
- **Voting Round**: Current estimation cycle with hidden estimates until reveal.
- **Moderator**: Participant who may close voting manually or start a new round.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of submitted estimates remain hidden until all active estimators have submitted or the moderator closes voting.
- **SC-002**: 100% of reveal events expose all stored estimates for the round at the same time.
- **SC-003**: 100% of post-reveal estimate change attempts are prevented unless a new round has started.
- **SC-004**: At least 90% of participants report that estimates are revealed only after independent submission is complete.

## Assumptions

- The current round has a known set of connected active estimators.
- Spectators can observe the round but are not eligible to submit estimates.
- The moderator is authorized to close voting when waiting is no longer appropriate.
- A new round resets estimate visibility and editability rules.
