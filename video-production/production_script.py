"""
CAAASA Aspiring District Office Administrator's Academy
Full Production Script — Sora 2 + ElevenLabs + Jamendo + Remotion

Usage:
  python production_script.py                  # Run full pipeline
  python production_script.py --narration-only # Generate narration only
  python production_script.py --video-only     # Generate video clips only
  python production_script.py --clips 1A 2B    # Generate specific clips
"""

import os, sys, time, json, argparse, requests
from pathlib import Path

# ── CONFIG ──────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
VOICE_ID = "HkA22KiGe8DgUA6JGVbq"  # Superintendent male voice (Morgan Freeman inspired)
VOICE_MODEL = "eleven_multilingual_v2"

PROJECT_DIR = Path(__file__).parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
CLIPS_DIR = OUTPUT_DIR / "clips"
NARRATION_DIR = OUTPUT_DIR / "narration"
MUSIC_DIR = OUTPUT_DIR / "music"

SORA_MODEL = "sora-2"        # $0.10/sec at 720p
SORA_SIZE = "1280x720"       # 720p
SORA_API_URL = "https://api.openai.com/v1/videos"

# ── STYLE BIBLE ─────────────────────────────────────────────────────────────
# Appended to EVERY video prompt for visual consistency across all 26 clips.
# REPRESENTATION RULE: All adult leaders MUST be African-American. Students can be diverse.
STYLE_SUFFIX = (
    "Cinematic 4K, warm golden-hour lighting, shallow depth of field, "
    "anamorphic lens flare, professional corporate documentary style, "
    "African-American male and female adult leaders as protagonists, "
    "diverse students in background, muted navy and gold color grade, "
    "steady dolly or gimbal movement, 24fps film grain"
)

# ── NARRATION SCRIPT ────────────────────────────────────────────────────────
# Each scene's narration text, exactly as written in the approved script.
# ElevenLabs will generate one MP3 per scene.
NARRATION = {
    "scene1": {
        "title": "OPENING",
        "time": "0:00-0:15",
        "text": (
            "You've transformed your school. You've built a culture of excellence. "
            "You've proven you can lead a building. But late at night, when you're "
            "reviewing your school improvement plan, you know the real barriers to "
            "student success aren't just happening on your campus; they're systemic. "
            "And you're ready to solve them at the district level."
        ),
    },
    "scene2": {
        "title": "WHO IT'S FOR",
        "time": "0:15-0:30",
        "text": (
            "CAAASA's Aspiring District Office Administrator's Academy is designed "
            "for you, principals, assistant principals, and site coordinators who've "
            "mastered building-level leadership and are ready to scale your impact "
            "across an entire district. You've proven yourself at the site. Now it's "
            "time to position yourself for Director of Curriculum, Director of "
            "Student Services, Executive Director roles, Assistant Superintendent, "
            "or other district cabinet positions. This is your pathway from managing "
            "one school to transforming many."
        ),
    },
    "scene3": {
        "title": "WHY IT EXISTS",
        "time": "0:30-0:50",
        "text": (
            "Because running an excellent school doesn't automatically prepare you "
            "for district-level leadership. The leap from site to district office "
            "requires a fundamentally different skill set, systems thinking instead "
            "of building management, policy instead of procedures, district-wide "
            "strategy instead of campus culture. The Academy exists to accelerate "
            "that transition. We give you the frameworks, the competencies, and "
            "the network, to compete for district positions and excel in them from "
            "day one."
        ),
    },
    "scene4": {
        "title": "WHAT DOORS IT OPENS",
        "time": "0:50-1:20",
        "text": (
            "The Academy opens every door to district-level leadership. You'll master: "
            "Systems-level thinking, how to analyze and improve performance across "
            "multiple schools, not just one building. District finance and resource "
            "allocation, understanding multi-million dollar budgets, collective "
            "bargaining, and strategic investments. Policy development and governance, "
            "working effectively with boards, unions, and community stakeholders at "
            "scale. Leading leaders, coaching and supervising principals while building "
            "high-performing district teams. Data-driven district strategy. And the "
            "competitive positioning that makes superintendents and boards see you not "
            "just as a great principal, but as their next cabinet member. Our graduates "
            "aren't just applying for district roles, they're being recruited for them."
        ),
    },
    "scene6": {
        "title": "THE CAAASA DISTRICT LEADERSHIP ADVANTAGE",
        "time": "1:45-1:55",
        "text": (
            "This is the CAAASA advantage. We've been developing African-American "
            "educational leaders for district impact for over 10 years. Our alumni "
            "hold cabinet positions in districts across the state, and they started "
            "exactly where you are now. You'll learn from sitting superintendents, "
            "assistant superintendents, and executive directors who understand both "
            "the opportunities and obstacles you'll face. Our network doesn't just "
            "prepare you, it connects you to the opportunities that can transform "
            "your career."
        ),
    },
    "scene7": {
        "title": "CALL TO ACTION",
        "time": "1:55-2:05",
        "text": (
            "You've proven you can lead a school. Now prove you can transform a "
            "district. Join CAAASA's Aspiring District Office Administrators' Academy. "
            "Master the systems. Learn the tools. Secure the position. Your district "
            "is waiting for leaders like you, leaders who combine site-level credibility "
            "with district-level vision."
        ),
    },
    "scene7_final": {
        "title": "FINAL VOICE",
        "time": "2:03-2:05",
        "text": (
            "From principal to cabinet. From campus to district. Your impact "
            "multiplies here."
        ),
    },
}

