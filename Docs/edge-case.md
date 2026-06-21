# Edge Case Analysis: AI-Powered Restaurant Recommendation System

This document outlines the detailed edge cases, corner scenarios, and recovery strategies for the Zomato AI-Powered Restaurant Recommendation System. It serves as a guide for implementation robustness, defensive programming, and unit testing.

---

## 1. Data Ingestion & Preprocessing Layer

### 1.1 Multi-Currency and Country Codes (Critical)
- **Scenario:** The Zomato Hugging Face dataset contains international data (e.g. USA, UK, India, UAE, Australia). The `Average_Cost_for_two` field values are represented in local currencies, and the dataset includes a `Currency` and `Country Code` column.
- **Impact:** Applying standard INR budget thresholds ($\le 500$, $500 - 1500$, $> 1500$) globally will fail. For example, a USD restaurant costing \$30 would be categorized as "Low" budget because $30 \le 500$, leading to incorrect categorization.
- **Handling/Mitigation:** 
  - Segment data by country/currency.
  - For this milestone, **filter the dataset to include only Indian restaurants** (`Country Code == 1` or `Currency == 'Indian Rupees(Rs.)'`).
  - If expanding globally, dynamically scale budget thresholds based on the currency/country code, or maintain country-specific configuration thresholds in `config.py`.

### 1.2 Non-Numeric and Missing Ratings
- **Scenario:** The aggregate rating column contains non-numeric strings such as `"NEW"`, `"-"`, `"N/A"`, or missing/null values.
- **Impact:** Naive conversions to float will raise a `ValueError` and crash the preprocessing pipeline.
- **Handling/Mitigation:** 
  - Treat `"NEW"`, `"-"`, and `"N/A"` as `0.0` or `None`.
  - Coerce numeric rating values cleanly (e.g. parse `"3.9/5"` or `"4.2"`).
  - Cleanly separate valid numeric ratings from unrated/new locations. Unrated locations should default to a rating of `0.0` or be excluded from ratings-based ranking.

### 1.3 Cost-for-Two Formatting and Empty Values
- **Scenario:** The cost column contains commas (e.g., `"1,500"`), currency symbols, or empty spaces.
- **Impact:** Throws conversion exceptions when casting to integer.
- **Handling/Mitigation:** 
  - Strip all non-numeric characters (commas, spaces, currency symbols) from the string before parsing.
  - Impute missing cost values with the median cost of that specific locality/city, or default to a safe fallback (e.g., ₹500) and log a warning.

### 1.4 Inconsistent Location and Cuisine String Formatting
- **Scenario:** The dataset has mixed-casing (e.g., `"new delhi"`, `"New Delhi"`, `"DELHI "`), trailing spaces, or nested locality sub-neighborhoods.
- **Handling/Mitigation:** 
  - Strip leading/trailing whitespaces and convert locations to Title Case.
  - Parse the comma-separated `cuisines` string (e.g., `"North Indian, Chinese, Fast Food"`) into a cleaned list of lowercase, stripped strings: `["north indian", "chinese", "fast food"]`. Handle `NaN` cuisines by initializing an empty list `[]`.

---

## 2. User Input & Preference Validation

### 2.1 Locality vs. City Ambiguity
- **Scenario:** The user types `"Connaught Place"` (a locality) in the location field instead of `"New Delhi"` (the city).
- **Impact:** A strict match against the `City` column returns zero results.
- **Handling/Mitigation:** 
  - Check user inputs against both the `City` and `Locality` columns.
  - Use fuzzy matching (e.g., Levenshtein distance) to suggest correct location names if no exact match is found.
  - Populate dropdown selectors in the Streamlit UI with unified list items in the format: `"{Locality}, {City}"` (or separate City and Locality selectors).

### 2.2 Tyranny of Structured Dropdowns (No Matches Left)
- **Scenario:** The user sets extremely restrictive matching filters (e.g., Location: `"Bangalore"`, Budget: `"low"`, Cuisine: `"Japanese"`, Min Rating: `4.5`), returning zero candidates.
- **Handling/Mitigation (Step-Wise Relaxation Pipeline):**
  Implement a deterministic fallback relaxation algorithm:
  1. **Step 1:** Lower the minimum rating threshold by `0.5` increments (down to a floor of `3.0`).
  2. **Step 2:** If candidates are still zero, drop the **Cuisine** constraint (searching for any cuisine matching the budget and location).
  3. **Step 3:** If candidates are still zero, drop the **Budget** constraint (searching for any budget).
  4. **Step 4:** If candidates are still zero, return a structured response stating that no restaurants could be found and suggesting alternative locations.
  5. Always display a banner detailing which constraints were relaxed (e.g., *"No low-budget Japanese restaurants with rating >= 4.5. Showing all budget Japanese restaurants with rating >= 3.5"*).

