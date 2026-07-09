I’m using the `speckit-clarify` skill and limiting inputs to the files you named.

---

The command’s experimental constraints override the normal interactive/write-back parts of the skill, so I’m only reading the allowed files and producing unresolved questions.

---

1. [NEEDS CLARIFICATION] Which ZIP code formats are valid?
   Options: A) 5-digit US ZIP only; B) 5-digit ZIP and ZIP+4; C) Any postal code accepted by geocoding service.

2. [NEEDS CLARIFICATION] What facility details must appear in each search result so users can decide which facilities to consider?
   Answer in <=5 words.

3. [NEEDS CLARIFICATION] If multiple facilities have the same distance, how should ties be ordered?
   Options: A) Alphabetically by facility name; B) Verification recency; C) Directory order; D) No guaranteed order.

4. [NEEDS CLARIFICATION] What should happen when the Geocoding Service or Facility Directory is unavailable?
   Options: A) Show temporary error and no results; B) Retry then show error; C) Use cached results if available.

5. [NEEDS CLARIFICATION] Should results include only facilities that accept all recyclable materials, or any verified active recycling facility?
   Options: A) Any verified active facility; B) Only facilities accepting all materials; C) Filter by user-selected material.