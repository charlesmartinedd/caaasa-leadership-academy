# Handoff Prompt — CAAASA PLN Video Production Script

Copy everything below this line and paste it into a new Claude Code session:

---

I need you to create a video production HTML review document AND a Python production script for the following CAAASA video. This is the same pipeline we use for our other CAAASA videos:

## Tech Stack
- **Video Generation**: OpenAI Sora 2 API (`sora-2` model, 720p, `$0.10/sec`)
  - API Key: `[REDACTED — stored in ~/.env as OPENAI_API_KEY]`
  - Endpoint: `POST https://api.openai.com/v1/videos` (multipart/form-data with fields: model, prompt, size="1280x720", seconds)
  - Poll: `GET https://api.openai.com/v1/videos/{id}` until status=completed
  - Download: `GET https://api.openai.com/v1/videos/{id}/content` with Accept: video/mp4
- **Narration**: ElevenLabs API
  - Voice: "Superintendant male voice.morgan freeman inspired" — ID: `HkA22KiGe8DgUA6JGVbq`
  - Model: `eleven_multilingual_v2`
  - Settings: stability=0.65, similarity_boost=0.80, style=0.30
  - API Key is in `~/.env` as `ELEVENLABS_API_KEY`
- **Music**: Jamendo API (free with attribution)
  - Search for warm, uplifting, human-centered instrumental that starts reflective and builds to hopeful
  - Client ID/Secret in `~/.env` as `JAMENDO_CLIENT_ID` / `JAMENDO_CLIENT_SECRET`
- **Assembly**: Remotion (later step)
- **Logo**: `C:/Users/MarieLexisDad/Downloads/CAAASA Logo.avif`

## Style Bible (append to EVERY Sora 2 video prompt)
```
Cinematic, warm amber and golden-hour lighting, shallow depth of field, authentic documentary style, African-American male and female adult leaders as protagonists, diverse students in background, warm orange and gold color grade with soft browns, steady gimbal movement, 24fps, intimate and human
```
Note: This PLN video uses warmer oranges/ambers vs the District Leadership video's navy/gold. The tone is more intimate and empathetic.

## CRITICAL REPRESENTATION RULE
- All adult leaders, administrators, principals, mentors MUST be African-American male or female
- Students and children can be diverse/multicultural
- The protagonist in every clip should be an African-American leader
- This is non-negotiable — enforce in every single prompt

## Project Directory
Create everything in: `01_Projects/Personal--CAAASA-Video-PLN/`

## What I Need You to Create

### 1. `production_review.html`
A beautiful dark-mode HTML review document (like the one at `01_Projects/Personal--CAAASA-Video/production_review.html` — you can read that for reference on the exact design pattern) that shows:
- Pipeline overview (4 phases)
- Cost estimate (clips × $0.10/sec for Sora 2)
- Voice & music selection
- The visual style bible
- Every scene with:
  - Exact narration text (DO NOT deviate from the script below)
  - Each video clip prompt with clip ID and duration
  - Text overlay timing
- Summary table of all clips
- Approval section at bottom

### 2. `production_script.py`
A complete Python production script (same pattern as `01_Projects/Personal--CAAASA-Video/production_script.py` — read it for reference) that:
- Has all narration text stored per scene
- Has all clip prompts with durations
- Uses Sora 2 API (not Veo) — the endpoint format is multipart/form-data
- Generates ElevenLabs narration per scene
- Downloads Jamendo music
- Polls and downloads Sora 2 clips
- Generates an assembly manifest JSON for Remotion
- Supports `--narration-only`, `--video-only`, `--clips 1A 2B`, `--cost` flags

### 3. Open the HTML in Chrome when done

## IMPORTANT RULES
- DO NOT deviate from the script text below — use it exactly as written for all narration
- Break each scene into 3-5 video clips of 2-5 seconds each
- Write detailed, specific Sora 2 prompts for each clip that match the Visual descriptions
- Always append the style bible to every video prompt
- The imagery style for this video is warmer and more intimate than corporate — show real struggles and real support
- Total clip seconds should be ~100-110s to cover the 90-120s video

## THE COMPLETE SCRIPT

### SCENE 1: OPENING (0:00-0:15)
**Visual:**
Open with site administrator alone in office late at night, looking tired but determined. Quick cuts showing the reality of site leadership: difficult conversations, crisis response, budget challenges, staff conflicts, parent concerns. Show them checking phone for answers, searching alone for solutions. Transition to same administrator in vibrant meeting with other site leaders, laughing and problem-solving together.

**Narration:**
"2 AM. You're awake, thinking about tomorrow's difficult parent meeting. The budget crisis. The teacher your need to support them. The initiative that's not working. You're searching for answers, but mostly? You're searching for someone who understands. Because site leadership isn't just hard—it's isolating. But what if it didn't have to be?"

---

### SCENE 2: WHO IT'S FOR (0:15-0:30)
**Visual:**
Show diverse African-American site administrators in their daily work: Elementary principal managing morning arrival and campus culture. High school assistant principal handling discipline and student support. Middle school principal leading instructional improvement. Dean coordinating interventions and family engagement. New administrator (1-2 years) looking uncertain. Veteran administrator (10+ years) still seeking fresh perspectives.

**Text overlays:** "New Site Administrators", "Veteran Principals", "Assistant Principals", "Deans & Site Coordinators", "Anyone Leading a School"

