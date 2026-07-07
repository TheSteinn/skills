# RPI → CRISPY (QRSPI): Faithful Extraction

Source: `.planning/qrspi-transcript.md` — a raw, unpunctuated transcript of a conference talk by Dex (HumanLayer) on evolving "Research → Plan → Implement" (RPI) into an eight-stage workflow (Question → Research → Design → Structure → Plan → Worktree → Implement → PR), nicknamed "crispy" (QRSPI).

This is a faithful extraction only. Everything below closely paraphrases or directly quotes the talk. Ambiguities in the transcript are preserved, not resolved. Direct quotes are in "quotes".

---

## Background and framing

- Dex has been "talking about coding agents for quite a while," basically since August; did "a long talk in November." The RPI methodology got "a lot of up votes on hackernews." He estimates "probably 10,000 people who have gone to our open source and grabbed our prompts and are using them internally from small startups up to the enterprise."
- "It all started with this guy" — a person the transcript renders as **"E" / "Eigor"** (ambiguous transcription; possibly a name/initial). "Eigor went in and he said like okay cool we're using a lot of tokens. We're spending a lot of money to get AI developer productivity but what he found was that it actually tends to lead to a lot of rework."
  - Finding: "you are shipping 50% more but half of that is just cleaning up the slop from last week."
  - "these are last year's numbers... this does not account for opus 4.5. So I would... inflate this a little bit."
  - "it's great for low complexity green field tasks, not great for high complexity brownfield tasks."
- The talk's stated purpose: "I'm going to tell you everything we got wrong about RPI today." (He declines to re-give the RPI talk; points to other talks for context.)

## What RPI got WRONG vs. what it got RIGHT

Things they got **wrong** (Dex: "I am humble enough to admit when I was wrong"):
1. "I don't think it's okay to not read the code." (Relevant to a Twitter debate "today.")
2. "I also don't think you should read really long plan files." (He says these two are related.)
3. "Claude should not be allowed to [ship unread] if you['re] writing production code that is used by users and you're going to get [paged] 3:00 a.m. if it's broken."
4. "No slop. This is the year 2026. No more slop."

Things they got **right**:
1. "There is no magic prompt."
2. "Do not outsource the thinking. You the engineer are an important part of this process."
3. "Seek leverage. There's a lot of code being written. Find ways to make sure it's correct without having to read all of it and resteer after the fact."

The four goals to aim for:
- "High leverage planning."
- "Not outsource the thinking."
- "Read and own the code."
- "Ideally we will avoid... magic words."

Diagnosis of the core problem: "we would give these tools to an expert... and they would get great results. They would go sit and talk to Cloud for 70 hours a week and they would start shipping like crazy. And then they would go give it to their team and the results were not always so good." Two failure areas surfaced when they "got in the trenches": (1) people were "not getting good research," and (2) people were "getting not great plans."

## The research problem

- The November approach: "pick a zone of your codebase... say we're going to build something over here," then launch a coding-agent session that sends **sub agents through deep vertical slices** through the codebase to produce "compressed context about what is the thing we're about to go build."
- The rule for research: "keep things objective, discourage opinions. Don't actually put any implementation details in there. You just want to compress the truth. What is true about how the code works today?"
- A skilled engineer was good at going from ticket → questions → research: "here's my ticket. Let me write some questions that will cause the model to go touch all the parts of the codebase that matter."
  - Worked example: ticket = "add a new endpoint to reticulate splines across tenants" → questions like "tell me how endpoints work and trace the logic flow for everything that touches splines and... go find the workers that do all the reticulation."
- The failure mode: many people "would just say, Hey research codebase. Here's what I'm building."
- The key principle: **"good research is all facts. But if you tell the model what you're building, then you get opinions."** ("we'll get into why the model shouldn't have opinions later." Ties to "do not outsource the thinking," which the transcript attributes to **"Jake from Netflix."**)
- The fix (deterministic ticket-hiding + separate context windows): "we just hide the ticket from the context window that's doing research and we do it deterministically. So basically you have **one context window to generate questions and then a fresh context window with no knowledge of what we're building** to go make your research doc."
- Analogy: "this is pretty trivial if you're familiar with the concept of **query planning**. It's similar in concept but for... LMS reading through code bases."

## The planning problem

