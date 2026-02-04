import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class UserProfileManager:
    def __init__(self):
        self.profile_dir = Path("profile")
        self.profile_file = self.profile_dir / "user_profile.json"
        self.profile_dir.mkdir(exist_ok=True)

    def load_profile(self) -> Dict[str, Any]:
        """Load user profile or create default if not exists."""
        if not self.profile_file.exists():
            return self._create_default_profile()

        try:
            with open(self.profile_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return self._create_default_profile()

    def save_profile(self, profile: Dict[str, Any]) -> None:
        """Save user profile to file."""
        with open(self.profile_file, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

    def _create_default_profile(self) -> Dict[str, Any]:
        """Create default user profile structure."""
        return {
            "created_at": datetime.now().isoformat(),
            "total_reviews": 0,
            "grammar_weaknesses": {},
            "translation_weaknesses": {},
            "vocabulary_gaps": [],
            "patterns": {
                "persistent_issues": [],
                "improving_areas": [],
                "new_issues": [],
                "resolved_issues": [],
            },
            "focus_areas": {"urgent": [], "practice": [], "maintain": []},
            "review_history": [],
        }

    def extract_weaknesses_from_review(
        self, review_content: str, task_type: str, date: str
    ) -> Dict[str, List[str]]:
        """Extract weaknesses from review content using keyword matching."""
        weaknesses = {"grammar": [], "translation": [], "vocabulary": []}

        # Grammar patterns
        grammar_patterns = {
            "articles": ["article", "a/an", "the"],
            "tenses": [
                "tense",
                "simple present",
                "simple past",
                "simple future",
                "parallelism",
            ],
            "prepositions": ["preposition", "because vs because of", "help me to"],
            "subject_verb": ["subject-verb", "agreement"],
            "comma_splice": ["comma splice", "koma untuk menyambung"],
        }

        # Translation patterns
        translation_patterns = {
            "incomplete_translation": ["tertinggal", "tidak diterjemahkan", "I", "and"],
            "time_expressions": ["time", "sore nanti", "this afternoon", "tomorrow"],
            "formal_informal": ["formal", "alignment", "penyelarasan"],
        }

        # Vocabulary patterns
        vocab_patterns = ["facilitate", "alignment", "mitigate", "proactive"]

        content_lower = review_content.lower()

        # Extract grammar weaknesses
        for weakness_type, keywords in grammar_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                weaknesses["grammar"].append(weakness_type)

        # Extract translation weaknesses
        for weakness_type, keywords in translation_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                weaknesses["translation"].append(weakness_type)

        # Extract vocabulary gaps
        for vocab in vocab_patterns:
            if vocab in content_lower:
                weaknesses["vocabulary"].append(vocab)

        return weaknesses

    def update_weaknesses(self, review_content: str, task_type: str, date: str) -> None:
        """Update user profile with new weaknesses from review."""
        profile = self.load_profile()
        weaknesses = self.extract_weaknesses_from_review(
            review_content, task_type, date
        )

        # Update grammar weaknesses
        for grammar_issue in weaknesses["grammar"]:
            if grammar_issue not in profile["grammar_weaknesses"]:
                profile["grammar_weaknesses"][grammar_issue] = {
                    "total_mistakes": 0,
                    "recent_mistakes": 0,
                    "trend": "new",
                    "history": [],
                }

            profile["grammar_weaknesses"][grammar_issue]["total_mistakes"] += 1
            profile["grammar_weaknesses"][grammar_issue]["recent_mistakes"] += 1
            profile["grammar_weaknesses"][grammar_issue]["history"].append(
                {"date": date, "count": 1, "task_type": task_type}
            )

        # Update translation weaknesses
        for trans_issue in weaknesses["translation"]:
            if trans_issue not in profile["translation_weaknesses"]:
                profile["translation_weaknesses"][trans_issue] = {
                    "total_mistakes": 0,
                    "recent_mistakes": 0,
                    "trend": "new",
                    "history": [],
                }

            profile["translation_weaknesses"][trans_issue]["total_mistakes"] += 1
            profile["translation_weaknesses"][trans_issue]["recent_mistakes"] += 1
            profile["translation_weaknesses"][trans_issue]["history"].append(
                {"date": date, "count": 1, "task_type": task_type}
            )

        # Update vocabulary gaps
        for vocab in weaknesses["vocabulary"]:
            existing_vocab = next(
                (v for v in profile["vocabulary_gaps"] if v["word"] == vocab), None
            )
            if existing_vocab:
                existing_vocab["missed_count"] += 1
                existing_vocab["last_seen"] = date
            else:
                profile["vocabulary_gaps"].append(
                    {
                        "word": vocab,
                        "context": "workplace_communication",
                        "missed_count": 1,
                        "last_seen": date,
                    }
                )

        # Update review history
        profile["review_history"].append(
            {
                "date": date,
                "task_type": task_type,
                "weaknesses_found": len(weaknesses["grammar"])
                + len(weaknesses["translation"])
                + len(weaknesses["vocabulary"]),
            }
        )

        profile["total_reviews"] += 1

        # Recalculate patterns and focus areas
        self._update_patterns(profile)
        self._update_focus_areas(profile)

        self.save_profile(profile)

    def _update_patterns(self, profile: Dict[str, Any]) -> None:
        """Update patterns based on weakness history."""
        persistent_issues = []
        improving_areas = []
        new_issues = []

        # Check grammar weaknesses
        for issue, data in profile["grammar_weaknesses"].items():
            if data["total_mistakes"] >= 3:
                persistent_issues.append(issue)
            elif len(data["history"]) == 1:
                new_issues.append(issue)
            elif self._is_improving(data["history"]):
                improving_areas.append(issue)

        # Check translation weaknesses
        for issue, data in profile["translation_weaknesses"].items():
            if data["total_mistakes"] >= 3:
                persistent_issues.append(issue)
            elif len(data["history"]) == 1:
                new_issues.append(issue)
            elif self._is_improving(data["history"]):
                improving_areas.append(issue)

        profile["patterns"]["persistent_issues"] = persistent_issues
        profile["patterns"]["improving_areas"] = improving_areas
        profile["patterns"]["new_issues"] = new_issues

    def _update_focus_areas(self, profile: Dict[str, Any]) -> None:
        """Update focus areas based on current weaknesses."""
        urgent = []
        practice = []
        maintain = []

        # Grammar focus
        for issue, data in profile["grammar_weaknesses"].items():
            if data["total_mistakes"] >= 5:
                urgent.append(issue)
            elif data["total_mistakes"] >= 2:
                practice.append(issue)
            else:
                maintain.append(issue)

        # Translation focus
        for issue, data in profile["translation_weaknesses"].items():
            if data["total_mistakes"] >= 3:
                urgent.append(issue)
            elif data["total_mistakes"] >= 2:
                practice.append(issue)

        profile["focus_areas"]["urgent"] = urgent[:3]  # Top 3 urgent
        profile["focus_areas"]["practice"] = practice[:5]  # Top 5 practice
        profile["focus_areas"]["maintain"] = maintain[:3]  # Top 3 maintain

    def _is_improving(self, history: List[Dict]) -> bool:
        """Check if user is improving in this area."""
        if len(history) < 3:
            return False

        recent_3 = history[-3:]
        return all(
            recent_3[i]["count"] >= recent_3[i + 1]["count"]
            for i in range(len(recent_3) - 1)
        )

    def get_user_context_for_ai(self) -> str:
        """Generate context string for AI prompts."""
        profile = self.load_profile()

        if profile["total_reviews"] == 0:
            return "New user - no previous weaknesses identified."

        context_parts = []

        # Urgent focus areas
        if profile["focus_areas"]["urgent"]:
            context_parts.append(
                f"URGENT areas to focus on: {', '.join(profile['focus_areas']['urgent'])}"
            )

        # Persistent issues
        if profile["patterns"]["persistent_issues"]:
            context_parts.append(
                f"Persistent issues (3+ mistakes): {', '.join(profile['patterns']['persistent_issues'])}"
            )

        # Vocabulary gaps
        if profile["vocabulary_gaps"]:
            vocab_words = [v["word"] for v in profile["vocabulary_gaps"][:5]]
            context_parts.append(f"Vocabulary gaps: {', '.join(vocab_words)}")

        # Recent improvements
        if profile["patterns"]["improving_areas"]:
            context_parts.append(
                f"Improving areas: {', '.join(profile['patterns']['improving_areas'])}"
            )

        return (
            "\n".join(context_parts)
            if context_parts
            else "User showing good progress overall."
        )
