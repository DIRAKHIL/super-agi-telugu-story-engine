"""
Prompt templates for the AI Emotional Engine for Telugu Story Creation.
PRODUCTION-READY REAL AI SYSTEM - 100% open source OPERATIONAL!
"""

import json


def get_story_plan_prompt(genre, theme, setting, characters, emotional_arc):
    """
    Generate a prompt for creating a story plan.
    
    Args:
        genre (str): Story genre.
        theme (str): Story theme.
        setting (dict): Story setting.
        characters (list): Story characters.
        emotional_arc (str): Emotional arc of the story.
    
    Returns:
        str: Prompt for story plan generation.
    """
    setting_str = json.dumps(setting, ensure_ascii=False)
    characters_str = json.dumps(characters, ensure_ascii=False)
    
    prompt = f"""
    Create a detailed story plan for a Telugu story with the following parameters:
    
    Genre: {genre}
    Theme: {theme}
    Setting: {setting_str}
    Characters: {characters_str}
    Emotional Arc: {emotional_arc}
    
    Your response should be a JSON object with the following structure:
    {{
        "title": "Story title",
        "genre": "{genre}",
        "theme": "{theme}",
        "setting": {setting_str},
        "plot_structure": ["plot_point_1", "plot_point_2", ...],
        "scenes": [
            {{
                "id": 1,
                "title": "Scene 1 title",
                "plot_point": "plot_point_1",
                "description": "Detailed scene description",
                "setting": "Specific location for this scene",
                "characters": ["Character 1", "Character 2"]
            }},
            ...
        ],
        "emotional_progression": ["emotion_1", "emotion_2", ...],
        "cultural_elements": ["element_1", "element_2", ...]
    }}
    
    Ensure the story is culturally authentic to Telugu traditions and values.
    Include regional specificity in settings, character interactions, and cultural references.
    The emotional arc should follow: {emotional_arc}
    """
    
    return prompt


def get_story_draft_prompt(story_plan, characters):
    """
    Generate a prompt for creating a story draft.
    
    Args:
        story_plan (dict): Story plan.
        characters (list): Developed characters.
    
    Returns:
        str: Prompt for story draft generation.
    """
    story_plan_str = json.dumps(story_plan, ensure_ascii=False)
    characters_str = json.dumps(characters, ensure_ascii=False)
    
    prompt = f"""
    Write a complete Telugu story based on the following story plan and characters:
    
    Story Plan: {story_plan_str}
    
    Characters: {characters_str}
    
    Guidelines:
    1. Write a cohesive narrative that follows the plot structure and scenes in the story plan.
    2. Develop the characters according to their traits and backgrounds.
    3. Include authentic Telugu cultural elements, expressions, and regional specificity.
    4. Use a mix of Telugu and English as appropriate, with Telugu for dialogue and cultural elements.
    5. Follow the emotional arc specified in the story plan.
    6. Include sensory details and vivid descriptions of settings.
    7. Use appropriate Telugu literary techniques and storytelling traditions.
    
    Format the story with clear scene breaks, character dialogue, and narrative flow.
    """
    
    return prompt


def get_story_enhancement_prompt(story, enhancement_type="general", specific_instructions=""):
    """
    Generate a prompt for enhancing a story.
    
    Args:
        story (str): Existing story.
        enhancement_type (str): Type of enhancement to perform.
        specific_instructions (str): Specific instructions for enhancement.
    
    Returns:
        str: Prompt for story enhancement.
    """
    enhancement_instructions = {
        "general": "Improve the overall quality, coherence, and impact of the story.",
        "emotional": "Enhance the emotional depth and impact of the story.",
        "cultural": "Strengthen the Telugu cultural authenticity and regional specificity.",
        "character": "Develop the characters more fully with psychological depth and consistency.",
        "language": "Improve the language, including appropriate Telugu expressions and literary techniques.",
        "plot": "Strengthen the plot structure, pacing, and narrative coherence."
    }
    
    instruction = enhancement_instructions.get(enhancement_type, enhancement_instructions["general"])
    
    prompt = f"""
    Enhance the following Telugu story:
    
    {story}
    
    Enhancement focus: {instruction}
    
    Additional instructions: {specific_instructions}
    
    Preserve the original story's essence while making it more compelling, authentic, and impactful.
    Maintain cultural authenticity and emotional resonance throughout.
    """
    
    return prompt


