# Phase-Wise Implementation Plan: AI-Powered Restaurant Recommendation System

This document details the phase-wise execution roadmap for the restaurant recommendation system based on the [context.md](file:///Users/vkg/Downloads/google-cloud-sdk/Docs/context.md) and [architecture.md](file:///Users/vkg/Downloads/google-cloud-sdk/Docs/architecture.md).

---

## Phase 1: Data Ingestion & Repository Layer
**Goal:** Ingest the Zomato Hugging Face dataset, clean/normalize columns, map them to a canonical schema, and cache the dataframe locally.

### Key Tasks:
1. Define baseline configurations inside `src/config.py` (including dataset identifier, caching directories, and budget thresholds).
2. Model the canonical `Restaurant` data structure (`src/models/restaurant.py`).
3. Build the dataset loader (`src/data/loader.py`) to download `ManikaSaini/zomato-restaurant-recommendation` and save it to a local Git-ignored directory (e.g., `./data/zomato_cache.parquet`).
4. Implement the preprocessor (`src/data/preprocessor.py`):
   - Parse comma-separated cuisine string into a list of strings.
   - Clean location strings (e.g., lowercase, title-case, strip whitespace).
   - Coerce rating and cost to numeric values, handling nulls or invalid values.
   - Derive the budget tier based on cost-for-two.
5. Create the database interface/repository (`src/data/repository.py`) to keep the loaded records in memory and provide simple query interfaces.

---

## Phase 2: User Input Validation & Pre-Filtering
**Goal:** Model user preferences, validate incoming parameters, and perform deterministic pre-filtering to prepare a compact candidate shortlist for the LLM.

### Key Tasks:
1. Define the `UserPreferences` input model (`src/models/preferences.py`).
2. Build preference validators to enforce rules:
   - Validating min-rating matches bounds `[0.0, 5.0]`.
   - Validating budget input corresponds to `low`, `medium`, or `high`.
3. Implement the filter query logic (`src/services/filter.py`):
   - Apply location constraint.
   - Apply budget constraint.
   - Apply rating constraint.
   - Filter by cuisine match (if provided).
   - Order candidates by aggregate rating and review/vote count.
   - Restrict list size to top $N = 15$ candidates.
4. Implement relaxation fallback rules (e.g., if no matching restaurants are found, automatically drop cuisine constraints, then rating bounds, and present a soft warning to the user).

---

## Phase 3: Prompt Construction & LLM Client (Groq Integration)
**Goal:** Setup prompt layout schemas, connect with the Groq client library, and manage response parsing and error retries.

### Key Tasks:
1. Model LLM responses (`src/models/recommendation.py`):
   - Structured recommendation node format (Rank, Name, Cuisine, Rating, Cost, Rationale).
   - Full structured response container with meta-data information.
2. Build the system prompt generator (`src/services/prompt_builder.py`):
   - Instruct the LLM to output pure JSON.
   - Prevent the LLM from hallucinating/fabricating candidate details.
   - Pass user preferences and the candidate list as json data contexts.
3. Code the `LLMClient` adapter (`src/services/llm_client.py`):
   - Initialize the SDK client using `GROQ_API_KEY`.
   - Implement temperature controls (`0.3` default, retrying at `0.1` on invalid JSON payload errors).
   - Handle rate limits (HTTP 429) using exponential backoff retry.
4. Build the core orchestration coordinator (`src/services/recommendation.py`):
   - Chain pre-filtering $\to$ prompt generation $\to$ Groq completion API request $\to$ response parsing $\to$ schema verification.

---

## Phase 4: Integration & Presentation Layer
**Goal:** Expose the core recommendation engine through a robust backend API and build a high-quality frontend interface for the user.

### Sub-Phase 4.1: Backend API Development
1. Create a basic CLI script (`src/ui/cli.py`) allowing interactive console queries for local testing.
2. Initialize a FastAPI server (`src/api/main.py`) to serve the recommendation engine.
3. Build the `POST /api/recommendations` endpoint to accept user preferences, run the orchestration logic, and return the structured JSON responses.
4. Configure CORS middleware and global error handlers to support the frontend application.

### Sub-Phase 4.2: High-Quality Frontend Development
1. Initialize a modern frontend web application (e.g., React + Vite) inside the `frontend/` directory.
2. Build an interactive and aesthetically pleasing UI with modern design principles (vibrant colors, glassmorphism, micro-animations).
3. Create form widgets (location, budget dropdown, cuisine selectors, rating slider) that send requests to the FastAPI backend.
4. Implement active execution loaders/spinners while waiting for the LLM response.
5. Display results using modern card components showcasing badges, clean spacing, rating scores, cost levels, and the explanation rationale.
6. Render elegant warnings or alerts when fallbacks/relaxations occur.

---

## Phase 5: Hardening, Fallbacks & Testing
**Goal:** Implement automated tests, robust fallbacks, and complete documentation.

### Key Tasks:
1. Write Unit Tests (`tests/`):
   - `test_preprocessor.py`: Verify column conversions and budget bucketing.
   - `test_filter.py`: Assert filtering functions correctly isolate subsets.
   - `test_recommendation.py`: Verify JSON payload extraction and parsing.
2. Formulate complete error handling fallbacks:
   - If the Groq API fails repeatedly (due to quota/limits), fallback to sorting matches strictly via heuristic scores (rating $\times$ review counts) with a standard explanation card.
3. Package dependencies inside `requirements.txt` and provide a clean `README.md`.