**Narration:**
"CAAASA's School Site Administrator Professional Learning Network is for every African-American site leader—whether you're in your first year feeling overwhelmed, or your fifteenth year needing fresh energy. Elementary, middle, or high school. Principal, assistant principal, or dean. If you're responsible for leading a school site, this network exists for you. Because you need more than professional development—you need a professional family."

---

### SCENE 3: WHY IT EXISTS (0:30-0:50)
**Visual:**
Montage contrasting isolation vs. community: Administrator alone researching best practices at midnight. Same person in network meeting getting instant solutions from peers. Administrator stuck on a problem. Network members sharing strategies that worked at their sites. Single leader carrying heavy burden. Network distributing wisdom and support. Show authentic moments: Site leaders being vulnerable about challenges. Celebrating each other's wins. Sharing resources and practical tools. Providing emotional support during tough times.

**Narration:**
"The network exists because site leadership shouldn't be lonely. Yes, you have district support and your staff. But they don't sit in your chair. They don't face your impossible decisions. They don't wake up at 2 AM with your worries. The PLN connects you with people who do. People who've handled the teacher performance issue you're facing. Who've navigated the parent conflict that's consuming you. Who've survived the budget cut, the enrollment decline, the staff turnover. They're not consultants—they're colleagues. And they're ready to walk with you."

---

### SCENE 4: WHAT THE NETWORK OPENS (0:50-1:20)
**Visual:**
Dynamic montage showing network benefits in action: Monthly learning sessions with relevant, practical content. Small group problem-solving circles. Text thread showing real-time support. Resource sharing (documents, templates, protocols). Site visits to each other's schools. Social events and relationship building. Mentoring relationships forming organically. Members presenting their innovations to each other. Celebrating promotions and achievements together. Supporting each other through difficult times.

**Text overlays (doors opening):** "Real-Time Problem Solving", "Proven Resources & Tools", "Authentic Peer Support", "Monthly Professional Learning", "Mentorship & Friendship", "Career Advancement Support", "Sanity & Sustainability"

**Narration:**
"The Professional Learning Network opens doors that transform your daily leadership and your career trajectory. You'll gain: Monthly learning sessions on what you actually need—not generic PD, but real strategies for the challenges you're facing right now. A text thread of peers who respond within minutes when you need advice, a resource, or just someone who gets it. Ready-to-use tools and protocols tested at schools like yours—not theory, but what's actually working. Mentors and thought partners who've been there and will tell you the truth, with love. A safe space to be vulnerable about your struggles without judgment—because we all have them. Support for your next career move, whether that's thriving in your current role or preparing for district leadership. And honestly? The reminder that you're not alone, you're not failing, and you're exactly the leader your school needs."

---

### SCENE 5: HOW THE PLN HELPS (1:20-1:40)
**Visual:**
Show specific, concrete examples of the network in action: Morning: Admin faces crisis, texts network, gets immediate advice. Afternoon: Uses protocol shared in last month's meeting. Evening: Video call with mentor from the network, working through a staff issue. Weekend: Attends network social event, recharges emotionally. Next week: Visits another member's school to see innovative practice. Month later: Presents their own success to the network, paying it forward. Show before/after: Stressed admin alone → Confident admin connected.

**Narration:**
"Here's how the PLN actually helps your daily leadership: It's Tuesday morning, your dean just quit, and you need coverage immediately. You text the network—within 10 minutes, three members share how they handled similar situations, one sends you their interim job description, another offers to talk through your restructuring plan. It's Thursday night, you're preparing for a difficult teacher evaluation meeting. Your PLN mentor—a veteran principal you met at the network—walks you through the conversation, helps you anticipate responses, reminds you to lead with compassion and clarity. It's Sunday, you're exhausted and questioning whether you can do this another week. You attend the network's social gathering—no agenda, just community—and you remember why you lead. You leave refueled. This isn't networking. This is survival. This is sustainability. This is sanity. This is how great site administrators stay great without burning out."

---

### SCENE 6: THE CAAASA COMMUNITY DIFFERENCE (1:40-1:50)
**Visual:**
Show warm, authentic moments: Network members embracing at gatherings. Diverse ages and experience levels learning from each other. Laughter and genuine connection. Supporting a member through a hard time. Celebrating promotions and achievements. Multi-generational mentorship happens naturally.

**Narration:**
"This is the CAAASA difference. We're not just a professional organization; we're a family. For over 20 years, we've been creating spaces where African-American site administrators can be their full selves, brilliant and struggling, confident and uncertain, leading and learning. You bring your excellence and your questions. You give your wisdom and receive support. You lead your school better because you're not leading alone."

---

### SCENE 7: CALL TO ACTION (1:50-2:00)
**Visual:**
Show the transformation: Administrator who opened the video alone, now surrounded by supportive colleagues, laughing and strategizing together. Group photo of network members, diverse, joyful, connected. Display membership information and QR code. End with the administrator back at their school, confidently handling a challenge, then checking their phone to see an encouraging message from a PLN member.

**Narration:**
"You're already doing the hardest job in education. Stop doing it alone. Join CAAASA's School Site Administrator Professional Learning Network. Your people are waiting. Your support system is ready. Your next challenge is easier with us."

**Final voice:**
"Because the best site administrators don't go it alone."

**Text on screen:** "CAAASA School Site Administrator PLN | Monthly Meetings | Real-Time Support | Lifelong Community | Join Now: www.CAAASA.org/leadershipacademy | (818) 217-6310 | #LeadTogether #SiteAdminPLN #CAAASA"
