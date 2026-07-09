Using `speckit-clarify` to inspect the existing spec and permitted experiment inputs, then I’ll return only the requested clarification output.

---

1. [NEEDS CLARIFICATION] What exact minimum data qualifies a user as having “sufficient history” for personalized recommendations?

2. [NEEDS CLARIFICATION] What makes a content item “eligible” beyond not being dismissed by the current user?

3. [NEEDS CLARIFICATION] How should “popular eligible content” be calculated for fallback recommendations?

4. [NEEDS CLARIFICATION] When a user disables interaction-history use, should their history also be excluded from similarity calculations for recommending content to other users?

5. [NEEDS CLARIFICATION] What should happen when fewer than 10 eligible recommendations are available: return fewer items, fill with fallback items, or show a no-results state?