# ── VIDEO CLIP PROMPTS ──────────────────────────────────────────────────────
# Each clip is mapped to a scene, with duration and generation prompt.
# Style suffix is auto-appended.
CLIPS = {
    # ── SCENE 1: OPENING (0:00-0:15) ──
    "1A": {
        "scene": "scene1",
        "duration": 4,
        "prompt": (
            "An African-American male school principal in a navy suit walks through "
            "a modern school campus at golden sunrise, greeting students with a warm "
            "smile. Students wave back. Camera follows from behind in a slow tracking shot."
        ),
    },
    "1B": {
        "scene": "scene1",
        "duration": 3,
        "prompt": (
            "Quick montage: An African-American woman principal leads a faculty meeting "
            "in a bright conference room, gestures toward a whiteboard with data charts. "
            "Cut to: coaching a teacher in a classroom doorway. Professional, warm lighting."
        ),
    },
    "1C": {
        "scene": "scene1",
        "duration": 4,
        "prompt": (
            "An African-American male administrator sits at the far end of a large "
            "district boardroom table, observing other leaders discussing strategy. "
            "He takes notes. Camera slowly pushes in on his thoughtful expression."
        ),
    },
    "1D": {
        "scene": "scene1",
        "duration": 4,
        "prompt": (
            "Close-up of an African-American male school leader standing outside, "
            "looking toward a modern glass district office building in the distance. "
            "Wind gently moves his tie. Lens flare from the setting sun. "
            "Aspirational, contemplative mood."
        ),
    },

    # ── SCENE 2: WHO IT'S FOR (0:15-0:30) ──
    "2A": {
        "scene": "scene2",
        "duration": 3,
        "prompt": (
            "An African-American woman elementary school principal walks confidently "
            "through a colorful elementary school hallway, tablet in hand, smiling at "
            "students' artwork on the walls. Slow dolly forward."
        ),
    },
    "2B": {
        "scene": "scene2",
        "duration": 3,
        "prompt": (
            "An African-American male high school assistant principal stands at a "
            "command center with multiple monitors showing schedules and data. He "
            "coordinates with staff on a walkie-talkie. Dynamic, competent energy."
        ),
    },
    "2C": {
        "scene": "scene2",
        "duration": 4,
        "prompt": (
            "An African-American woman middle school principal presents a data "
            "slideshow to a small group of district leaders in a modern conference "
            "room. She gestures confidently at rising achievement graphs. Professional lighting."
        ),
    },
    "2D": {
        "scene": "scene2",
        "duration": 5,
        "prompt": (
            "A diverse group of African-American site administrators, men and women "
            "of various ages, stand together in a modern school lobby, arms crossed "
            "confidently, looking directly at camera. Slow push-in. Powerful, unified."
        ),
    },

    # ── SCENE 3: WHY IT EXISTS (0:30-0:50) ──
    "3A": {
        "scene": "scene3",
        "duration": 3,
        "prompt": (
            "An African-American male principal sits at his desk late at night, "
            "reading a district-level job description on his laptop screen. His "
            "expression shows determination mixed with uncertainty. Desk lamp warm glow."
        ),
    },
    "3B": {
        "scene": "scene3",
        "duration": 4,
        "prompt": (
            "Split-screen visual concept: left side shows a principal managing one "
            "school building, right side shows a complex web of interconnected "
            "schools, departments, and systems. Transition from simple to complex. "
            "Abstract, clean."
        ),
    },
    "3C": {
        "scene": "scene3",
        "duration": 3,
        "prompt": (
            "An interview panel of three superintendents and board members sits "
            "behind a long table, reviewing candidate folders. Professional boardroom "
            "setting. Shot from the candidate's perspective approaching the table."
        ),
    },
    "3D": {
        "scene": "scene3",
        "duration": 5,
        "prompt": (
            "A cohort of 12 African-American site administrators engaged in a "
            "workshop, working on district-level case studies at round tables. A "
            "senior district leader facilitates. Energetic, collaborative atmosphere. "
            "Overhead angle transitioning to eye level."
        ),
    },
    "3E": {
        "scene": "scene3",
        "duration": 5,
        "prompt": (
            "An African-American woman administrator stands at a large whiteboard "
            "covered in systems maps and flowcharts. She steps back, seeing the full "
            "picture, and nods with growing confidence. Camera pulls back to reveal "
            "the scope of her thinking."
        ),
    },

    # ── SCENE 4: WHAT DOORS IT OPENS (0:50-1:20) ──
    "4A": {
        "scene": "scene4",
        "duration": 5,
        "prompt": (
            "An African-American woman presents confidently to a school board in a "
            "formal boardroom. Board members nod approvingly. Large screen behind "
            "her shows a district strategic plan. Wide shot with shallow depth of field."
        ),
    },
    "4B": {
        "scene": "scene4",
        "duration": 4,
        "prompt": (
            "An African-American male district leader leads a cabinet meeting at a "
            "large oval table. The superintendent sits at the head. He gestures toward "
            "a projected district-wide achievement dashboard. Authoritative, respected."
        ),
    },
    "4C": {
        "scene": "scene4",
        "duration": 5,
        "prompt": (
            "Close-up of hands working on a complex district budget spreadsheet on a "
            "large monitor, then pulling back to reveal an African-American male "
            "executive director analyzing multi-million dollar resource allocation "
            "across schools."
        ),
    },
    "4D": {
        "scene": "scene4",
        "duration": 4,
        "prompt": (
            "An African-American woman Director of Student Services coaches a group "
            "of principals in a professional development session. She uses a large "
            "touchscreen showing equity data across multiple school sites."
        ),
    },
    "4E": {
        "scene": "scene4",
        "duration": 5,
        "prompt": (
            "An African-American male candidate sits confidently in a district-level "
            "interview, leaning forward with composed body language. Three interviewers "
            "across the table smile and take notes. Professional, warm."
        ),
    },
    "4F": {
        "scene": "scene4",
        "duration": 5,
        "prompt": (
            "The same candidate from the interview is now in a corner office with a "
            "nameplate reading Executive Director. He places a family photo on his new "
            "desk and looks out the window at the district below. Triumphant, earned moment."
        ),
    },

    # ── SCENE 6: THE CAAASA ADVANTAGE (1:45-1:55) ──
    "6A": {
        "scene": "scene6",
        "duration": 3,
        "prompt": (
            "A cohort of African-American site administrators work intensely on a "
            "district-level simulation exercise at a U-shaped conference table. "
            "Whiteboards filled with strategy maps surround them. Focused, elite atmosphere."
        ),
    },
    "6B": {
        "scene": "scene6",
        "duration": 3,
        "prompt": (
            "One-on-one mentoring: A senior African-American district superintendent "
            "mentors a younger site administrator in a quiet office. They review a "
            "career development plan together. Warm, personal, intergenerational."
        ),
    },
    "6C": {
        "scene": "scene6",
        "duration": 2,
        "prompt": (
            "A group of administrators tour a district office, walking through corridors "
            "past department doors labeled Curriculum and Instruction, Human Resources, "
            "Business Services. They observe and take notes. Tracking shot."
        ),
    },
    "6D": {
        "scene": "scene6",
        "duration": 3,
        "prompt": (
            "A cohort celebrates as one member holds up a letter, a district office job "
            "offer. Group hugs, applause, genuine emotion. Joyful, authentic, triumphant."
        ),
    },

    # ── SCENE 7: CALL TO ACTION (1:55-2:05) ──
    "7A": {
        "scene": "scene7",
        "duration": 3,
        "prompt": (
            "An African-American male administrator is ceremonially welcomed into a "
            "district cabinet meeting. He takes his seat at the table for the first "
            "time. Other cabinet members shake his hand. Dignified, milestone moment."
        ),
    },
    "7B": {
        "scene": "scene7",
        "duration": 4,
        "prompt": (
            "A cohort of 15 diverse African-American site leaders stands together on "
            "the steps of a modern educational building, confident and ready. "
            "Slow-motion push-in. Golden hour backlighting. Iconic group shot."
        ),
    },
    "7C": {
        "scene": "scene7",
        "duration": 3,
        "prompt": (
            "The new district administrator contributes an idea at the cabinet table. "
            "His laptop shows an AI-powered analytics dashboard. The superintendent "
            "nods. He has arrived. Camera slowly pulls back through the boardroom "
            "window. Closing shot."
        ),
    },
}

