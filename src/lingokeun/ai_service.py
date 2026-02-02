from .config import settings
from google import genai


class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate_daily_task(self) -> str:
        """
        Membuat materi latihan harian.
        AI otomatis memilih 5 kata.
        Level Translation: B1 (Intermediate).
        """
        prompt = """
        You are an expert English Tutor for a Senior Backend Engineer.
        
        **Task:**
        1. Randomly select **5 high-value English vocabulary words** (verbs, adjectives, or nouns) suitable for a **General Professional Tech environment**.
        2. Create a daily learning challenge based on these 5 selected words.

        # Context Setting
        The user is a Software Engineer. The context is **General Professional English**.
        Focus on daily interactions, clear communication, and standard work updates.
        
        Please generate a Markdown response with this exact structure:
        
        # Daily Task
        **Selected Vocabulary:** [List the 5 words here]
        **Focus:** Clear Professional Communication
        
        ## 1. Word Transformation Challenge
        For each selected word, create a fill-in-the-blank list for:
        - Verb:
        - Noun:
        - Adjective:
        - Adverb:
        - Opposite:
        (Leave the answers completely blank after the colon, no underscores).
        
        ## 2. Translation Challenge (B1 Level)
        Create 6 Indonesian sentences related to daily work life.
        Keep the sentence structure simple and direct (Subject-Verb-Object), suitable for Intermediate learners.
        Make the sentences slightly longer and more detailed to increase the challenge.
        
        **Requirements:**
        - Sentences 1-4: Regular statements (positive sentences)
        - Sentence 5: MUST be a negative sentence (using "tidak", "belum", "bukan", etc.)
        - Sentence 6: MUST be a question sentence (using "apakah", "bagaimana", "kapan", etc.)
        
        Format: List sentences directly without extra blank lines between them.
        Example:
        - Saya akan mengirimkan pembaruan kode tersebut sore ini setelah meeting dengan tim.
        - Tim kami tidak menemukan kesalahan di dalam dokumen persyaratan tersebut setelah review kedua.
        - Apakah kita bisa mendiskusikan masalah ini di pertemuan besok pagi sebelum presentasi?
        
        ## 3. Conversation Transliteration Challenge
        Create ONE short professional conversation between 2 people (Person A and Person B) in English.
        The conversation should be about a common workplace scenario (meeting, code review, project discussion, etc.).
        Keep it natural and conversational (4-6 exchanges total).
        
        Format: List dialogue lines directly without extra blank lines between them.
        **Scenario:** [Brief context, e.g., "Discussing a bug fix in a code review"]
        **A:** [English sentence]
        **B:** [English sentence]
        **A:** [English sentence]
        (Continue for 4-6 exchanges)
        
        ## 4. Tense Construction Challenge
        Create 3 workplace scenarios for sentence construction practice:
        
        **Scenario 1 (Simple Present):** Describe your daily routine or regular tasks at work
        Example context: "What do you usually do during your workday?"
        Write 1-2 sentences using Simple Present tense.
        
        **Scenario 2 (Simple Past):** Tell about something you completed or experienced recently
        Example context: "Describe a bug you fixed or a meeting you attended yesterday"
        Write 1-2 sentences using Simple Past tense.
        
        **Scenario 3 (Simple Future):** Explain your plans or predictions for upcoming work
        Example context: "What will you work on next week or next sprint?"
        Write 1-2 sentences using Simple Future tense (will/going to).
        
        ## 5. Daily Tip
        Provide one practical tip for improving English communication skills in a professional tech environment.
        Keep it short, actionable, and relevant to the selected vocabulary.
        
        **Do NOT provide the answer key yet.**
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating task from AI: {str(e)}"

    def review_task1(self, user_answers: str) -> str:
        """Review Task 1 (Word Transformation Challenge)."""
        prompt = f"""
        You are an expert English Tutor reviewing a student's word transformation exercise.
        
        The student has completed a word transformation challenge. Here are their answers:
        
        {user_answers}
        
        **Your task:**
        1. Review each word and its transformations
        2. Correct any mistakes (spelling, wrong forms, or missing forms)
        3. Add missing forms if the student left them blank
        4. Provide Indonesian meanings for each word form
        
        **Output format:**
        Create a markdown table for each word with these columns:
        - Form Type (Verb/Noun/Adjective/Adverb/Opposite)
        - Correct Answer
        - Student's Answer (show what they wrote, or "Kosong" if blank)
        - Status (✓ Benar / ✗ Salah / + Ditambahkan)
        - Arti (Indonesian meaning)
        
        Provide the review in Bahasa Indonesia with a friendly, encouraging tone.
        Start with a brief summary of overall performance.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error reviewing task: {str(e)}"

    def review_task2(self, indonesian_sentences: str, user_translations: str) -> str:
        """Review Task 2 (Translation Challenge)."""
        prompt = f"""
        You are an expert English Tutor reviewing translation exercises for a B1 (Intermediate) level student.
        
        **Original Indonesian sentences:**
        {indonesian_sentences}
        
        **Student's English translations:**
        {user_translations}
        
        **Your task:**
        For each translation, evaluate:
        1. **B1 Level Accuracy** - Is the meaning correct? Are grammar and vocabulary appropriate for B1?
        2. **Nativeness** - How natural does it sound to a native English speaker?
        3. **Suggestions** - Provide a more natural alternative if needed
        4. **Advanced Tips** - Suggest better phrasal verbs, collocations, prepositions, or idioms when applicable
        
        **Output format:**
        Create a review for each sentence with this structure:
        
        ### Sentence 1
        **Indonesian:** [original sentence]
        **Your Translation:** [student's answer]
        **Accuracy:** ✓ Benar / ⚠️ Kurang Tepat / ✗ Salah
        **Nativeness Score:** ⭐⭐⭐⭐⭐ (1-5 stars)
        
        **Feedback:**
        - [Brief explanation in Bahasa Indonesia about accuracy]
        - [Comment on naturalness]
        
        **More Natural Alternative:**
        "[Provide a more natural version]"
        
        **Key Improvements:**
        - [Specific suggestion 1]
        - [Specific suggestion 2]
        
        **💡 Advanced Tips:** (if applicable)
        - **Phrasal Verb:** [Suggest better phrasal verb if relevant]
        - **Collocation:** [Suggest natural word combinations]
        - **Preposition:** [Correct preposition usage]
        - **Idiom:** [Suggest relevant idiom if it makes the sentence more natural]
        
        ---
        
        At the end, provide:
        - Overall performance summary
        - Common patterns to improve
        - Encouragement and next steps
        
        Use Bahasa Indonesia for explanations, but keep English examples in English.
        Be encouraging but honest about areas for improvement.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error reviewing task: {str(e)}"

    def review_task3(self, english_conversation: str, user_translations: str) -> str:
        """Review Task 3 (Conversation Transliteration Challenge)."""
        prompt = f"""
        You are an expert English Tutor reviewing conversation transliteration exercises for a B1 (Intermediate) level student.
        
        **Original English conversation:**
        {english_conversation}
        
        **Student's Indonesian translations:**
        {user_translations}
        
        **Your task:**
        For each dialogue line, evaluate:
        1. **Translation Accuracy** - Is the meaning correctly conveyed in Indonesian?
        2. **Naturalness** - Does it sound natural in Indonesian conversation?
        3. **Context Awareness** - Does the translation maintain the conversational flow and tone?
        
        **Output format:**
        Create a review for each dialogue line with this structure:
        
        ### Line 1 - Person A
        **English:** [original line]
        **Your Translation:** [student's answer]
        **Accuracy:** ✓ Benar / ⚠️ Kurang Tepat / ✗ Salah
        **Naturalness:** ⭐⭐⭐⭐⭐ (1-5 stars)
        
        **Feedback:**
        - [Brief explanation in Bahasa Indonesia about accuracy and naturalness]
        
        **More Natural Alternative:**
        "[Provide a more natural Indonesian version]"
        
        **💡 Tips:**
        - [Specific suggestion about conversational Indonesian, informal vs formal register, common expressions]
        
        ---
        
        At the end, provide:
        
        ## Overall Conversation Review
        **Strengths:**
        - [What the student did well]
        
        **Areas to Improve:**
        - [Specific patterns or issues to work on]
        
        **Conversational Tips:**
        - [Tips for translating conversations more naturally]
        - [Common conversational expressions in Indonesian]
        
        Use Bahasa Indonesia for explanations, but keep English examples in English.
        Be encouraging and focus on helping the student understand conversational nuances.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error reviewing task: {str(e)}"

    def review_task4(self, user_answers: str) -> str:
        """
        Review Task 4 (Grammar and Structure Challenge).
        Evaluates correct tense usage, sentence structure, and grammar.
        """
        prompt = f"""
        You are an expert English Tutor reviewing grammar and structure exercises for a B1 (Intermediate) level student.
        
        **Student's answers:**
        {user_answers}
        
        **Your task:**
        Review each sentence for:
        1. **Correct Tense Usage** - Is the appropriate tense used (Simple Present/Past/Future)?
        2. **Grammar Accuracy** - Subject-verb agreement, word order, auxiliary verbs
        3. **Sentence Structure** - Is the sentence well-formed and natural?
        
        **Output format:**
        
        ### Scenario 1: Simple Present
        
        **Sentence 1:**
        **Your Answer:** [student's sentence]
        **Grammar Check:** ✓ Correct / ✗ Incorrect
        **Feedback:** [Brief explanation in Bahasa Indonesia]
        **Correct Version:** "[If needed, provide corrected sentence]"
        
        (Repeat for sentences 2-3)
        
        ### Scenario 2: Simple Past
        (Same format)
        
        ### Scenario 3: Simple Future
        (Same format)
        
        ---
        
        ## Overall Grammar Review
        
        **Strengths:**
        - What the student did well with tenses and structure
        
        **Common Mistakes:**
        - Patterns of errors to watch out for
        
        **Grammar Tips:**
        - **Simple Present:** Use for habits, facts, routines (I work, She codes, They meet)
        - **Simple Past:** Use for completed actions (worked, coded, met)
        - **Simple Future:** Use will/going to for plans (will work, is going to code)
        
        Use Bahasa Indonesia for explanations, but keep English examples in English.
        Be encouraging and focus on helping the student master basic tenses.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error reviewing task: {str(e)}"
