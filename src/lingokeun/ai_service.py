from .config import settings
from google import genai

class AIService():
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
        
        Format: List each sentence with a blank line below for the answer.
        Example:
        - Saya akan mengirimkan pembaruan kode tersebut sore ini setelah meeting dengan tim.
        - Tim kami tidak menemukan kesalahan di dalam dokumen persyaratan tersebut setelah review kedua.
        - Apakah kita bisa mendiskusikan masalah ini di pertemuan besok pagi sebelum presentasi?
        
        ## 3. Daily Tip
        Provide one practical tip for improving English communication skills in a professional tech environment.
        Keep it short, actionable, and relevant to the selected vocabulary.
        
        **Do NOT provide the answer key yet.**
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating task from AI: {str(e)}"

    def review_task1(self, user_answers: str) -> str:
        """
        Review Task 1 (Word Transformation Challenge).
        Returns corrections and meanings in table format.
        """
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
        
        Example format:
        
        ### Word 1: Simplify
        
        | Form | Correct Answer | Student's Answer | Status | Arti |
        |------|----------------|------------------|--------|------|
        | Verb | Simplify | Simplify | ✓ Benar | Menyederhanakan |
        | Noun | Simplification | Simplification | ✓ Benar | Penyederhanaan |
        | Adjective | Simple | Simplified | ✗ Salah | Sederhana |
        | Adverb | Simply | Kosong | + Ditambahkan | Dengan sederhana |
        | Opposite | Complicate | Kosong | + Ditambahkan | Memperumit |
        
        Provide the review in Bahasa Indonesia with a friendly, encouraging tone.
        Start with a brief summary of overall performance.
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error reviewing task: {str(e)}"

    def review_task2(self, indonesian_sentences: str, user_translations: str) -> str:
        """
        Review Task 2 (Translation Challenge).
        Evaluates B1 level accuracy, nativeness, and provides natural alternatives.
        """
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
                model='gemini-3-flash-preview',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error reviewing task: {str(e)}"