# ── TEXT OVERLAYS (for Remotion) ────────────────────────────────────────────
TEXT_OVERLAYS = {
    "scene2": {
        "entries": [
            {"text": "Building Principals", "start_sec": 16, "duration": 3},
            {"text": "Assistant Principals", "start_sec": 19, "duration": 3},
            {"text": "Deans & Coordinators", "start_sec": 22, "duration": 3},
            {"text": "Site Leaders Ready for District Impact", "start_sec": 25, "duration": 5},
        ],
        "style": "fade_in_bottom",
    },
    "scene4": {
        "entries": [
            {"text": "Assistant Superintendent", "start_sec": 52, "duration": 4},
            {"text": "Executive Director Roles", "start_sec": 56, "duration": 4},
            {"text": "Director of Curriculum/Instruction", "start_sec": 60, "duration": 4},
            {"text": "Director of Student Services", "start_sec": 64, "duration": 4},
            {"text": "Chief Academic Officer", "start_sec": 68, "duration": 4},
            {"text": "District-Wide Impact", "start_sec": 72, "duration": 4},
        ],
        "style": "door_open_wipe",
    },
    "scene7_cta": {
        "entries": [
            {"text": "CAAASA Aspiring District Office Administrator's Academy", "start_sec": 118, "duration": 5},
            {"text": "For Site Leaders Ready for District Impact", "start_sec": 118, "duration": 5},
            {"text": "Applications Open Now", "start_sec": 120, "duration": 5},
            {"text": "Visit: www.CAAASA.org/leadershipacademy", "start_sec": 120, "duration": 5},
            {"text": "(818) 217-6310", "start_sec": 120, "duration": 5},
            {"text": "#FromSiteToDistrict  #DistrictLeadership  #CAAASA", "start_sec": 122, "duration": 3},
        ],
        "style": "final_card",
    },
}

