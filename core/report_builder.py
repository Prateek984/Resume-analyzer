def predicted_score(score: int, edits_count: int) -> int:
    if edits_count <= 2:
        return min(score + 8, 95)
    elif edits_count <= 4:
        return min(score + 15, 95)
    else:
        return min(score + 22, 95)


def verdict(score: int) -> str:
    if score >= 85:
        return "You will likely get interview calls, but stronger positioning can increase response rate."
    elif score >= 70:
        return "You meet requirements, but recruiters may not notice your relevance quickly — many applications may be ignored."
    elif score >= 50:
        return "Your resume will likely be rejected in screening unless key gaps are fixed."
    else:
        return "Your resume will almost certainly be filtered out before human review."


def build_report(analysis: dict) -> str:
    if not analysis:
        return "Report could not be generated."

    score = analysis.get("ats_score", 0)
    chance = analysis.get("selection_chance", "unknown")

    report = []
    report.append("RESUME REVIEW RESULT")
    report.append("=" * 50)

    # 1️⃣ Verdict (Primary message)
    report.append("\nFINAL OUTCOME:")
    report.append(verdict(score))

    # 2️⃣ Score (supporting information)
    report.append(f"\nMatch Score: {score}/100")
    report.append(f"Shortlist Chance: {chance.upper()}")

    # 3️⃣ HERO SECTION — Copy paste fixes
    report.append("\n⭐ READY-TO-USE RESUME LINES:")
    report.append("(Add these under your project or experience section)")

    edits = analysis.get("resume_edits", [])

    if edits:
        for i, edit in enumerate(edits, 1):
            problem = edit.get("problem", "")
            rewrite = edit.get("rewrite_example", "").strip()

            if rewrite:
                report.append(f"\n{i}) Fix: {problem}")
                report.append(f"   → {rewrite}")
    else:
        report.append("No direct rewrite suggestions generated.")
    
    edits_count = len(edits)
    improved = predicted_score(score, edits_count)

    report.append("\nEXPECTED RESULT AFTER FIXES:")
    report.append(f"If you apply these changes, your match score can improve to ~{improved}/100")

    # 4️⃣ High impact fixes
    report.append("\nHIGH IMPACT FIXES (Do these first):")
    suggestions = analysis.get("suggestions", [])
    if suggestions:
        for s in suggestions[:3]:
            report.append(f"• {s}")
    else:
        report.append("No major fixes identified.")

    # 5️⃣ Why skipped (reasoning)
    report.append("\nWHY RECRUITERS MAY SKIP YOU:")
    weaknesses = analysis.get("weaknesses", [])
    if weaknesses:
        for w in weaknesses:
            report.append(f"• {w}")
    else:
        report.append("No critical weaknesses detected.")

    # Competition reasoning
    skipped = analysis.get("why_skipped_among_others", [])
    if skipped:
        report.append("\nIN COMPARISON TO OTHER CANDIDATES:")
        for r in skipped:
            report.append(f"• {r}")

    # 6️⃣ Strengths last (confidence close)
    report.append("\nWHAT IS ALREADY GOOD:")
    strengths = analysis.get("strengths", [])
    if strengths:
        for s in strengths:
            report.append(f"• {s}")
    else:
        report.append("No strengths detected.")

    report.append("\n" + "=" * 50)

    return "\n".join(report)