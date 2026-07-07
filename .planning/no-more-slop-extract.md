# No More Slop — RPI to "Crispy" (QRSPI)

Faithful extraction from a conference talk by Dex Horthy (HumanLayer). This is a
close paraphrase/quote of the talk only — no outside knowledge or invention.
Where the talk is ambiguous, the ambiguity is preserved.

## Background and framing

- Dex has been talking about coding agents since roughly August; there was a
  long talk in November. The existing methodology is **Research → Plan →
  Implement (RPI)**. It got lots of upvotes on Hacker News; "probably 10,000
  people" have grabbed the open-source prompts and use them internally, from
  small startups up to the enterprise.
- It started with a talk/finding (attributed to "Eigor"): teams are using a lot
  of tokens and spending a lot of money to get AI developer productivity, but
  it tends to lead to a lot of rework — "you are shipping 50% more but half of
  that is just cleaning up the slop from last week."
- Those were last year's numbers and do **not** account for Opus 4.5, so Dex
  says he would "inflate this a little bit." The finding: AI is great for **low
  complexity green-field tasks**, not great for **high complexity brownfield
  tasks.**
- The talk is explicitly a retrospective: "I'm going to tell you everything we
  got wrong about RPI today... I am humble enough to admit when I was wrong."
- Recurring theme / tagline: "This is the year 2026. No more slop." Everyone is
  talking about the difference between **slop and craft.**

## What RPI got wrong vs. what it got right

### What they got wrong
1. **"I don't think it's okay to not read the code."** (Reversing earlier advice.)
2. **You should not read really long plan files.** (These two are related.)
3. Cloud/the agent should not be allowed to write production code unused by
   users unchecked — "if you're going to get paged at 3 a.m. if it's broken."
   No slop.

### What they got right
1. **There is no magic prompt.**
2. **Do not outsource the thinking.** "You the engineer are an important part of
   this process." (Credited to Jake from Netflix: "do not outsource the
   thinking.")
3. **Seek leverage.** "There's a lot of code being written. Find ways to make
   sure it's correct without having to read all of it and re-steer after the
   fact."

### The stated goals for getting to near-human quality
- High-leverage planning.
- Do not outsource the thinking.
- Read and own the code.
- Ideally avoid "magic words."
- Aim for **2–3x**, not 10x: "going 10 times faster doesn't matter if you're
  going to throw it all away in 6 months." (This is why Dex is "a little mid on
  agent swarms and the whole gas town thing" — you still need to ensure
  quality.) How to measure and reach 2–3x while maintaining near-human quality
  is "actually another talk."

### Why "read the code" specifically
- In November, Dex told people on stage "you have to read the plan otherwise it
  won't work." In August he had said "don't read the code... just ship and let
  Cloud do its thing." He now says both were wrong.
- "We tried not reading the code for like six months. It did not end well. We
  had to rip out and replace large parts of that system."
- On the counter-examples (OSS projects where maintainers don't read every
  line): "Beads, 300,000 lines and counting. No one's read that code
  allegedly." OpenClaw's Pete "knows the structure and the pieces and how they
  fit together, but doesn't read every line of every PR." Dex is "deeply
  humbled" by these maintainers — but the stakes differ from **regulated-industry
  / production SaaS** code. "If you have people who depend on your code, please
  I'm begging you, please read it. We have a profession to uphold."

## The adoption problem: "expert vs. team"

- Since October, HumanLayer worked with thousands of engineers, tiny startups up
  to Fortune 500s. Give the tools to an expert and they get great results —
  they'd "sit and talk to Cloud for 70 hours a week and start shipping like
  crazy." Then they'd give it to their team and results were not always good.
- Getting in the trenches with users, the failures fell into: bad research, bad
  plans, and reviewing the wrong artifact (the plan) for leverage.

## The "magic words" problem

- The RPI `create plan` prompt had steps built in (present design options, get
  feedback on structure before writing the plan), but it was **one giant
  monolithic prompt with 85+ instructions.**