# ── MUSIC ───────────────────────────────────────────────────────────────────
BACKGROUND_MUSIC = {
    "track": "Spirit of Success",
    "artist": "Alumo",
    "jamendo_id": "1284462",
    "duration_sec": 166,
    "file": "music/bg_music_spirit_of_success.mp3",
    "volume": 0.15,  # Duck under narration
    "volume_no_narration": 0.40,  # Between scenes / transitions
}

# ── LOGO ────────────────────────────────────────────────────────────────────
LOGO = {
    "file": "C:/Users/MarieLexisDad/Downloads/CAAASA Logo.avif",
    "position": "top_right",
    "opacity": 0.85,
    "scenes": ["scene7_cta"],  # Show logo on final CTA card
}


# ═══════════════════════════════════════════════════════════════════════════
# PIPELINE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def setup_dirs():
    """Create output directories."""
    for d in [OUTPUT_DIR, CLIPS_DIR, NARRATION_DIR, MUSIC_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    print(f"Output directories ready: {OUTPUT_DIR}")


def generate_narration():
    """Generate narration MP3 for each scene via ElevenLabs API."""
    import requests

    if not ELEVENLABS_API_KEY:
        print("ERROR: ELEVENLABS_API_KEY not set in environment")
        return False

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }

    for scene_id, scene in NARRATION.items():
        outfile = NARRATION_DIR / f"{scene_id}.mp3"
        if outfile.exists() and outfile.stat().st_size > 1000:
            print(f"  [skip] {scene_id} already exists ({outfile.stat().st_size:,} bytes)")
            continue

        print(f"  Generating {scene_id}: {scene['title']} ({scene['time']})...")
        payload = {
            "text": scene["text"],
            "model_id": VOICE_MODEL,
            "voice_settings": {
                "stability": 0.65,
                "similarity_boost": 0.80,
                "style": 0.30,
            },
        }

        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            outfile.write_bytes(resp.content)
            print(f"    Saved: {outfile} ({len(resp.content):,} bytes)")
        else:
            print(f"    ERROR {resp.status_code}: {resp.text[:200]}")
            return False

    print("Narration generation complete.")
    return True


