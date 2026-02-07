import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict


class VocabularyDatabase:
    def __init__(self):
        self.db_path = Path("profile") / "vocabulary_mastery.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database with tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main vocabulary table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                word_type TEXT,
                total_reviews INTEGER DEFAULT 0,
                accuracy_score INTEGER DEFAULT 0,
                last_reviewed TEXT,
                source TEXT DEFAULT 'task',
                meaning TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Forms mastery tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS forms_mastery (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_id INTEGER NOT NULL,
                form_type TEXT NOT NULL,
                form_value TEXT,
                form_meaning TEXT,
                is_mastered BOOLEAN DEFAULT 0,
                FOREIGN KEY (word_id) REFERENCES vocabulary(id),
                UNIQUE(word_id, form_type)
            )
        """)

        # Review history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_id INTEGER NOT NULL,
                review_date TEXT NOT NULL,
                accuracy INTEGER NOT NULL,
                FOREIGN KEY (word_id) REFERENCES vocabulary(id)
            )
        """)

        # Create indexes for fast queries
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_accuracy ON vocabulary(accuracy_score)"
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_word ON vocabulary(word)")

        conn.commit()
        conn.close()

    def add_vocabulary(
        self,
        word: str,
        word_type: Optional[str] = None,
        meaning: Optional[str] = None,
        source: str = "manual",
    ) -> None:
        """Add new vocabulary from external source (book, article, etc).

        Args:
            word: The vocabulary word
            word_type: Type of word (n/noun, v/verb, adj/adjective, adv/adverb)
            meaning: Indonesian meaning
            source: Source of the word (manual, task, book, article)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().isoformat()
        word_lower = word.lower()

        try:
            cursor.execute(
                """
                INSERT INTO vocabulary (word, word_type, meaning, source, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (word_lower, word_type, meaning, source, now, now),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            # Word already exists, update meaning/type if provided
            updates = []
            params = []

            if meaning:
                updates.append("meaning = ?")
                params.append(meaning)
            if word_type:
                updates.append("word_type = ?")
                params.append(word_type)

            if updates:
                updates.append("updated_at = ?")
                params.append(now)
                params.append(word_lower)

                cursor.execute(
                    f"""
                    UPDATE vocabulary 
                    SET {", ".join(updates)}
                    WHERE word = ?
                    """,
                    params,
                )
                conn.commit()
        finally:
            conn.close()

    def update_vocabulary_mastery(
        self,
        word: str,
        accuracy_score: int,
        forms_correct: list[str],
        forms_weak: list[str],
        date: str,
        word_type: Optional[str] = None,
        meaning: Optional[str] = None,
        forms_data: Optional[Dict[str, str]] = None,
        forms_meanings: Optional[Dict[str, str]] = None,
    ) -> None:
        """Update vocabulary mastery after review."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        word_lower = word.lower()
        now = datetime.now().isoformat()

        # Insert or get word
        cursor.execute(
            """
            INSERT OR IGNORE INTO vocabulary (word, source, created_at, updated_at)
            VALUES (?, 'task', ?, ?)
            """,
            (word_lower, now, now),
        )

        # Get word_id
        cursor.execute("SELECT id FROM vocabulary WHERE word = ?", (word_lower,))
        word_id = cursor.fetchone()[0]

        # Build update query dynamically
        updates = [
            "total_reviews = total_reviews + 1",
            "accuracy_score = ?",
            "last_reviewed = ?",
            "updated_at = ?",
        ]
        params = [accuracy_score, date, now]

        if word_type:
            updates.append("word_type = ?")
            params.append(word_type)

        if meaning:
            updates.append("meaning = ?")
            params.append(meaning)

        params.append(word_id)

        cursor.execute(
            f"""
            UPDATE vocabulary 
            SET {", ".join(updates)}
            WHERE id = ?
            """,
            params,
        )

        # Update forms mastery with values and meanings
        all_forms = ["verb", "noun", "adjective", "adverb", "opposite"]
        for form in all_forms:
            is_mastered = 1 if form in forms_correct else 0
            form_value = forms_data.get(form) if forms_data else None
            form_meaning = forms_meanings.get(form) if forms_meanings else None

            cursor.execute(
                """
                INSERT OR REPLACE INTO forms_mastery (word_id, form_type, form_value, form_meaning, is_mastered)
                VALUES (?, ?, ?, ?, ?)
                """,
                (word_id, form, form_value, form_meaning, is_mastered),
            )

        # Add to review history
        cursor.execute(
            """
            INSERT INTO review_history (word_id, review_date, accuracy)
            VALUES (?, ?, ?)
            """,
            (word_id, date, accuracy_score),
        )

        conn.commit()
        conn.close()

    def get_mastered_words(self, threshold: int = 80) -> list[str]:
        """Get words with accuracy >= threshold."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT word FROM vocabulary 
            WHERE accuracy_score >= ? AND total_reviews > 0
            ORDER BY accuracy_score DESC
            """,
            (threshold,),
        )

        words = [row[0] for row in cursor.fetchall()]
        conn.close()
        return words

    def get_weak_words(self, threshold: int = 80) -> list[str]:
        """Get words with accuracy < threshold that have been reviewed."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT word FROM vocabulary 
            WHERE accuracy_score < ? AND total_reviews > 0
            ORDER BY accuracy_score ASC, last_reviewed ASC
            """,
            (threshold,),
        )

        words = [row[0] for row in cursor.fetchall()]
        conn.close()
        return words

    def get_unreviewed_words(self, limit: int = 10) -> list[str]:
        """Get words that haven't been reviewed yet (from manual additions)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT word FROM vocabulary 
            WHERE total_reviews = 0
            ORDER BY created_at ASC
            LIMIT ?
            """,
            (limit,),
        )

        words = [row[0] for row in cursor.fetchall()]
        conn.close()
        return words

    def get_vocabulary_stats(self) -> dict:
        """Get overall vocabulary statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM vocabulary")
        total = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM vocabulary WHERE accuracy_score >= 80 AND total_reviews > 0"
        )
        mastered = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM vocabulary WHERE accuracy_score < 80 AND total_reviews > 0"
        )
        weak = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM vocabulary WHERE total_reviews = 0")
        unreviewed = cursor.fetchone()[0]

        conn.close()

        return {
            "total": total,
            "mastered": mastered,
            "weak": weak,
            "unreviewed": unreviewed,
        }

    def get_word_details(self, word: str) -> Optional[dict]:
        """Get detailed information about a word."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        word_lower = word.lower()

        cursor.execute(
            """
            SELECT id, word, word_type, total_reviews, accuracy_score, last_reviewed, 
                   source, meaning, created_at
            FROM vocabulary 
            WHERE word = ?
            """,
            (word_lower,),
        )

        vocab_row = cursor.fetchone()
        if not vocab_row:
            conn.close()
            return None

        word_id = vocab_row[0]

        # Get forms mastery with values
        cursor.execute(
            """
            SELECT form_type, form_value, form_meaning, is_mastered 
            FROM forms_mastery 
            WHERE word_id = ?
            """,
            (word_id,),
        )
        forms = {}
        for form_row in cursor.fetchall():
            forms[form_row[0]] = {
                "value": form_row[1],
                "meaning": form_row[2],
                "is_mastered": bool(form_row[3]),
            }

        # Get review history
        cursor.execute(
            """
            SELECT review_date, accuracy 
            FROM review_history 
            WHERE word_id = ?
            ORDER BY review_date DESC
            """,
            (word_id,),
        )
        history = [{"date": h[0], "accuracy": h[1]} for h in cursor.fetchall()]

        conn.close()

        return {
            "word": vocab_row[1],
            "word_type": vocab_row[2],
            "total_reviews": vocab_row[3],
            "accuracy_score": vocab_row[4],
            "last_reviewed": vocab_row[5],
            "source": vocab_row[6],
            "meaning": vocab_row[7],
            "created_at": vocab_row[8],
            "forms": forms,
            "history": history,
        }

    def update_word_form(self, word: str, form_type: str, form_value: str) -> bool:
        """Manually update a word form (verb/noun/adj/adv/opposite)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        word_lower = word.lower()

        # Get word_id
        cursor.execute("SELECT id FROM vocabulary WHERE word = ?", (word_lower,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return False

        word_id = result[0]
        now = datetime.now().isoformat()

        # Update or insert form
        cursor.execute(
            """
            INSERT OR REPLACE INTO forms_mastery (word_id, form_type, form_value, is_mastered)
            VALUES (?, ?, ?, 1)
            """,
            (word_id, form_type.lower(), form_value),
        )

        # Update vocabulary updated_at
        cursor.execute(
            """
            UPDATE vocabulary SET updated_at = ? WHERE id = ?
            """,
            (now, word_id),
        )

        conn.commit()
        conn.close()
        return True
