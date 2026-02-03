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
        Create ONE short professional conversation between 2 people with actual tech roles in English.
        Use real roles like: Backend Engineer, Frontend Developer, PM (Product Manager), DevOps Engineer, QA Engineer, Tech Lead, Designer, etc.
        The conversation should be about a common workplace scenario (meeting, code review, project discussion, deployment, etc.).
        Keep it natural and conversational (4-6 exchanges total).
        
        Format:
        **Scenario:** [Brief context, e.g., "Backend and Frontend discussing API integration"]
        
        **Backend:** [English sentence]
        
        **Frontend:** [English sentence]
        
        **Backend:** [English sentence]
        
        (Continue for 4-6 exchanges)
        
        Leave blank lines after each dialogue line for the student to write the Indonesian translation.
        
        ## 4. Grammar and Structure Challenge
        Create 3 workplace scenarios, one for each tense:
        
        **Scenario 1: Simple Present**
        Describe a daily routine or regular work activity.
        Provide 3 prompts for the student to write sentences using Simple Present.
        Example prompts:
        - (Your team / meet / every Monday)
        - (The system / process / data automatically)
        - (I / review / code before deployment)
        
        **Scenario 2: Simple Past**
        Describe a completed project or past event.
        Provide 3 prompts for the student to write sentences using Simple Past.
        Example prompts:
        - (We / launch / the new feature yesterday)
        - (The bug / cause / system downtime last week)
        - (She / present / the results to stakeholders)
        
        **Scenario 3: Simple Future**
        Describe upcoming plans or predictions.
        Provide 3 prompts for the student to write sentences using Simple Future (will/going to).
        Example prompts:
        - (The team / deploy / the update next week)
        - (I / attend / the conference in March)
        - (We / migrate / to the new server soon)
        
        Format: List each prompt with a blank line below for the answer.
        
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
        Start directly with word reviews. NO greeting or intro paragraphs.
        
        ### Word 1: [Word]
        
        | Form | Correct Answer | Student's Answer | Status | Arti |
        |------|----------------|------------------|--------|------|
        | Verb | ... | ... | ✓/✗/+ | ... |
        
        (Repeat for all words)
        
        ---
        
        **Summary:** [1-2 sentences only: overall score and main improvement area]
        
        Use Bahasa Indonesia. Be concise and direct.
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
        
        **Summary:** [2-3 sentences only: score, main patterns to improve, one actionable tip]
        
        Use Bahasa Indonesia for explanations. Be direct and concise. NO lengthy intro or closing paragraphs.
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
        Review translations with focus on CASUAL/INFORMAL workplace conversation style.
        Evaluate:
        1. **Translation Accuracy** - Is the meaning correct?
        2. **Conversational Tone** - Does it sound like natural, casual workplace chat in Indonesian?
        3. **Register** - Is it appropriately informal (not too formal/stiff)?
        
        **Output format:**
        
        ### Scenario
        **English:** [original scenario]
        **Your Translation:** [student's answer]
        **Accuracy:** ✓ Benar / ⚠️ Kurang Tepat / ✗ Salah
        **Feedback:** [Brief comment in Bahasa Indonesia]
        **Casual Alternative:** "[More casual/natural version if needed]"
        
        ---
        
        ### Line 1 - [Role]
        **English:** [original line]
        **Your Translation:** [student's answer]
        **Accuracy:** ✓ Benar / ⚠️ Kurang Tepat / ✗ Salah
        **Conversational:** ⭐⭐⭐⭐⭐ (1-5 stars, how casual/natural it sounds)
        
        **Feedback:**
        - [Is it too formal? Too stiff? Or naturally casual?]
        
        **Casual Alternative:**
        "[Provide more casual/natural workplace conversation version]"
        
        **💡 Casual Tips:**
        - [How to make it sound more like real casual workplace chat]
        - [Common casual expressions used in Indonesian tech workplace]
        
        ---
        
        **Summary:** [2-3 sentences: overall conversational tone score, formality issue if any, tip for casual workplace Indonesian]
        
        Use Bahasa Indonesia. Focus on helping student sound natural in casual workplace conversations, not overly formal.
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
        
        ---
        
        **Summary:** [2-3 sentences: overall tense accuracy, main grammar issue, one tip]
        
        Use Bahasa Indonesia. Be direct and concise. NO lengthy intro or closing.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error reviewing task: {str(e)}"