def generate_video_clips(clip_ids=None):
    """Generate video clips via OpenAI Sora 2 API."""
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    targets = clip_ids if clip_ids else list(CLIPS.keys())

    print(f"\n  Model: {SORA_MODEL}")
    print(f"  Clips to generate: {len(targets)}")
    total_sec = sum(CLIPS[c]["duration"] for c in targets)
    print(f"  Total video seconds: {total_sec}s")
    print(f"  Estimated cost: ${total_sec * 0.10:.2f}\n")

    # Submit all clip generation requests
    submitted = {}
    for clip_id in targets:
        clip = CLIPS[clip_id]
        outfile = CLIPS_DIR / f"{clip_id}.mp4"

        if outfile.exists() and outfile.stat().st_size > 10000:
            print(f"  [skip] {clip_id} already exists ({outfile.stat().st_size:,} bytes)")
            continue

        full_prompt = f"{clip['prompt']} {STYLE_SUFFIX}"
        print(f"  Submitting {clip_id} ({clip['duration']}s): {clip['prompt'][:70]}...")

        try:
            resp = requests.post(
                SORA_API_URL,
                headers=headers,
                data={
                    "model": SORA_MODEL,
                    "prompt": full_prompt,
                    "size": SORA_SIZE,
                    "seconds": str(clip["duration"]),
                },
            )
            result = resp.json()
            if "id" in result:
                submitted[clip_id] = result["id"]
                print(f"    Queued: {result['id']} (status: {result.get('status')})")
            else:
                print(f"    ERROR: {result}")
            # Small delay between submissions to avoid rate limits
            time.sleep(2)
        except Exception as e:
            print(f"    ERROR submitting {clip_id}: {e}")

    # Poll all operations until complete
    if submitted:
        print(f"\n  Waiting for {len(submitted)} clips to generate...")
        pending = dict(submitted)
        max_wait = 600  # 10 minutes max
        elapsed = 0

        while pending and elapsed < max_wait:
            time.sleep(15)
            elapsed += 15
            still_pending = {}

            for clip_id, video_id in pending.items():
                try:
                    resp = requests.get(
                        f"{SORA_API_URL}/{video_id}",
                        headers=headers,
                    )
                    data = resp.json()
                    status = data.get("status", "unknown")
                    progress = data.get("progress", 0)

                    if status == "completed":
                        # Download the video
                        outfile = CLIPS_DIR / f"{clip_id}.mp4"
                        dl_resp = requests.get(
                            f"{SORA_API_URL}/{video_id}/content",
                            headers={**headers, "Accept": "video/mp4"},
                        )
                        outfile.write_bytes(dl_resp.content)
                        print(f"    {clip_id} complete! ({outfile.stat().st_size:,} bytes)")
                    elif status == "failed":
                        print(f"    {clip_id} FAILED: {data.get('error')}")
                    else:
                        still_pending[clip_id] = video_id
                except Exception as e:
                    print(f"    {clip_id} poll error: {e}")
                    still_pending[clip_id] = video_id

            pending = still_pending
            if pending:
                clip_list = list(pending.keys())
                print(f"    [{elapsed}s] Waiting on {len(pending)}: {clip_list[:5]}{'...' if len(clip_list)>5 else ''}")

        if pending:
            print(f"  WARNING: {len(pending)} clips timed out: {list(pending.keys())}")

    print("Video clip generation complete.")
    return True


