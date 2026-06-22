# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  - "The hints provide were the opposite of what was correct"
  - "The new game button would not start a new game"

  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| changed difficulty from easy to hard| banner under "Make a guess" heading should show the correct range(1-50)| the range would not change and remains (1-100) | none|
| start new game on hard mode| all numbers in secret should be between 1 and 50 | the actual random number would be between 1-100 |Secret: 82 |
|secret was 82, inputted 75 as guess | the hint should say go higher  | the hint said to go lower | |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - Claude code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - for the banner bug, Claude reviewed the code that updates the difficulty changes, noting that the sidebar will update the changes correctly but the code for the banner has a hard coded value. It provides a fix that uses f strings to embed the range into the banner. I verified the result by trying the suggested fix and saw that the intervals were now properly showing.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - for the bug where the genrated secret wouldn't be in range when switching difficulties, claude gave me a hard coded answer when the mode is hard. I instead changed it to directly take the range values from the selected diffculty and generate a number from there. I tested that it worked by repeatedly changing the difficulties to ensure no wrong numbers were generated.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I reviewed the code's logic and checked the tests that Claude generated to see if they passed
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  -One test that I ran on pytest was a test that tested all that all diffucluties generated numbers within it's range. It showed me that the code I had was functioning as I expected.
  
- Did AI help you design or understand any tests? How?
  - The AI helped me design automated tests using Pytest, which saved me a lot of time as I was testing everything manual before

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Streamlit is like a whiteboard, as each app interaction will rerun the main script and renders the page again.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  -when ever I implement new features, I can use AI to help me generate tests based on what I need to test. When I am prompting claude, the caveman skill helps to save tokens and provide concise yet clear information.
- What is one thing you would do differently next time you work with AI on a coding task?
  -I would spend more time adding comment blocks for better context
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - this project helped me understand how I can use AI to better debug code. Using it as an assistant in explaining logic and building tests really helped.