def get_character_development_prompt(character_info, story_context):
    """
    Generate a prompt for developing a character.
    
    Args:
        character_info (dict): Basic character information.
        story_context (dict): Context information about the story.
    
    Returns:
        str: Prompt for character development.
    """
    character_str = json.dumps(character_info, ensure_ascii=False)
    context_str = json.dumps(story_context, ensure_ascii=False)
    
    prompt = f"""
    Develop a psychologically complex and culturally authentic Telugu character based on the following information:
    
    Character: {character_str}
    
    Story Context: {context_str}
    
    Your response should be a JSON object with the following structure:
    {{
        "name": "{character_info.get('name', 'Character Name')}",
        "age": {character_info.get('age', 30)},
        "gender": "{character_info.get('gender', 'unspecified')}",
        "background": "Detailed character background",
        "personality": {{
            "traits": ["trait1", "trait2", ...],
            "strengths": ["strength1", "strength2", ...],
            "flaws": ["flaw1", "flaw2", ...],
            "motivations": ["motivation1", "motivation2", ...],
            "fears": ["fear1", "fear2", ...],
            "values": ["value1", "value2", ...]
        }},
        "relationships": [
            {{
                "with": "Other character name",
                "type": "relationship type",
                "dynamics": "relationship dynamics"
            }},
            ...
        ],
        "arc": "Character's emotional/psychological arc in the story",
        "cultural_elements": ["element1", "element2", ...],
        "speech_patterns": "Description of how the character speaks",
        "physical_description": "Detailed physical description"
    }}
    
    Ensure the character is psychologically consistent, culturally authentic, and appropriate for the story context.
    Include Telugu-specific cultural elements, values, and social dynamics.
    """
    
    return prompt


def get_cultural_adaptation_prompt(content, dialect="standard", region="Coastal Andhra"):
    """
    Generate a prompt for cultural adaptation of content.
    
    Args:
        content (str): Content to adapt.
        dialect (str): Telugu dialect to use.
        region (str): Specific region of Telugu culture.
    
    Returns:
        str: Prompt for cultural adaptation.
    """
    dialect_info = {
        "standard": "Standard literary Telugu",
        "telangana": "Telangana dialect with its unique vocabulary and expressions",
        "rayalaseema": "Rayalaseema dialect with its distinctive cadence and vocabulary",
        "coastal": "Coastal Andhra dialect with its flowing rhythm and vocabulary",
        "nellore": "Nellore region dialect with its unique expressions",
        "godavari": "Godavari region dialect with its distinctive vocabulary"
    }
    
    dialect_description = dialect_info.get(dialect.lower(), dialect_info["standard"])
    
    prompt = f"""
    Adapt the following content to be culturally authentic for Telugu speakers from the {region} region, using the {dialect_description}:
    
    {content}
    
    Guidelines:
    1. Incorporate region-specific cultural references, traditions, and values.
    2. Use appropriate dialect-specific vocabulary, expressions, and speech patterns.
    3. Include authentic cultural elements like festivals, food, clothing, and social customs.
    4. Adapt metaphors and similes to reflect Telugu literary traditions.
    5. Ensure the emotional expressions align with Telugu cultural norms.
    6. Incorporate appropriate Telugu proverbs, sayings, or literary references.
    7. Maintain the original meaning and emotional impact while making it culturally authentic.
    
    The adaptation should feel natural and authentic to Telugu speakers from the specified region.
    """
    
    return prompt


def get_emotional_enhancement_prompt(content, emotional_tone, intensity=0.7):
    """
    Generate a prompt for emotional enhancement of content.
    
    Args:
        content (str): Content to enhance.
        emotional_tone (str): Primary emotional tone to enhance.
        intensity (float): Intensity of emotional enhancement (0.0-1.0).
    
    Returns:
        str: Prompt for emotional enhancement.
    """
    intensity_description = "subtle" if intensity < 0.4 else "moderate" if intensity < 0.7 else "strong"
    
    prompt = f"""
    Enhance the emotional impact of the following content with a {intensity_description} {emotional_tone} tone:
    
    {content}
    
    Guidelines:
    1. Amplify the {emotional_tone} emotional elements to an intensity of {intensity_description}.
    2. Use Telugu-appropriate emotional expressions and cultural context.
    3. Enhance sensory details that evoke the desired emotion.
    4. Adjust pacing, sentence structure, and word choice to reinforce the emotional tone.
    5. Incorporate culturally authentic emotional metaphors and expressions.
    6. Ensure the emotional enhancement feels natural and authentic, not forced.
    7. Maintain the original meaning and narrative flow while enhancing the emotional impact.
    
    The enhanced content should resonate emotionally with Telugu readers in a culturally authentic way.
    """
    
    return prompt