def download_music():
    """Download background music from Jamendo."""
    import requests

    outfile = MUSIC_DIR / "bg_music_spirit_of_success.mp3"
    if outfile.exists() and outfile.stat().st_size > 100000:
        print(f"  [skip] Music already downloaded ({outfile.stat().st_size:,} bytes)")
        return True

    jamendo_id = BACKGROUND_MUSIC["jamendo_id"]
    client_id = os.environ.get("JAMENDO_CLIENT_ID", "")
    if not client_id:
        print("ERROR: JAMENDO_CLIENT_ID not set")
        return False

    api_url = f"https://api.jamendo.com/v3.0/tracks/?client_id={client_id}&format=json&id={jamendo_id}"
    data = requests.get(api_url).json()
    download_url = data["results"][0]["audiodownload"]

    print(f"  Downloading: {BACKGROUND_MUSIC['track']} by {BACKGROUND_MUSIC['artist']}...")
    resp = requests.get(download_url)
    outfile.write_bytes(resp.content)
    print(f"  Saved: {outfile} ({len(resp.content):,} bytes)")
    return True


def generate_assembly_manifest():
    """Generate a JSON manifest for Remotion to consume."""
    manifest = {
        "title": "CAAASA Aspiring District Office Administrator's Academy",
        "duration_target_sec": 125,
        "fps": 30,
        "resolution": {"width": 1920, "height": 1080},
        "scenes": [],
        "music": BACKGROUND_MUSIC,
        "logo": LOGO,
    }

    scene_order = ["scene1", "scene2", "scene3", "scene4", "scene6", "scene7"]
    current_time = 0.0

    for scene_id in scene_order:
        scene_clips = [
            {"clip_id": cid, **cdata}
            for cid, cdata in CLIPS.items()
            if cdata["scene"] == scene_id
        ]

        scene_data = {
            "scene_id": scene_id,
            "narration": NARRATION.get(scene_id, {}),
            "narration_file": f"narration/{scene_id}.mp3",
            "start_sec": current_time,
            "clips": [],
            "text_overlays": TEXT_OVERLAYS.get(scene_id, {}).get("entries", []),
            "overlay_style": TEXT_OVERLAYS.get(scene_id, {}).get("style", "fade_in"),
        }

        for clip in scene_clips:
            scene_data["clips"].append({
                "clip_id": clip["clip_id"],
                "file": f"clips/{clip['clip_id']}.mp4",
                "duration": clip["duration"],
                "start_in_scene": current_time - scene_data["start_sec"],
                "prompt": clip["prompt"],
            })
            current_time += clip["duration"]

        scene_data["end_sec"] = current_time
        manifest["scenes"].append(scene_data)

    # Add final voice scene7_final
    if "scene7_final" in NARRATION:
        manifest["scenes"][-1]["final_narration_file"] = "narration/scene7_final.mp3"

    # Add CTA overlays to last scene
    if "scene7_cta" in TEXT_OVERLAYS:
        manifest["scenes"][-1]["cta_overlays"] = TEXT_OVERLAYS["scene7_cta"]["entries"]

    manifest["total_clip_seconds"] = current_time

    outfile = OUTPUT_DIR / "assembly_manifest.json"
    outfile.write_text(json.dumps(manifest, indent=2))
    print(f"  Manifest saved: {outfile}")
    return manifest


