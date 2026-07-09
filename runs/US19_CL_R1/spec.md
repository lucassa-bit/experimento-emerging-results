# Feature Specification: Training Waitlist

**Feature Branch**: `[003-training-waitlist]`

**Created**: 2026-07-08

**Status**: Draft

**Input**: User description: "As an attendee, I want to join a training waitlist so that I can be considered when a place becomes available."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Join waitlist for a full training class (Priority: P1)

An eligible attendee joins the waitlist for a full class while registration is open so they can be considered if a place becomes available.

**Why this priority**: Joining the waitlist is the core user goal and creates the ordered entry needed for later consideration.

**Independent Test**: Can be fully tested by using a full class with open registration and an eligible attendee, then verifying that the attendee is added to the ordered waitlist.

**Acceptance Scenarios**:

1. **Given** a class is full, registration is open, and the attendee is eligible, **When** the attendee joins the waitlist, **Then** the attendee is added to the waitlist with an order based on successful entry time.
2. **Given** a class is not full, **When** an attendee attempts to join the waitlist, **Then** the attendee is not added to the waitlist because places are still available.
3. **Given** registration is closed, **When** an attendee attempts to join the waitlist, **Then** the attendee is not added to the waitlist.

### User Story 2 - Offer an available place to the first eligible attendee (Priority: P2)

When a place becomes available, the first eligible attendee on the waitlist is notified and has 24 hours to accept the place.

**Why this priority**: Consideration for available places is the outcome promised by joining the waitlist.

**Independent Test**: Can be fully tested by creating an ordered waitlist, making a place available, and verifying that the first eligible attendee receives an offer with a 24-hour acceptance period.

**Acceptance Scenarios**:

1. **Given** a class has an ordered waitlist, **When** a place becomes available, **Then** the first eligible attendee is notified of the available place.
2. **Given** an attendee receives a waitlist offer, **When** the attendee accepts within 24 hours, **Then** the attendee can be enrolled for the class.
3. **Given** an attendee receives a waitlist offer, **When** 24 hours pass without acceptance, **Then** the offer is no longer available to that attendee.

### User Story 3 - Coordinator removes ineligible or duplicate entries (Priority: P3)

A coordinator removes waitlist entries that are duplicates or no longer eligible, with a recorded reason.

**Why this priority**: Removal keeps the waitlist accurate and auditable without changing the first-come, first-served policy.

**Independent Test**: Can be fully tested by removing a duplicate or ineligible entry and verifying that the reason is recorded and the waitlist order updates accordingly.

**Acceptance Scenarios**:

1. **Given** a duplicate waitlist entry exists, **When** a coordinator removes it with a reason, **Then** the entry is removed and the reason is recorded.
2. **Given** an attendee is no longer eligible, **When** a coordinator removes the entry with a reason, **Then** the entry is removed and the reason is recorded.

### Edge Cases

- Two attendees join the waitlist at nearly the same time.
- An attendee tries to join the same waitlist more than once.
- The first attendee on the waitlist becomes ineligible before a place is available.
- A place is added after the class was previously full.
- A notified attendee does not accept within 24 hours.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow an attendee to join a training waitlist only when registration is open and the class is full.
- **FR-002**: System MUST verify attendee eligibility before adding the attendee to a waitlist.
- **FR-003**: System MUST maintain waitlist order by the timestamp of successful entry.
- **FR-004**: System MUST prevent duplicate active waitlist entries for the same attendee and class.
- **FR-005**: System MUST notify the first eligible attendee when a place becomes available.
- **FR-006**: System MUST give a notified attendee 24 hours to accept the available place.
- **FR-007**: System MUST NOT automatically enroll an attendee when a waitlist notification is sent.
- **FR-008**: System MUST enroll the attendee only after the attendee accepts an available-place offer within the allowed period.
- **FR-009**: System MUST allow coordinators to remove duplicate or no-longer-eligible entries with a recorded reason.

### Key Entities

- **Attendee**: Person eligible to register for training and join waitlists.
- **Training Class**: Class with capacity, registration status, eligibility rules, and available places.
- **Waitlist Entry**: Ordered record of an attendee waiting for a place in a full class.
- **Available-Place Offer**: Notification that gives the first eligible attendee 24 hours to accept an available place.
- **Coordinator Removal**: Recorded action that removes a duplicate or ineligible waitlist entry with a reason.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of successful waitlist joins are ordered by successful entry timestamp.
- **SC-002**: 100% of waitlist joins are blocked unless registration is open, the class is full, and the attendee is eligible.
- **SC-003**: 100% of available-place notifications go to the first eligible attendee on the waitlist.
- **SC-004**: 100% of waitlist offers expire after 24 hours if not accepted.
- **SC-005**: 100% of coordinator removals record a reason.

## Assumptions

- The training catalog provides class capacity, registration status, and eligibility rules.
- Joining a waitlist does not guarantee enrollment.
- First-come, first-served ordering is the expected policy for waitlist consideration.
- Coordinators are authorized to remove duplicate or no-longer-eligible entries.
