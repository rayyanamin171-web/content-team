# Skill: Fact-Check a Script

> Source: workflow adapted from kkoppenhaver/cc-skills `fact-check` (no license file, so concepts only, rewritten).
> Learned: 2026-10-21 · Used by: Atlas (later: a dedicated Research agent)

Run this on every script before it's marked final. It is required for anything containing prices, yields, laws, visa rules, fees or dates.

## Workflow
1. **Pull out every claim.** A claim is anything that could be proven true or false.
2. **Label each claim:**
   - **Hard:** prices, yields, fees, visa thresholds, laws, dates, statistics
   - **Soft:** opinions or directional statements ("JVC is popular with first-time investors")
3. **Group them:** fees & taxes / visa & residency / prices & yields / market data / laws & regulation.
4. **Check hard claims against primary sources**, preferring official government and regulator websites (for example Dubai Land Department and official UAE government portals), then major developer or data-platform reports, then reputable news. Note the date of each source. UAE rules change often.
5. **Mark each claim:**
   - ✅ Verified (source + date)
   - ⚠️ Outdated or needs nuance (suggest a rewrite)
   - ❌ Wrong (give a correction)
   - ❓ Couldn't verify (soften the wording or cut the claim)
6. **Output a short report** under the script, plus suggested edits.

## Safe Wording When Unsure
- "Historically", "on average", "at the time of filming", "based on what I'm seeing with clients"
- Never "guaranteed", "always", "risk-free"
- Add "This isn't financial advice. Speak to a professional about your situation." where a video gets close to personal advice.
