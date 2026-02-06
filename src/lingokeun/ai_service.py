from .config import settings
from .user_profile import UserProfileManager
from google import genai


class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.profile_manager = UserProfileManager()

    def generate_daily_task(self) -> str:
        """
        Membuat materi latihan harian.
        AI otomatis memilih 5 kata.
        Level Translation: B1 (Intermediate).
        """
        # Get user context for personalized tasks
        user_context = self.profile_manager.get_user_context_for_ai()
        vocab_context = self.profile_manager.get_vocabulary_context_for_ai()

        prompt = f"""
        You are an expert English Tutor for a Senior Backend Engineer.
        
        **User Context:**
        {user_context}
        
        **Vocabulary Selection Rules:**
        - AVOID these mastered words (80%+ accuracy): {", ".join(vocab_context["mastered"][:20]) if vocab_context["mastered"] else "None yet"}
        - PRIORITIZE reviewing these weak words (<80%): {", ".join(vocab_context["weak"][:10]) if vocab_context["weak"] else "None"}
        - CONSIDER these unreviewed words (from user's reading): {", ".join(vocab_context["unreviewed"][:10]) if vocab_context["unreviewed"] else "None"}
        - Select 5 words total: prioritize weak words, then unreviewed words, then new words
        
        **Task:**
        1. Select **5 vocabulary words** following the rules above
        2. Create a daily learning challenge based on these 5 selected words
        3. If user has specific weaknesses, incorporate vocabulary that helps address those areas

        # Context Setting
        The user is a Software Engineer. The context is **General Professional English**.
        Focus on daily interactions, clear communication, and standard work updates.
        
        Please generate a Markdown response with this exact structure:
        
        # Daily Task
        **Selected Vocabulary:** [List the 5 words here]
        **Focus:** Clear Professional Communication
        
        ## 💡 Daily Tip
        Provide one practical tip for improving English communication skills in a professional tech environment.
        
        **Focus areas for tips (rotate between these):**
        - Casual conversational responses (Sure, That sounds good, Exactly, Got it, Makes sense, Fair enough)
        - Natural workplace reactions (Oh I see, Right, Gotcha, Yep, Absolutely, For sure)
        - Phrasal verbs in casual context
        - Informal vs formal register
        - Common workplace expressions
        
        Keep it SHORT and actionable. Include ONLY 2-3 example phrases (not 5+).
        
        **⚠️ Common Mistake:** Add ONE line about a common mistake to avoid (e.g., "Don't say 'I am agree' → Say 'I agree'")
        
        ## 1. Word Transformation Challenge
        For each selected word, create a fill-in-the-blank list for:
        - Verb:
        - Noun:
        - Adjective:
        - Adverb:
        - Opposite:
        (Leave the answers completely blank after the colon, no underscores).
        
        ## 2. Translation Challenge (B1 Level)
        Create 7 Indonesian sentences related to daily work life.
        Keep the sentence structure simple and direct (Subject-Verb-Object), suitable for Intermediate learners.
        Make the sentences slightly longer and more detailed to increase the challenge.
        
        **Requirements:**
        - Sentences 1-4: Regular statements (positive sentences)
        - Sentence 5: MUST be a negative sentence (using "tidak", "belum", "bukan", etc.)
        - Sentence 6: MUST be a question sentence (using "apakah", "bagaimana", "kapan", etc.)
        - Sentence 7: MUST be a passive voice sentence (using "di-" prefix, e.g., "dikerjakan", "diperiksa", "diselesaikan")
        
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
        Provide 5 different words (verb, noun, adjective, or adverb) for sentence construction practice.
        Each word should be used with a specific tense in a workplace context.
        
        **Challenge:** Write a sentence using the given word in the specified tense.
        
        **1. Simple Present:** [word]
        
        
        **2. Simple Past:** [word]
        
        
        **3. Simple Future:** [word]
        
        
        **4. Present Continuous:** [word]
        
        
        **5. Present Perfect:** [word]
        
        
        Make sure each word is different and relevant to tech workplace context.
        
        **Do NOT provide the answer key yet.**
        - Natural workplace reactions (Oh I see, Right, Gotcha, Yep, Absolutely, For sure, etc.)
        - Phrasal verbs in casual context
        - Informal vs formal register
        
        **Do NOT provide the answer key yet.**
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating task from AI: {str(e)}"

    def extract_vocabulary_mastery_from_review(
        self, review_content: str, date: str
    ) -> None:
        """Extract vocabulary mastery from Task 1 review and update profile."""
        import re

        # Extract words and their accuracy from review
        # Pattern: ### Word X: [word] (type: [n/v/adj/adv])
        word_pattern = r"### Word \d+: (\w+)(?: \(type: ([nvadj]+)\))?"
        matches = re.findall(word_pattern, review_content, re.IGNORECASE)

        for word, word_type in matches:
            # Count correct/wrong forms for this word
            # Look for ✓ Benar and ✗ Salah in the word's section
            word_section_pattern = rf"### Word \d+: {word}.*?(?=### Word|---|$)"
            word_section = re.search(
                word_section_pattern, review_content, re.DOTALL | re.IGNORECASE
            )

            if word_section:
                section_text = word_section.group(0)

                # Count status markers
                correct_count = section_text.count("✓")

                total_forms = 5  # verb, noun, adj, adv, opposite
                forms_correct_count = correct_count

                # Calculate accuracy
                accuracy = int((forms_correct_count / total_forms) * 100)

                # Extract form values from table
                # Pattern: | Form | Correct Answer | ...
                forms_data = {}
                for form_name in ["Verb", "Noun", "Adjective", "Adverb", "Opposite"]:
                    pattern = rf"\| {form_name} \| ([^|]+) \|"
                    match = re.search(pattern, section_text)
                    if match:
                        form_value = match.group(1).strip()
                        # Skip if it's a placeholder or empty
                        if form_value and form_value != "..." and form_value != "-":
                            forms_data[form_name.lower()] = form_value

                # Determine which forms are correct/weak
                forms_correct = []
                forms_weak = []

                if (
                    "| Verb |" in section_text
                    and "✓" in section_text.split("| Verb |")[1].split("\n")[0]
                ):
                    forms_correct.append("verb")
                else:
                    forms_weak.append("verb")

                if (
                    "| Noun |" in section_text
                    and "✓" in section_text.split("| Noun |")[1].split("\n")[0]
                ):
                    forms_correct.append("noun")
                else:
                    forms_weak.append("noun")

                if (
                    "| Adjective |" in section_text
                    and "✓" in section_text.split("| Adjective |")[1].split("\n")[0]
                ):
                    forms_correct.append("adjective")
                else:
                    forms_weak.append("adjective")

                if (
                    "| Adverb |" in section_text
                    and "✓" in section_text.split("| Adverb |")[1].split("\n")[0]
                ):
                    forms_correct.append("adverb")
                else:
                    forms_weak.append("adverb")

                if (
                    "| Opposite |" in section_text
                    and "✓" in section_text.split("| Opposite |")[1].split("\n")[0]
                ):
                    forms_correct.append("opposite")
                else:
                    forms_weak.append("opposite")

                # Update profile with word_type and forms_data
                self.profile_manager.update_vocabulary_mastery(
                    word=word,
                    word_type=word_type if word_type else None,
                    accuracy_score=accuracy,
                    forms_correct=forms_correct,
                    forms_weak=forms_weak,
                    forms_data=forms_data,
                    date=date,
                )

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
        5. Identify the PRIMARY word type (n/v/adj/adv) - the most common usage
        
        **Output format:**
        Start directly with word reviews. NO greeting or intro paragraphs.
        
        ### Word 1: [Word] (type: [n/v/adj/adv])
        
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
        
        **CRITICAL: NO greeting or intro paragraphs. Start directly with scenario review.**
        
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
        1. **Correct Tense Usage** - Is the appropriate tense used?
        2. **Word Usage** - Is the given word used correctly in the sentence?
        3. **Grammar Accuracy** - Subject-verb agreement, word order, auxiliary verbs
        4. **Naturalness** - Does it sound natural in workplace context?
        
        **Output format:**
        
        ### 1. Simple Present
        **Given Word:** [the word provided]
        **Your Sentence:** [student's sentence]
        **Tense:** ✓ Correct / ✗ Incorrect
        **Word Usage:** ✓ Correct / ✗ Incorrect
        **Grammar:** ✓ Correct / ⚠️ Minor Issues / ✗ Major Issues
        **Naturalness:** ⭐⭐⭐⭐⭐ (1-5 stars)
        
        **Feedback:** [Brief explanation in Bahasa Indonesia]
        **Better Version:** "[If needed, provide improved sentence]"
        
        ### 2. Simple Past
        (Same format)
        
        ### 3. Simple Future
        (Same format)
        
        ### 4. Present Continuous
        (Same format)
        
        ### 5. Present Perfect
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

    def update_user_profile_after_review(
        self, review_content: str, task_type: str, date: str
    ) -> None:
        """Update user profile with weaknesses found in review."""
        self.profile_manager.update_weaknesses(review_content, task_type, date)

    def generate_learning_material(self, topic: str) -> str:
        """Generate B1 intermediate learning material for specific topic."""
        prompt = f"""
        You are an expert English Tutor creating B1 (Intermediate) level learning materials for software engineers.
        
        **Topic:** {topic}
        
        **Your task:**
        Create comprehensive learning material in Markdown format with this structure:
        
        # {topic}
        
        ## Overview
        [Brief explanation of the topic - 2-3 sentences]
        
        ## Key Concepts
        [List 3-5 main concepts with brief explanations]
        
        ## Common Patterns in Tech Workplace
        [Show 5-7 examples relevant to software engineering context]
        Example format:
        - **Pattern:** [English example]
          **Usage:** [When to use it]
          **Indonesian:** [Translation]
        
        ## Practice Exercises
        [Provide 5 practice sentences/scenarios]
        Format: Leave blank lines for answers
        
        ## Common Mistakes to Avoid
        [List 3-4 common mistakes with corrections]
        ❌ Wrong: [example]
        ✅ Correct: [example]
        
        ## Quick Reference
        [Summary table or bullet points for quick review]
        
        Keep language at B1 level - not too simple, not too complex.
        Focus on practical workplace communication.
        Use Bahasa Indonesia for explanations when helpful.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating material: {str(e)}"

    def suggest_material_topics(self) -> list[str]:
        """Suggest material topics based on user weaknesses."""
        profile = self.profile_manager.load_profile()

        topics = []

        # Get all grammar weaknesses from profile (sorted by total_mistakes)
        grammar_weaknesses = profile.get("grammar_weaknesses", {})
        sorted_grammar = sorted(
            grammar_weaknesses.items(),
            key=lambda x: x[1].get("total_mistakes", 0),
            reverse=True,
        )

        for weakness_key, data in sorted_grammar[:3]:  # Top 3
            topic_name = weakness_key.replace("_", " ").title()
            topics.append(f"{topic_name} in English")

        # Get all translation weaknesses from profile (sorted by total_mistakes)
        translation_weaknesses = profile.get("translation_weaknesses", {})
        sorted_translation = sorted(
            translation_weaknesses.items(),
            key=lambda x: x[1].get("total_mistakes", 0),
            reverse=True,
        )

        for weakness_key, data in sorted_translation[:2]:  # Top 2
            topic_name = weakness_key.replace("_", " ").title()
            topics.append(f"{topic_name} for Tech Workplace")

        # Add vocabulary gap topics
        vocab_gaps = profile.get("vocabulary_gaps", [])
        if vocab_gaps:
            vocab_words = [v["word"] for v in vocab_gaps[:3]]
            topics.append(f"Essential Vocabulary: {', '.join(vocab_words)}")

        return topics[:5]  # Return top 5 suggestions
