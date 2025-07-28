"""
Quality agent for the AI Emotional Engine for Telugu Story Creation.
"""

from loguru import logger

from src.agents.base_agent import BaseAgent


class QualityAgent(BaseAgent):
    """
    Agent responsible for overall quality assurance.
    """
    
    def __init__(self, config):
        """
        Initialize the quality agent.
        
        Args:
            config (dict): Configuration dictionary.
        """
        super().__init__(config)
        logger.info("Quality agent initialized")
    
    def process(self, input_data, context=None):
        """
        Process input data and return results.
        
        Args:
            input_data: Input data to process.
            context: Optional context information.
        
        Returns:
            Processing results.
        """
        if isinstance(input_data, str):
            return self.ensure_quality(input_data, context)
        else:
            raise ValueError("Invalid input data for QualityAgent")
    
    def ensure_quality(self, story, parameters=None):
        """
        Ensure overall quality of the story.
        
        Args:
            story (str): Story content.
            parameters (dict, optional): Story parameters.
        
        Returns:
            str: Quality-assured story.
        """
        logger.info("Ensuring overall quality of story")
        
        # Perform quality assessment
        assessment = self.assess_quality(story, parameters)
        
        # If quality is below threshold, improve it
        if assessment["overall_score"] < 0.7:
            logger.info(f"Story quality below threshold ({assessment['overall_score']:.2f}), improving...")
            story = self._improve_quality(story, assessment, parameters)
        
        return story
    
    def assess_quality(self, story, parameters=None):
        """
        Assess overall quality of the story.
        
        Args:
            story (str): Story content.
            parameters (dict, optional): Story parameters.
        
        Returns:
            dict: Quality assessment.
        """
        logger.info("Assessing story quality")
        
        # Assess different quality dimensions
        narrative_score = self._assess_narrative_quality(story)
        emotional_score = self._assess_emotional_impact(story)
        cultural_score = self._assess_cultural_authenticity(story, parameters)
        character_score = self._assess_character_quality(story)
        technical_score = self._assess_technical_quality(story)
        
        # Calculate overall quality score
        overall_score = (
            narrative_score * 0.25 +
            emotional_score * 0.25 +
            cultural_score * 0.2 +
            character_score * 0.2 +
            technical_score * 0.1
        )
        
        assessment = {
            "overall_score": overall_score,
            "narrative_score": narrative_score,
            "emotional_score": emotional_score,
            "cultural_score": cultural_score,
            "character_score": character_score,
            "technical_score": technical_score,
            "issues": self._identify_quality_issues(story, parameters)
        }
        
        logger.debug(f"Quality assessment: {overall_score:.2f}/1.0")
        
        return assessment
    
    def _improve_quality(self, story, assessment, parameters=None):
        """
        Improve story quality based on assessment.
        
        Args:
            story (str): Story content.
            assessment (dict): Quality assessment.
            parameters (dict, optional): Story parameters.
        
        Returns:
            str: Improved story.
        """
        logger.info("Improving story quality")
        
        # In a real implementation, this would use an LLM to improve the story
        # based on the specific issues identified in the assessment
        # For now, we'll return the original story
        
        return story
    
    def _assess_narrative_quality(self, story):
        """
        Assess narrative quality.
        
        Args:
            story (str): Story content.
        
        Returns:
            float: Narrative quality score (0.0-1.0).
        """
        # In a real implementation, this would analyze narrative structure
        # For now, we'll return a placeholder score
        
        return 0.8
    
    def _assess_emotional_impact(self, story):
        """
        Assess emotional impact.
        
        Args:
            story (str): Story content.
        
        Returns:
            float: Emotional impact score (0.0-1.0).
        """
        # In a real implementation, this would analyze emotional content
        # For now, we'll return a placeholder score
        
        return 0.75
    
    def _assess_cultural_authenticity(self, story, parameters=None):
        """
        Assess cultural authenticity.
        
        Args:
            story (str): Story content.
            parameters (dict, optional): Story parameters.
        
        Returns:
            float: Cultural authenticity score (0.0-1.0).
        """
        # In a real implementation, this would analyze cultural elements
        # For now, we'll return a placeholder score
        
        return 0.85
    
    def _assess_character_quality(self, story):
        """
        Assess character quality.
        
        Args:
            story (str): Story content.
        
        Returns:
            float: Character quality score (0.0-1.0).
        """
        # In a real implementation, this would analyze character development
        # For now, we'll return a placeholder score
        
        return 0.8
    
    def _assess_technical_quality(self, story):
        """
        Assess technical quality.
        
        Args:
            story (str): Story content.
        
        Returns:
            float: Technical quality score (0.0-1.0).
        """
        # In a real implementation, this would analyze technical aspects
        # For now, we'll return a placeholder score
        
        return 0.9
    
    def _identify_quality_issues(self, story, parameters=None):
        """
        Identify quality issues in the story.
        
        Args:
            story (str): Story content.
            parameters (dict, optional): Story parameters.
        
        Returns:
            list: Identified quality issues.
        """
        # In a real implementation, this would identify specific quality issues
        # For now, we'll return an empty list
        
        return []
    
    def generate_quality_report(self, story, parameters=None):
        """
        Generate a detailed quality report.
        
        Args:
            story (str): Story content.
            parameters (dict, optional): Story parameters.
        
        Returns:
            dict: Detailed quality report.
        """
        logger.info("Generating quality report")
        
        # Perform quality assessment
        assessment = self.assess_quality(story, parameters)
        
        # Calculate word count
        word_count = len(story.split())
        
        # Calculate additional metrics
        report = {
            "quality_assessment": assessment,
            "metrics": {
                "word_count": word_count,
                "average_sentence_length": self._calculate_average_sentence_length(story),
                "dialogue_percentage": self._calculate_dialogue_percentage(story),
                "description_percentage": self._calculate_description_percentage(story)
            },
            "recommendations": self._generate_recommendations(assessment)
        }
        
        return report
    
    def _calculate_average_sentence_length(self, text):
        """
        Calculate average sentence length.
        
        Args:
            text (str): Input text.
        
        Returns:
            float: Average sentence length.
        """
        # Simple sentence splitting by punctuation
        sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        
        if not sentences:
            return 0
        
        total_words = sum(len(s.split()) for s in sentences)
        return total_words / len(sentences)
    
    def _calculate_dialogue_percentage(self, text):
        """
        Calculate percentage of text that is dialogue.
        
        Args:
            text (str): Input text.
        
        Returns:
            float: Dialogue percentage.
        """
        # Simple dialogue detection by quotation marks
        dialogue_words = 0
        total_words = len(text.split())
        
        if total_words == 0:
            return 0
        
        # Count words in quotation marks
        in_quote = False
        for line in text.split("\n"):
            for char in line:
                if char == '"' or char == '"' or char == '"':
                    in_quote = not in_quote
            
            if in_quote:
                dialogue_words += len(line.split())
        
        return dialogue_words / total_words
    
    def _calculate_description_percentage(self, text):
        """
        Calculate percentage of text that is description.
        
        Args:
            text (str): Input text.
        
        Returns:
            float: Description percentage.
        """
        # Estimate description as non-dialogue text
        dialogue_percentage = self._calculate_dialogue_percentage(text)
        return 1.0 - dialogue_percentage
    
    def _generate_recommendations(self, assessment):
        """
        Generate recommendations based on quality assessment.
        
        Args:
            assessment (dict): Quality assessment.
        
        Returns:
            list: Recommendations.
        """
        recommendations = []
        
        # Generate recommendations based on scores
        if assessment["narrative_score"] < 0.7:
            recommendations.append("Improve narrative structure and plot coherence")
        
        if assessment["emotional_score"] < 0.7:
            recommendations.append("Enhance emotional impact and character motivations")
        
        if assessment["cultural_score"] < 0.7:
            recommendations.append("Increase cultural authenticity and Telugu-specific elements")
        
        if assessment["character_score"] < 0.7:
            recommendations.append("Develop characters with more depth and consistency")
        
        if assessment["technical_score"] < 0.7:
            recommendations.append("Improve technical quality, grammar, and language usage")
        
        return recommendations