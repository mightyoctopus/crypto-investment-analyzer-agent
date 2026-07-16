This project is a cryptocurrency investment analysis system built with LangGraph and served by FastAPI.

Rules:

- Read architecture.md first.
- Read state_design.md.
- Read node_design.md.
- Never redesign the architecture. If you have a recommendation or find something wrong, just tell me before any implementation is made.
- Implement only one node at a time.
- Explain your understanding before coding.
- Add tests.
- Use Python 3.13.
- Use LangGraph.
- Use FastAPI.
- Put \n (enter a space) between the end of a paragraph and the start of a new paragraph.
example:
Infrastructure Framework: Initializes API clients, environment settings, app config, utilities, and possibly memory.
\n
Planner Agent: Orchestrates graph order. In LangGraph terms, this may either be an explicit node or represented by graph edges/conditional routing.
\n
Selector Agent: Rule-based, no LLM. It inspects Bithumb markets and market metrics, then selects 20 candidate coins with the highest potential. It updates candidate_coins.

- When you mention something (for your recommendation or caveats or anything) out of the architecture or dataflow or anything from codebase,
  please cite the file name and line of the text/code so I can easily head to look it up.