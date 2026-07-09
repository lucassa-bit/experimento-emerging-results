# Lexical Context

- A user profile is the set of declared interests and recorded content interactions associated with a user.
- Similar profiles are profiles with comparable interest and interaction patterns.
- A content recommendation is a ranked suggestion from the eligible content catalog.

# Operational Context

- Similarity is calculated from shared interests, viewed content, saved content, and positive feedback.
- The system returns up to ten eligible items that the current user has not already dismissed.
- Users with insufficient history receive non-personalized popular content instead.

# Decisional Context

- Demographic attributes were excluded from profile similarity.
- Collaborative behavioral similarity was selected as the primary recommendation approach.
- Users may disable the use of their interaction history for personalized recommendations.

# Systemic Context

- The Profile Service provides declared interests and privacy settings.
- The Interaction History Service provides eligible behavioral events.
- The Recommendation Engine compares profiles and ranks items from the Content Catalog.
