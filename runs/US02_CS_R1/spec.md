# Feature Specification: Recycling Facility Search

**Feature Branch**: `[001-recycling-facility-search]`

**Created**: 2026-07-08

**Status**: Draft

**Input**: User description: "As a user, I want to enter a ZIP code and receive a list of nearby recycling facilities so that I can decide which facilities to consider."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Find nearby recycling facilities by ZIP code (Priority: P1)

A user enters a ZIP code and receives an ordered list of nearby active, verified recycling facilities so they can decide which facilities to consider.

**Why this priority**: This is the primary value of the feature and directly satisfies the user goal.

**Independent Test**: Can be fully tested by submitting a valid ZIP code with known nearby facilities and verifying that the returned list contains only eligible facilities ordered by distance.

**Acceptance Scenarios**:

1. **Given** a valid ZIP code with active, verified facilities within 25 miles, **When** the user submits the ZIP code, **Then** the user sees up to 20 nearby recycling facilities ordered by straight-line distance from the ZIP code center.
2. **Given** a valid ZIP code with more than 20 active, verified facilities within 25 miles, **When** the user submits the ZIP code, **Then** the user sees no more than 20 results.
3. **Given** a valid ZIP code with no active, verified facilities within 25 miles, **When** the user submits the ZIP code, **Then** the user is told that no nearby recycling facilities were found.

### User Story 2 - Prevent searches with invalid ZIP codes (Priority: P2)

A user receives feedback when a ZIP code cannot be validated, preventing an invalid search from being submitted.

**Why this priority**: Validation prevents misleading or unusable results and supports a clear user experience.

**Independent Test**: Can be fully tested by entering invalid ZIP code values and verifying that the search is not submitted and corrective feedback is shown.

**Acceptance Scenarios**:

1. **Given** an invalid ZIP code, **When** the user attempts to search, **Then** the system rejects the search and explains that a valid ZIP code is required.
2. **Given** an empty ZIP code entry, **When** the user attempts to search, **Then** the system rejects the search and prompts the user to enter a ZIP code.

### Edge Cases

- The submitted ZIP code is syntactically valid but cannot be converted into geographic coordinates.
- The facility directory contains inactive or unverified facilities within the search radius.
- Multiple facilities have the same calculated distance from the ZIP code center.
- Fewer than 20 eligible facilities are available within the configured search radius.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to enter a ZIP code as the search input.
- **FR-002**: System MUST validate the ZIP code before submitting the search.
- **FR-003**: System MUST reject empty or invalid ZIP code searches with clear user-facing feedback.
- **FR-004**: System MUST identify nearby recycling facilities within a 25-mile search radius from the geographic center of the submitted ZIP code.
- **FR-005**: System MUST exclude inactive facilities from search results.
- **FR-006**: System MUST exclude unverified facilities from search results.
- **FR-007**: System MUST return no more than 20 eligible facilities for a submitted ZIP code.
- **FR-008**: System MUST order returned facilities by straight-line distance from the geographic center of the submitted ZIP code.
- **FR-009**: System MUST show a no-results message when no eligible facilities are found within the configured radius.

### Key Entities

- **ZIP Code**: Postal code submitted by the user to define the geographic area of the search.
- **Recycling Facility**: Registered facility with coordinates, active status, and verification status.
- **Result List**: Ordered collection of matching facilities returned for the submitted ZIP code.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of valid ZIP code searches with eligible facilities show a result list in under 3 seconds.
- **SC-002**: 100% of displayed results are active and verified facilities within 25 miles of the submitted ZIP code center.
- **SC-003**: 100% of result lists contain 20 or fewer facilities.
- **SC-004**: At least 90% of users can submit a ZIP code and interpret whether nearby facilities are available without assistance.

## Assumptions

- Users search by manually entering a ZIP code rather than sharing device location.
- Nearby means within the configured 25-mile radius.
- Distance is calculated as straight-line distance for the initial version.
- The facility directory contains the facility location, active status, and verification status needed for eligibility filtering.