- The old planning prompt was "a single giant like monolithic thing with **85 or more instructions**." It had steps built in like: "present design options to the user, get feedback on the structure, before you actually go write the plan."
- A *good* planning session (all in **one context window / one session** — Dex notes the sideways slides using columns that would normally denote separate context windows):
  1. Say "create plan" → loads the skill, looks at the ticket, loads the research doc.
  2. Launches sub agents "to go find a bunch of things that are true about the codebase, just confirm some stuff that wasn't maybe in the research."
  3. Agent asks questions ("here's our options for question one"); user picks options.
  4. Agent proposes an order of phases; user can resteer ("we need to add a testing step up front, and I want to swap phases three and four").
  5. Agent gives a new outline; user approves; "only then would we write our plan file."
- The failure mode: "for about **50% of people, maybe more**, if you didn't prompt it with this work back and forth with me — or Opus was just feeling dumb for that... particular hour of the day — it would just take the stuff and it would just immediately go and write the plan out." Result: "cool, I wrote the plan, didn't ask me any questions, made all the decisions for me. Yikes."

### The "magic words"

- Users told him: "you have to say the magic words." The magic incantation: **"work back and forth with me starting with your open questions and outline before writing the plan."** Saying it made the agent ask questions.
- Dex found himself in "workshops full of enterprise engineers saying... don't forget to say the magic words. It was, quite frankly, it was embarrassing."
- His stance: "this isn't the user's fault. If you built a tool that requires hours and hours of training and reps to get... good results from, go fix the tool."

### The instruction budget

- "One of the big takeaways... is you have an **instruction budget**."
- His co-founder **Kyle** "wrote this really good blog post in December or November" citing "this archive [arXiv] paper" (also "from last year") that "**Frontier LMS could only follow about 150 to 200 instructions with... good consistency. Anything more than that and it's kind of half attending to all of them and you're rolling the dice.**"
- "So if you have a prompt with 85 instructions and your cloud MD and your system prompt and your tools and your MCP... you're not likely to get full adherence to the workflow."

## The leverage argument (don't read plans; read code)

- November-era advice (which he now recants): "you have to read the plan otherwise it won't work." Some people "would PR their plans and code review them together."
- The problem: "a **thousand line plan tends to be about a thousand lines of code within 10% or so**. And plans can have surprises." You review the plan, then the implementation "would be different," so reviewers "have to go read the code again and see what the surprises were and what changed."
- "This isn't leverage. **Leverage is about... do less work to get more output.**"
- New advice: "**don't read the plans. Please read the code.** Just... it's the same amount of work and... look for leverage elsewhere."
- On his August position ("don't read the code... the plans are enough... just ship"): "I was wrong... We tried not reading the code for like six months. It did not end well. **We had to rip out and replace large parts of that system.**"
- On projects where people *don't* read the code:
  - "Beads, 300,000 lines and counting. No one's read that code allegedly."
  - "OpenClaw Pete's like... I know the structure and the pieces and how they fit together, but I don't read every line of every PR."
  - Distinction: "these are OSS projects. They don't charge money. Nobody gets paid at 3 a.m. if it's broken. And no one gets fined millions of dollars if it's done wrong." (He is "deeply humbled by the accomplishments of the maintainers"; stakes are still high — "if you break open claw, a lot of people are going to be upset" — but "different than if you're... working in a regulated industry shipping production SAS code.")
- "If you have people who depend on your code, please... read it. We have a profession to uphold. **2026 is supposed to be the year of no more slop.** Literally everyone is talking about the difference between slop and craft."
- On agent swarms: "this is why I'm a little mid on agent swarms and the whole gas town thing because you still need to be able to ensure quality... **going 10 times faster doesn't matter if you're going to throw it all away in 6 months. So shoot for 2 to 3x.**" (How to measure/achieve that is "another talk.")

## The design document (design discussion)

- Answers: **"where are we going? What does the final solution look like?"**
- Contents:
  - **Current state**
  - **Desired end state**
  - **Patterns to follow** — "This is your chance to go read all the patterns it found that it thinks are relevant and be like, Nope, that's not how we do atomic SQL updates. That's some engineer that doesn't work here anymore... Go find the way we do it over there." (Addresses agents following bad/wrong patterns.)
  - **Resolved design decisions** — "it'll keep track of resolved design decisions that we've made."
  - **Open questions** — "It will ask open questions."
