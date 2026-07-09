# Lexical Context

- A ZIP code is the postal code used to identify the geographic area of the search.
- A nearby recycling facility is a registered facility located within the configured search radius.
- A result list is an ordered collection of matching facilities, not a saved favorites list.

# Operational Context

- The ZIP code must be validated before the search is submitted.
- The default search radius is 25 miles, and no more than 20 active facilities are returned.
- Results are ordered by distance from the geographic center of the submitted ZIP code.

# Decisional Context

- ZIP-code search was selected instead of mandatory device location to preserve user privacy and support desktop users.
- Straight-line distance was selected for the initial version instead of travel-time estimation.
- Inactive and unverified facilities are excluded from search results.

# Systemic Context

- The Geocoding Service converts the ZIP code into geographic coordinates.
- The Facility Directory provides facility coordinates, verification status, and active status.
- The Search Service ranks the facilities and sends the result list to the web interface.