### 2.3 Semantic Negations in Custom Instructions
- **Scenario:** The user types negative constraints in the additional text preferences box: `"Not Chinese"`, `"Vegetarian only (no meat)"`, or `"No spicy food"`.
- **Impact:** Simple substring keyword filters on the backend might mistakenly match `"Chinese"` and pre-filter *only* Chinese restaurants, violating the user's intent.
- **Handling/Mitigation:** 
  - **Never** perform programmatic keyword pre-filtering on the backend using the raw free-text `additional` field.
  - Pass the custom text preference raw to the LLM. Let the LLM's semantic parser handle logical negations during the ranking and explanation phase.

---

## 3. Integration & Pre-Filtering Layer

### 3.1 Substring Cuisine Clashes
- **Scenario:** User filters for the cuisine `"Thai"`. Programmatic matching checks `if "thai" in restaurant.cuisines`.
- **Impact:** A restaurant serving `"Mughlai"` or `"Rajasthani"` might match because they contain the letters `"hai"`.
- **Handling/Mitigation:** Perform exact list membership checks rather than raw substring operations. Search the preprocessed cuisine list (`"thai"` in `restaurant.cuisines` list) instead of running a substring check on the raw string.

### 3.2 Over-Saturated Shortlists (Too Many Matches)
- **Scenario:** A search query matches hundreds of rows (e.g., Delhi, Medium Budget, North Indian, Rating $\ge 3.5$).
- **Impact:** Sending hundreds of candidates to the LLM exceeds token limits, increases costs, and degrades performance.
- **Handling/Mitigation:** 
  - Cap candidates forwarded to the LLM at **$N = 15$**.
  - Shortlist sorting order: `aggregate_rating` DESC $\to$ `votes` (popularity) DESC $\to$ `cost_for_two` ASC (value for money).

### 3.3 Near-Empty Shortlists (LLM Ranking of Single Candidate)
- **Scenario:** Only 1 restaurant matches the criteria.
- **Impact:** The LLM cannot perform "ranking" or "comparison". Prompts designed for lists might crash or return warnings.
- **Handling/Mitigation:** 
  - If candidate count is `1`, still invoke the LLM to write a personalized explanation card, but dynamically adjust the prompt template to bypass list comparison ranking.
  - If candidate count is `0`, skip the LLM entirely and immediately return an empty response with user-friendly suggestions.

---

## 4. LLM & Groq API Integration Layer

### 4.1 JSON Mode Prompt Requirements
- **Scenario:** Groq's JSON mode is highly sensitive. If the prompt does not explicitly contain the word `"json"`, the API request will fail or return errors.
- **Handling/Mitigation:** 
  - Ensure the word `"json"` (or `"JSON"`) is explicitly written in the system instructions.
  - Set `response_format={"type": "json_object"}` in the SDK parameters.

### 4.2 Malformed LLM Responses
- **Scenario:** The LLM returns valid JSON, but the structure is wrong (e.g., returns a raw array `[...]` instead of an object `{"recommendations": [...]}`), or misses critical keys (such as `id` or `explanation`).
- **Handling/Mitigation:**
  - Define a strict Pydantic parsing schema on the backend.
  - If parsing fails, catch the error, decrement the LLM temperature (e.g., to `0.1` or `0.0`), and retry the API call once.
  - If the retry fails, activate the **Heuristic Fallback** (Section 4.4).

### 4.3 Out-of-Context Restaurant ID Hallucinations
- **Scenario:** The LLM recommends a restaurant but returns an `id` that was not in the candidate list (either a hallucinated ID or a completely different restaurant).
- **Handling/Mitigation:** 
  - Programmatically validate all IDs in the LLM response against the candidate list sent in the prompt.
  - Discard any item where `response_id not in candidate_ids`.

### 4.4 Groq Rate Limits (HTTP 429) & Complete Failures
- **Scenario:** Groq API returns `RateLimitError` (429) or goes offline.
- **Handling/Mitigation:**
  - Wrap the LLM call in a retry wrapper with exponential backoff (e.g., 3 retries).
  - If the service remains unavailable, return the top 5 candidates derived from the **Heuristic Ranker** (sorted by rating and votes).
  - Supply standard fallback rationales: *"This restaurant matches your location and budget requirements, and is highly rated by Zomato users."*
  - Add a visible warning banner in the UI: *"AI rationale generator is currently offline. Recommendations are based on Zomato user rating heuristics."*

---

## 5. UI & Presentation Layer

### 5.1 RAM Out-of-Memory (OOM) on Large Dataset Ingestion
- **Scenario:** The Hugging Face dataset is large and loads completely into memory, exceeding container memory limits.
- **Handling/Mitigation:**
  - Load only the required split (e.g., `train`).
  - Preprocess and select only necessary columns (Name, Location, Cuisines, Cost, Rating, Votes) to minimize DataFrame memory usage.
  - Cache the preprocessed, compressed DataFrame to local **Parquet** format. On subsequent startups, load the parquet file instead of downloading the dataset.

### 5.2 Network Dropouts During Initial Data Ingestion
- **Scenario:** On first launch, the internet connection drops while downloading the dataset from Hugging Face.
- **Handling/Mitigation:**
  - Wrap the `DatasetLoader` in a try-except block.
  - If download fails and no local cache exists, display a full-page error block in Streamlit: *"Unable to download the Zomato database. Please check your network connection and try again."*