- Framing: "sort of like taking cloud code **plan mode and the ask user question tool** and just brain dumping it all to a single document that you can interact with — [it] is moldable and flexible."
- **The "design concept"** — attributed to **Matt Pco [Matt Pocock]**: "the thing that is locked up in this context window that is the shared understanding between you and the agent of what's being built and how."
- Format/size: "a **200-line markdown artifact**."
- Purpose = **human-agent alignment / "brain surgery on the agent":** "you're forcing the agent to brain dump out all the things it found, all the things it wants to do, all the things it thinks you want, and ask you questions about things it doesn't know. So you can do **brain surgery on the agent** before you proceed downstream... You want to give the agent every single opportunity to show you what it's wrong about **before you go write 2,000 lines of code.**"
- Leverage math here: "200 lines instead of a thousand — a little bit more leverage."

## The structure outline

- Distinction: **"if design is like where are we going, the structure outline is how do we get there?"** Meeting analogy: "there's the... architecture review [what are we going to build] and then there's the sprint planning meeting... how do we break it down into tasks?"
- Built in a **new context window** from design + ticket + research.
- Contents: "**high[-]level overview of the phases. Not the exact code we're going to write, but... what it's going to look like, what order we're going to do the changes in, and how we're going to test it along the way.**"
- **Test checkpoints:** "I don't actually test in between every phase everything I'm building. But if it's sensitive or if it's hard or if it's complex, I want to be able to catch it before it goes and writes all the code. I want to make sure **each two, three, 400 line block is correct.**"
- Lighter reviews / size comparison for the same feature: **"plan eight pages, structure outline two-ish pages, much shorter."**
- **C header file analogy:** "if the plan is the implementation, the outline is the C header files — just here's the signatures and the new types that we're changing — enough... for you to see what the agent is thinking and correct it if it's wrong."
- **Why it exists — vertical vs horizontal plans:** "despite... every single model and trying to prompt this out and eval the hell out of this, we cannot get models to stop writing **horizontal plans**. [This] is the best way to fix their need to write horizontal plans."
  - Horizontal plan (bad): "we're going to do all the database and then... all the services and then... all the API and then... all the front end and before you know it, you're on the other side of[ 1],200 lines of code and it's not working and now you have to go figure out which part is broken because there was... nothing really to test along the way."
  - **Vertical plans** (what he advocates, "what I call vertical plans... seen work really really well across orgs of all sizes"): "how I build... before AI — I would make a mock API endpoint and then get it working in the front end and then wire that and then mock out the services layer and then do the database migration and then put everything together." "Even though it's the same amount of code you have these **checkpoints** where you can see if it's working and if it's not you can pause and fix it before you go try to do the rest of it."
- These are markdown docs: "you can and should ask for more detail. They start high level, but... I don't think you're going to get this right — tell me what you're thinking — and it dumped out the types and the signatures."

## The plan

- Built the same way: "take that artifact, we build it up with all the previous artifacts and then we can go build the plan."
- **Same template as old create_plan:** "it is the same if you use create plan. It's the **exact same template, exact same setup, exact same prompt**, but this is a **tactical doc for the agent.**"
- **Spot-check only:** "we've already done enough aligning that... I'm just going to spot check this and then we save the deep review for the actual code."
- Content shape: "the model saying, Hey, here's all the changes I'm going to make."

## Context engineering principles

- Dex wrote **"12 factor agents"** — "allegedly the first time anyone was... talking a lot about context engineering."
- "Two ways to read context engineering":
  1. The common one (RAG-style): "put more information [in]. You put too much information in, the model can't make sense of it."
  2. The read he finds "more interesting": **"better instructions and simpler tasks and smaller context windows."**
- **The "dumb zone"** (attributed to context around "Jeff" — "we all know Jeff now"): "you have about **168,000 tokens** [of] 200,000, but some of them [are] reserved for output... around like **40% on average**... you hit this point where you have degrading results. Sometimes you can... still get good enough for you results at 60%. But **the less of the context window you use the better results you will get.**"
- **Too many instructions, not just too much info** (crediting "our friends at data bricks"): "you have too many MCPs, the whole context window is full of instructions about how to use a bunch of tools that you don't care about and then by the time you're writing code the model's... not good at following your instructions."
- **Prompts-for-control-flow vs. control-flow:**
  - Customer-support example: "if it's a complaint, go do this. If it's product feedback, go do this. If it's a billing issue, go do this."
  - Fix: "instead of using prompts for control flow, you can... classify the input and then feed it to a series of **smaller, more focused prompts where there are far fewer instructions and far fewer actions to choose from.**"
  - Lesson: **"don't use prompts for control flow if you can use control flow for control flow. The if statement is really really powerful and LM[s] are really good at classifying things."** ("not just true for coding agents... any AI LLM based system you're building.")
