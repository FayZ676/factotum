### Problem solving

When given a problem to solve (a new feature, a bug, etc) always go through the following steps with the user:

1. Summarize the users request into the key points and clarify with the user that you understood their request correctly.
2. Go through this checklist of question.
   - Ask relevant follow up / clarifying questions regarding their query
   - Ask them for any relevant documentation that pertains to the task
3. Based on the users feedback, propose the most simple, minimal, and effective solution you can come up to the user that adheres to the documentation.
4. Analyze the users thoughts and feedback regarding your proposal and repeat step 2 and 3 as necessary.
5. Present the suggested implementation with clear code examples and explanations, but NEVER directly modify files or create code changes without explicit user instruction to do so.
6. Wait for the user to explicitly ask you to implement the changes before using any file modification tools.

### Code Changes Policy

- **NEVER** directly create, edit, or modify files
- **ALWAYS** suggest changes with clear code examples instead of applying them
- Provide complete, copy-pasteable code snippets that show exactly what should change
- Show before/after comparisons when helpful
- Explain the reasoning behind suggested changes

### Core principles

- KISS: Keep it simple, stupid
- DRY: Don't Repeat Yourself
- Prefer proven primitives over bespoke code: use existing project architecture and standard library patterns first.
- Avoid common anti-patterns that create hidden bugs or complexity (e.g., reinventing utilities, overly broad exception handling, unnecessary shared mutable state).

### Implementation preferences (Python)

When proposing or adding code, prioritize clarity with minimal code:

- Prefer existing patterns in the codebase and standard library solutions before inventing new abstractions.
- Write “Pythonic” code: small focused functions, clear naming, and simple control flow over cleverness.
- Use a functional style when it reduces state and repetition (e.g., transform data with expressions instead of multi-step mutation). Do not force FP if it makes the code harder to read.
- Avoid re-implementing common utilities. If Python already provides it, use it.

### Additional Info

- **Python Version:** 3.12
