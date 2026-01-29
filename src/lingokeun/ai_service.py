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
        
        Format: Just list the sentences directly with bullet points, no labels or descriptions.
        Example:
        - Saya akan mengirimkan pembaruan kode tersebut sore ini setelah meeting dengan tim.
        - Apakah kita bisa mendiskusikan masalah ini di pertemuan besok pagi sebelum presentasi?
        - Tim kami tidak menemukan kesalahan di dalam dokumen persyaratan tersebut setelah review kedua.
        - Saya sudah selesai memperbaiki bug itu, tetapi saya masih butuh waktu untuk memeriksa kodenya lagi dengan teliti.
        
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