- The self-aware irony: "we got on stage and... said full fat agents don't work. Don't just call tools in a loop. Do context engineering and build workflows and graphs and micro agents. We told everybody don't do this. And then we turned around in August... and we wrote this giant monolithic prompt. So we figured it was time to actually go **drink our own Kool-Aid.**"
- The split result: the old **85-instruction** mega-prompt was broken into several prompts that are **each "less than 40" instructions** ("some of them could actually be even smaller. We're still iterating on them.").

## Team / social benefits

- The biggest leverage "is not just about you and the agent." Sharing the **design discussions and structure outlines** (the shorter docs, not the plans) with teammates is "really really good."
- Dex's own practice: "I am **not the code owner of most of our code at human layer** — my co-founder is — and **I send him my design discussions on purpose.** We don't have a required step, but... when we get to code review, [I want] it's just going to be like, Yep, that's what I wanted. So any of my bad decisions are headed off on a 200-line doc before I've gone and written the code and gotten it working and I'm attached to it."
- **Time-savings model:**
  - "Before AI... it's a two-day feature... The coding is probably **2 to four hours.**"
  - "If you just pick up cloud code... the coding takes **20 minutes**. It's still a two-day feature because I still have to align with my team, still get a code review and fix stuff... working across repos I don't personally own... verify and test it."
  - "But if you use AI to help you with your **planning and alignment**, then you also save time there... your code review and rework is also much shorter because you already know what's coming. The team that's reviewing it already... had their chance to resteer you."
  - "Really good teams do this... a meeting called **architecture review** where we decide... what's our technical design doc on how we're going to build this."
- On testing/verifying: "sorry I don't have a good answer for you. It's a whole other talk... go find **Drew Brunick** after [Drew's talk downstairs]. He will tell you all about testing and verifying."

## The full workflow (RPI → CRISPY / QRSPI)

- "We split it across several prompts. Before it was **research, plan, implement.** Now it's **questions, research, design, structure, plan, work[,] tree, implement, PR.**"
- Full stage list as summarized at the end: "**questions, research, design, structure outline, plan, work tree, implement. Finally, the pull request.**"
- Named the "**five stages of research and planning**" (i.e., planning was split into design discussion + structure outline + plan).
- On the name: "that didn't make a very good acronym though, so we just picked the ones we liked. And we're calling this **crispy**. So RPI to crispy."
- Note: "We're actually not going to have time to talk about the **implement** side of the thing today."

## What's next / open questions Dex raised

