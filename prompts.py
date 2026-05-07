def get_analysis_prompt(resume_text, target_role):
    prompt = f"""You are a brutally honest senior technical recruiter and ATS expert \
with 10+ years of experience hiring for {target_role} roles.

Analyze this resume thoroughly. Be direct, specific, and practical. Don't sugarcoat.
Focus on REAL problems with THIS resume, not generic advice. If it's weak, say so.

TARGET ROLE: {target_role}

RESUME TEXT:
---
{resume_text}
---

Provide a structured analysis in the EXACT format below. Use headers exactly as shown.

---

## OVERALL SCORES
Overall Score: [X/100]
ATS Score: [X/100]
Recruiter Impression: [X/100]
Resume Strength: [weak/average/good/strong]

## CANDIDATE SUMMARY
[2-3 sentences describing who this person is based on the resume. Be honest.]

## BIGGEST PROBLEMS
[List 4-6 specific problems with this exact resume. Reference actual content.]
- Problem 1
- Problem 2
- Problem 3
- Problem 4

## ATS ISSUES
[List specific ATS problems found in THIS resume]
- Issue 1
- Issue 2
- Issue 3

## TECHNICAL SKILLS ANALYSIS
[Analyze the actual skills listed. Comment on depth, relevance to {target_role}, \
what's missing, what's outdated or too basic]

## PROJECT REVIEW
[For each project mentioned, give honest feedback on quality and recruiter perception. \
If projects look tutorial-based, say so.]

## EXPERIENCE ANALYSIS
[Analyze work experience. Comment on lack of metrics, weak verbs, unclear contributions. \
If fresher, comment on project/internship quality.]

## BULLET POINT IMPROVEMENTS
[Pick 2-3 weak bullet points and rewrite them]

Before: [exact bullet from resume]
Improved: [better version with metrics and impact]

Before: [exact bullet from resume]
Improved: [better version]

## MISSING KEYWORDS FOR {target_role.upper()}
[List 10-15 specific ATS keywords missing but important for {target_role}]

## RECRUITER PERSPECTIVE
[3-4 sentences as if you're a recruiter reading this resume out loud. Be honest.]

## HIRING CHANCES
Fresher Market Competitiveness: [low/medium/high]
[1-2 sentences on how this resume competes for {target_role} roles today]

## IMPROVEMENT ROADMAP
Priority 1 (Fix immediately):
- [specific action]

Priority 2 (Fix this week):
- [specific action]

Priority 3 (Fix this month):
- [specific action]

Projects to add:
- [specific project ideas for {target_role}]

Skills to learn:
- [specific skills missing for {target_role}]

---

Be specific to THIS resume. Avoid generic advice that applies to everyone.
"""
    return prompt


def get_keyword_prompt(resume_text, target_role):
    prompt = f"""Given this resume and the target role of {target_role}:

1. List the top 20 most important keywords/skills for a {target_role} job
2. Mark which ones appear in the resume (YES/NO)
3. Calculate keyword match percentage

Resume:
{resume_text[:2000]}

Format your response exactly as:
Keyword Match: [X]%

Keywords:
- keyword1: YES/NO
- keyword2: YES/NO
...
"""
    return prompt