- For about 50% of people (maybe more), unless you prompted with the exact magic
  phrase, the agent would skip the interactive steps and immediately write the
  plan — "didn't ask me any questions, made all the decisions for me. Yikes."
  (Also framed jokingly as "Opus was just feeling dumb for that particular hour
  of the day.")
- **The magic words for research/planning:** *"Work back and forth with me,
  starting with your open questions and outline, before writing the plan."* Say
  this and the agent asks questions; omit it and it just writes the plan.
- Dex found himself in enterprise workshops saying "don't forget to say the
  magic words" — "quite frankly, it was embarrassing."
- Key stance: **"This isn't the user's fault. If you built a tool that requires
  hours and hours of training and reps to get good results from, go fix the
  tool."**
- During the hand-poll, only a couple of people had run `create plan` with the
  interactive "work back and forth" phrasing; "some of you found out about the
  magic words. A lot of people didn't."

## The instruction budget

- **Frontier LLMs can only follow about 150–200 instructions with good
  consistency.** Beyond that they're "kind of half attending to all of them and
  you're rolling the dice."
- Sourced to a blog post by co-founder Kyle (Dec/Nov) citing an arXiv paper
  (last year's number, "probably a little bit higher now").
- Implication: a prompt with 85 instructions, **plus** your CLAUDE.md, system
  prompt, tools, and MCP — "you're not likely to get full adherence to the
  workflow." If any of the instructions weren't followed, you'd skip the steps
  that made the process high-leverage.
- Databricks example: too many MCPs means the whole context window is full of
  instructions about tools you don't care about, so by the time the model is
  writing code it's "not good at following your instructions." You're not just
  giving the model too much information, "you're also probably giving it too
  many instructions."

## The research problem

- **Facts vs. opinions:** Good research is **all facts.** "If you tell the model
  what you're building, then you get opinions." (The model shouldn't have
  opinions — see "do not outsource the thinking.")
- The November approach (one reused slide): pick a zone of the codebase; launch
  a session that sends sub-agents through **deep vertical slices** of the
  codebase to gather compressed context about the thing you're about to build.
  Guidance: **keep things objective, discourage opinions, don't put
  implementation details in there.** "You just want to compress the truth. What
  is true about how the code works today?"
- **Hiding the ticket from the research context:** A skilled engineer takes the
  ticket and writes questions that make the model touch all the relevant parts
  of the codebase. Example ticket: "add a new endpoint to reticulate splines
  across tenants" → questions like "tell me how endpoints work, trace the logic
  flow for everything that touches splines, and go find the workers that do all
  the reticulation."
- The fix, done **deterministically**: **hide the ticket from the context
  window that does research.** Use **one context window to generate questions**,
  then a **fresh context window with no knowledge of what's being built** to
  produce the research doc.
- **Query-planning analogy:** "This is pretty trivial if you're familiar with
  the concept of query planning. It's similar in concept but for LLMs reading
  through codebases."

## Context engineering principles

- Dex wrote **"12-factor agents"** — "allegedly the first time anyone was
  talking a lot about context engineering."
- **Two readings of context engineering:**
  1. The RAG reading — "put more information in." But "you put too much
     information in, the model can't make sense of it."
  2. The more interesting reading (which Dex favors): **better instructions,
     simpler tasks, and smaller context windows.**
- **The "dumb zone":** A context window is about 200,000 tokens (some reserved
  for output — "about 168,000 tokens and 200,000"). Around **40% on average**
  (depending on task and how much of context is user messages vs. files) you
  hit degrading results. Sometimes you can still get "good enough" results at
  60%, but **the less of the context window you use, the better the results.**
- **Prompts-for-control-flow vs. control-flow-for-control-flow:** Customer-
  support example — if it's a complaint do X, if product feedback do Y, if
  billing do Z. Instead of using a prompt to do that branching, **classify the
  input and feed it to a series of smaller, more focused prompts** with far
  fewer instructions and far fewer actions to choose from. **"Don't use prompts
  for control flow if you can use control flow for control flow. The if
  statement is really powerful, and LLMs are really good at classifying
  things."** True for any LLM-based system, not just coding agents.
- **Splitting into <40-instruction prompts:** The single mega prompt with 85
  instructions was split across several prompts. RPI (research, plan, implement)
  became **questions, research, design, structure, plan, worktree, implement,
  PR.** Each prompt is now **under 40 instructions** ("some of them could
  actually be even smaller — we're still iterating").
- Self-deprecating aside: In earlier talks they told everyone "full-fat agents
  don't work, don't just call tools in a loop, do context engineering and build
  workflows and graphs and micro-agents." Then in August they "turned around and
  wrote this giant monolithic prompt." Splitting it up was "time to actually
  drink our own Kool-Aid."

## The leverage argument

- The problem with reviewing plans: "**A thousand-line plan tends to be about a
  thousand lines of code within 10% or so.** And plans can have surprises." You
  review the plan (an hour of a co-worker's time), then implement it, then the
  code is different, so they have to re-read the code to find the surprises.
  **"This isn't leverage. Leverage is about doing less work to get more
  output."**
- **New advice: "Don't read the plans. Please read the code."** Reading a
  thousand-line plan and then a thousand lines of code is the same amount of
  work — look for leverage elsewhere.
- Where the leverage actually is: **the design discussion might only be 200
  lines**, and "you get a lot of opportunities to re-steer in that moment."
- Comparison of artifacts for the same feature: **plan ≈ 8 pages; structure
  outline ≈ 2-ish pages** — much shorter, "lighter reviews."

## The design document

- Answers: **"Where are we going? What does the final solution look like?"**
- Contents:
  - **Current state**
  - **Desired end state**
  - **Patterns to follow** — your chance to read the patterns the agent found
    relevant and correct it: "Nope, that's not how we do atomic SQL updates.
    That's some engineer that doesn't work here anymore... go find the way we do
    it over there." (Addresses the common failure of agents following bad
    patterns they found in the codebase.)
  - **Resolved design decisions** (it keeps track of decisions made)
  - **Open questions** (it asks you)
- It's "like taking Cloud Code plan mode and the ask-user-question tool and just
  brain-dumping it all to a single document that you can interact with" — moldable
  and flexible.
- **Matt Pocock's "design concept":** "the thing that is locked up in this
  context window that is the shared understanding between you and the agent of
  what's being built and how." Put into a **~200-line markdown artifact.**
- **Human–agent alignment / "brain surgery on the agent":** You force the agent
  to brain-dump everything it found, everything it wants to do, everything it
  thinks you want, and ask questions about what it doesn't know — "so you can do
  brain surgery on the agent before you proceed downstream." It's all about
  **not outsourcing the thinking**: "give the agent every single opportunity to
  show you what it's wrong about before you go write 2,000 lines of code."

## The structure outline

- **Design = "where are we going"; structure = "how do we get there."**
- Meeting analogy: design is the **architecture review** ("what's our technical
  design doc"); structure is the **sprint planning meeting** ("how do we break
  it down into tasks").
- Built in a **new context window** from the design + ticket + research. It's a
  **high-level overview of the phases** — not the exact code, "just kind of what
  it's going to look like, what order we're going to do the changes in, and how
  we're going to test it along the way." **~2 pages.**
- **Test checkpoints between phases:** Dex doesn't test between every phase, but
  "if it's sensitive or hard or complex, I want to catch it before it writes all
  the code. I want to make sure each two-, three-, 400-line block is correct."
- **C header file analogy:** "If the plan is the implementation, the outline is
  the C header file. Just here's the signatures and the new types that we're
  changing — enough for you to see what the agent is thinking and correct it if
  it's wrong."
- **Vertical vs. horizontal plans:** Despite every model and heavy eval effort,
  "we cannot get models to stop writing horizontal plans" — the outline "is the
  best way to fix their need to write horizontal plans."
  - **Horizontal plan** (what models love to do): "do all the database, then all
    the services, then all the API, then all the front end" — and 1,200 lines
    later it's not working and there was nothing to test along the way, so you
    can't tell which part is broken.
  - **Vertical plan** (what works across orgs of all sizes): how Dex built
    pre-AI — mock an API endpoint, get it working in the front end, wire that,
    mock out the services layer, do the database migration, put it together.
    Same amount of code, but you get **checkpoints** where you can see if it's
    working and pause/fix before doing the rest.
- These are just markdown docs; you can and should ask for more detail. They
  start high level, but you can say "I don't think you're going to get this
  right, tell me what you're thinking," and it "dumped out the types and the
  signatures."

## The plan

- Built the usual way: take the structure artifact, build it up with all the
  previous artifacts, then build the plan.
- **Same as `create plan`** — "exact same template, exact same setup, exact same
  prompt" — but the plan is now a **tactical doc for the agent.**
- Because alignment has already happened upstream, "I'm just going to **spot
  check this** and then we **save the deep review for the actual code.**"
- RPI plans look like "the model saying, here's all the changes I'm going to
  make."

## Team / social benefits

- The leverage isn't just between you and the agent. The shorter docs (design
  discussions, structure outlines) are "really, really good" to review with
  teammates. ("I said don't review the plans, but these shorter docs are really
  good" to review.)
- Dex is not the code owner of most of HumanLayer's code (his co-founder is), so
  he **sends the co-founder his design discussions on purpose.** No required
  step, but "I want to know that when we get code review, it's just going to be
  'yep, that's what I wanted.'" Bad decisions get **headed off on a 200-line doc
  before** the code is written, working, and he's attached to it.
- **The two-day-feature time-savings model:**
  - A "two-day feature" where the actual coding is ~2–4 hours.
  - If you just use Cloud Code to ship: coding drops to ~20 minutes, but **it's
    still a two-day feature** — you still align with the team, get code review
    and fix stuff, maybe work across repos you don't own, and verify/test.
  - If you use AI to help with **planning and alignment**, you save time there
    too, get much better alignment, and **code review and rework are much
    shorter** because everyone already knows what's coming and had a chance to
    re-steer.
- **Architecture review analogy:** "Really good teams do this. They have a
  meeting called architecture review where we decide what's our technical design
  doc on how we're going to build this."
- On testing/verifying: "Sorry, I don't have a good answer for you. It's a whole
  other talk." (Points to Drew's talk / "Drew Brun.")

## Putting it together: "crispy" (QRSPI)

- Full process: **Questions → Research → Design → Structure (outline) → Plan →
  Worktree → Implement → Pull Request.**
- "That didn't make a very good acronym, so we just picked the ones we liked,
  and we're calling this **crispy.** RPI to crispy."
- The **implement side was not covered** in this talk due to time.

## What's next / open problems (not covered in depth)

- Three steps was already a lot for some teams to learn; now there are seven —
  "I thought we were supposed to make this easier for teams to adopt."
- **Measuring impact:** "We've been trying to measure developer productivity for
  50 years and still don't know how to do it very well."
- **Central platform teams:** how do you improve these prompts / the engineering
  system for the whole org without breaking or regressing some team's workflow?
  "Every team has a skill now, and we want to consolidate and make that shared
  and let people benefit from each other's learnings."
- HumanLayer is hiring and building an **IDE that orchestrates this stuff** —
  "you don't need this to get value out of it, but this is the kind of stuff
  we're working on."

## Q&A insights

- **Reading code / scalability:** Q: reading the code isn't scalable — will you
  be saying the same thing in six months? A: "Six months ago I said not to read
  it, and... everyone who is saying don't read the code now is going to be in
  six months being like, yeah, we had to throw that out. There's something in
  the middle... we're binary searching through the space of how much of the code
  you should read." If you still read the code you can get 2–3x speed-up, which
  is "better business outcomes than going 10x faster and shipping a bunch of
  slop and hoping GPT-7 will fix it for you."
- **Formal verification / software factory:** Q: what about the "software
  factory" idea (attributed to "strong DM") where no human reads either side, and
  isn't that pushing us into eval? A: There's a whole rabbit hole — **formal
  verification and TLA+** (mentions talking to someone building "TLA++",
  "TA++") — "what if we don't read the code, how can we formally verify
  everything?" "I think there's a lot more to be built," but a lot of people
  right now need to ship to production faster. He used to cite Sean Grove's talk
  ("it's just the spec — write the document that explains the desired behavior,
  treat the code like assembly, never read it again") but **"I do not endorse
  that."**
- **Dumb-zone thresholds / autocompaction:** Q: have you revisited the "dumb
  zone" given newer/larger context windows and autocompaction? A: For people who
  have used AI coding agents for 6–9 months at 60 hours/week, "the dumb zone is
  not a useful concept" — Dex "will regularly go up to 60" and also "aggressively
  keep it below 30," depending on task complexity and the ratio of instructions
  vs. information. For **beginners** who haven't developed the intuition: "shoot
  to keep it under 40, and if you get up to 60, think about wrapping it up... you
  can keep iterating on the same doc."
- **No built-in compaction because state lives in static artifacts:** "That's
  what's also nice about these — **we don't use the built-in compaction because
  everything that matters is going into static assets**, so you can always
  resume from where you left off without having to worry about the quality of an
  autocompact or a manual compact."