- Adoption complexity: "three steps was already a lot for some people to learn and now there are seven. I thought we were supposed to make this easier for teams to learn... and adopt."
- Measuring impact: "we've been trying to measure developer productivity for 50 years and we still don't know how to do it very well."
- Platform/central-team rollout: "if you're a central... platform team rolling out changes to everybody in your org, how do you make these prompts better?... every team has a skill now, and we want to consolidate and make that shared... How do you make that stuff better without breaking somebody's workflow or regressing it for some team?"
- Recruiting / calls to action: HumanLayer is hiring; "if you're in San Francisco and you're working on critical systems... let's chat." Contact "**Founders at human layer.dev**" (i.e., founders@humanlayer.dev). "We're building an IDE that orchestrates this stuff for you. You don't need this to get this value out of this."
- Events mentioned: a "**sandbox research hackathon on Saturday**" (test all sandbox providers, share learnings); the "**Daytona Compute Conference**"; "**AI Engineer Miami**" (where he'll give "the updated version of this talk with more stuff"). Thanks to "Demetrios and the entire organizing squad."

## Q&A insights

1. **"Reading the code isn't scalable — will you be saying the same thing in six months?"**
   - "Six months ago, I said not to read it... I think everyone who is saying don't read the code now is going to be in six months being like, Yeah, we had to throw that out. There's something in the middle... **we're binary searching through the space of how much of the code should you read.** ... if you still read the code, you can still get **two to 3x** speed up. And that's actually better business outcomes than going 10x faster and shipping a bunch of slop and hoping that... GPT7 will fix it for you."

2. **On the "software factory" / never having a human read either side (attributed to "strong DM" [Sourcegraph's/StrongDM?] — transcript ambiguous — "pushes us further into eval").**
   - "There's a whole rabbit hole... formal verification and TLA plus, or I talked to a guy who's building a new [T]A plus that is **TA++** — okay, what if we don't read the code? How can we actually formally verify everything?... I think there's a lot of people right now who need to ship code to production systems faster. So maybe someday. I used to [cite] **Sean Gro['s] [Sean Grove's]** talk where he was like it's just the spec — just write the document that explains the desired behavior and you treat the code like it's assembly and you never read it anymore. **I do not endorse that.**"

3. **On the "dumb zone" — has he revisited it given autocompaction, etc.?**
   - "For... if you have been using AI coding agents for six to nine months and you use them for 60 hours a week, **the dumb zone is not a useful concept to you.** I will regularly go up to 60. I will regularly aggressively keep it below 30. It depends on the complexity of your task, the amount of instructions versus information."
   - Guidance for beginners: "if you don't know what to do and you haven't developed that intuition, then shoot to keep it under **40** and if you get up to **60**, think about wrapping it up. You can keep iterating on the same doc."
   - On compaction: "**we don't use the built-in compaction because everything that matters is going into static assets and so you can always resume from where you left off** without having to worry about the quality of an autocompact or a manual compact."

---

## Names, references, and numbers mentioned (as transcribed)

- **Eigor** (ambiguous; the person/study behind the "50% more shipped, half is slop" and "green field vs brownfield" findings; "last year's numbers... doesn't account for opus 4.5").
- **Jake from Netflix** — origin of "do not outsource the thinking."
- **Kyle** — Dex's co-founder; blog post (Nov/Dec) citing an arXiv paper on the 150–200 instruction limit.
- **Matt Pco [Matt Pocock]** — "the design concept."
- **Jeff** — invoked around the "dumb zone" / context-window concept ("we all know Jeff now").
- **Drew Brunick** — testing & verifying (had a separate talk "downstairs").
- **Sean Gro [Sean Grove]** — "it's just the spec... treat the code like assembly"; Dex does NOT endorse.
- **Databricks** — the "too many MCPs / too many instructions" point.
- Projects cited as "don't read every line": **Beads** ("300,000 lines and counting"), **OpenClaw / OpenClaw Pete**.
- Key numbers: 10,000 users of the prompts; 85 instructions (old monolith) → <40 (each new prompt); 150–200 instruction limit; ~168,000 usable of 200,000 tokens; ~40% "dumb zone" onset (good-enough sometimes to 60%); 200-line design doc vs ~1,000-line plan vs ~1,000 lines of code; plan "eight pages" vs structure outline "two-ish pages"; 2–3 or 400-line test blocks; 2–3x realistic speedup vs 10x slop; two-day feature / 2–4 hr coding → 20 min coding; 12 Factor Agents; RPI → CRISPY.

---

## Details unique to (or more precise in) THIS transcript

Both `.planning` transcripts are near-identical transcriptions of the same talk. The substantive content (numbers, names, structure, quotes) matches almost word-for-word. Notable differences where THIS (`qrspi`) transcript is more precise, or differs:

- **"Drew Brunick"** — this transcript gives the fuller surname; the other transcript truncates it to "Drew Brun." (More precise here.)
- **"Founders at human layer.dev"** — this transcript renders the contact as separable words (readable as `founders@humanlayer.dev`); the other transcript mashes it into "Foundershumanlayer.dev." (Clearer here.)
- **First workflow enumeration includes "work, tree"** ("questions, research, design, structure, plan, work, tree, implement, PR") — i.e., worktree is present in the initial list; the other transcript's first enumeration omits "tree" ("...plan, work, implement, PR"). (More complete here; both later say "work tree" in the final summary.)
- **"this guy E."** — this transcript inserts an initial/name fragment ("Um this guy E. Has anyone seen this talk?") before "Eigor"; the other transcript omits it ("Um this guy has anyone seen this talk?"). Ambiguous either way.

Details **absent** from this transcript that appear in the other (for completeness — NOT part of this source, so not extracted above):
- The MC's opening banter and, importantly, the **slide count**: the other transcript captures Dex correcting "200 slides" down to **"158"** slides. This `qrspi` transcript starts directly at "Uh I am Dex" and does not contain the slide-count exchange.
- The closing line is shorter here ("Brilliant Dex.") vs. the other's fuller sign-off.