# ═══════════════════════════════════════════════════════════════════════════
# COST SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

def print_cost_summary():
    total_clip_sec = sum(c["duration"] for c in CLIPS.values())
    narration_chars = sum(len(s["text"]) for s in NARRATION.values())

    sora_cost = total_clip_sec * 0.10  # $0.10/sec for sora-2 at 720p
    # ElevenLabs: ~$0.30 per 1K chars on Creator plan
    el_cost = (narration_chars / 1000) * 0.30
    jamendo_cost = 0.00  # Free with attribution

    print("\n" + "=" * 60)
    print("PRODUCTION COST ESTIMATE")
    print("=" * 60)
    print(f"  Video: {len(CLIPS)} clips, {total_clip_sec}s total")
    print(f"    Sora 2 (720p): ${sora_cost:.2f}")
    print(f"  Narration: {len(NARRATION)} scenes, {narration_chars:,} chars")
    print(f"    ElevenLabs: ~${el_cost:.2f}")
    print(f"  Music: Jamendo (free with attribution)")
    print(f"    Jamendo: ${jamendo_cost:.2f}")
    print(f"  -----------------------------")
    print(f"  TOTAL ESTIMATE: ${sora_cost + el_cost + jamendo_cost:.2f}")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="CAAASA Video Production Pipeline")
    parser.add_argument("--narration-only", action="store_true")
    parser.add_argument("--video-only", action="store_true")
    parser.add_argument("--clips", nargs="+", help="Generate specific clips (e.g., 1A 2B 4F)")
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--cost", action="store_true", help="Show cost estimate only")
    args = parser.parse_args()

    print("=" * 60)
    print("CAAASA District Leadership Academy — Video Production")
    print("=" * 60)

    if args.cost:
        print_cost_summary()
        return

    setup_dirs()
    print_cost_summary()

    if args.manifest_only:
        print("\n[MANIFEST]")
        generate_assembly_manifest()
        return

    if not args.video_only:
        print("\n[NARRATION] Generating voiceovers...")
        generate_narration()

    if not args.narration_only:
        print("\n[MUSIC] Downloading background track...")
        download_music()

        print("\n[VIDEO] Generating Veo 3.1 clips...")
        generate_video_clips(args.clips)

    print("\n[MANIFEST] Building assembly manifest...")
    generate_assembly_manifest()

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print(f"  Outputs: {OUTPUT_DIR}")
    print(f"  Next step: Build Remotion composition from assembly_manifest.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
