# Truffle Hunt

**A rule-based AI reasoning assignment built around a collaborative digging game**

> Part of the [Ready · Remix · Run](https://github.com/Ready-Remix-Run) archive of classroom-tested CS assignments.

---

## At a Glance

| | |
|---|---|
| **Author** | Jeffrey L. Popyack, Drexel University |
| **Assignment Type** | Game-based / Interactive simulation |
| **CS Concepts** | Artificial intelligence, rule-based reasoning, pattern matching, logical deduction |
| **Grade Band** | High school · Introductory college |
| **Time Required** | 1–2 class periods (50–90 min each) |
| **Prerequisites** | Basic familiarity with logical reasoning; no prior programming required |
| **Materials** | Computer with a web browser |

---

## Overview

Truffle Hunt is a browser-based game in which students play the role of a truffle farmer working alongside a rule-trained boar to locate hidden truffles in a 10×10 field — without accidentally letting the boar eat them.

What makes this assignment rich is the AI layer. Students don't just play the game; they **train the boar** by writing pattern-matching rules that guide its decisions. The boar examines the field and applies student-defined rules to probe safe cells or mark cells it believes contain truffles. Students iterate on their rule sets, observing how well their logic holds up across different game states.

This is a highly accessible entry point into AI and rule-based reasoning — students engage with core concepts like pattern recognition, logical inference, and edge cases without writing a single line of traditional code.

---

## Learning Objectives

By the end of this assignment, students will be able to:

- Explain how rule-based AI systems make decisions
- Design and test pattern-matching rules using a structured notation
- Apply logical deduction to determine safe moves and identify truffle locations
- Reflect on the limitations of rule-based systems and where they break down
- Iterate on a system based on observed outcomes

---

## Files in This Folder

| File | Description |
|------|-------------|
| `index.html` | The Truffle Hunt game — open in any web browser, no installation needed |
| `TruffleHunt_instructions.pdf` | Student-facing assignment instructions |
| `ai-comparison.pdf` | Student-facing document/infographic comparing rules-based AI to large language models like ChatGPT. Note: This infographic was generated entirely by an LLM. |

---

## How to Teach It

### Before Class
- Test the game yourself in a browser (`index.html`) to get comfortable with gameplay and the Rule Center
- Decide whether students will work individually or in pairs (pairs work well for discussion)
- Optional: play a round of Truffle Hunt in Solo Mode as a warm-up to introduce the underlying logic — just add `?solo` to the end of the URL when opening `index.html`

### In Class
1. **Introduce the game** (5–10 min) — Briefly explain the premise: students are truffle farmers training a boar to help them search a field safely. Let students play freely in Solo Mode for a few minutes before introducing rules.
2. **Introduce rules** (10–15 min) — Walk through the rule notation together. The first rule (cells adjacent to a 0 are safe) is provided as a starting point.
3. **Students write and test rules** (30–45 min) — Students develop their own rule sets, test them using the Rule Maker, and iteratively improve their boar's performance.
4. **Debrief** (10–15 min) — Discuss: Where did your rules succeed? Where did they fail? What would it take to make a boar that never loses?

### Discussion Questions
- What happens when none of your rules apply? What does that tell you about rule-based AI?
- Can you write rules that *guarantee* a win? Why or why not?
- How is this similar to or different from how you imagine modern AI works?
- What would you need to add to make the boar handle uncertain situations?

---

## Adapting for Different Audiences

### Make It Easier
- Pre-load a starter set of rules and have students extend rather than build from scratch
- Reduce the number of rules students are expected to write (e.g., just the "safe neighbor" cases)
- Have students play the game manually first for a full period before introducing the rule-writing component
- Use pair programming / collaborative rule-writing to lower the barrier

### Make It Harder
- Challenge students to write a *complete* rule set that handles every provably solvable situation
- Ask students to analyze the game mathematically: what percentage of games are solvable with perfect rules?
- Have students document their rule sets formally and present them to the class
- Extend the activity by having students compare rule sets — whose boar wins more often?

### Connections to Other Courses
- **Math:** Logical deduction, set theory, probability
- **Philosophy:** Formal reasoning, the limits of rule-following systems
- **Introductory CS:** This works well as an early AI unit with no coding required, before transitioning to code-based AI topics

---

## Classroom Notes

*This section is for real stories from teachers who have used this assignment. If you've taught Truffle Hunt and want to contribute your experience — what worked, what surprised you, what you'd do differently — please open a pull request or an issue.*

---

## Credits & License

Created by **Jeffrey L. Popyack**, Drexel University (popyack@drexel.edu).
Original game developed in 2006; ported to HTML5/JavaScript in 2015; last updated October 2024.

Shared under [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to use, adapt, and share this assignment — please credit the original author.
