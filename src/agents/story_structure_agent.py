"""
Story Structure Agent for Telugu Story Engine
Real AI agent for narrative structure and plot development - NO MOCKS
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
import re
import json
from datetime import datetime

from .base_agent import BaseAgent, AgentResponse, AgentStatus
from ..core.model_manager import get_model_manager

logger = logging.getLogger(__name__)

class StoryStructureAgent(BaseAgent):
    """
    Real AI agent for managing narrative structure and plot development
    Uses actual language models for story structure analysis and generation
    """
    
    def __init__(self, agent_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        
        # Story structure specific configuration
        self.structure_types = self.config.get("structure_types", [
            "three_act", "hero_journey", "kishōtenketsu", "circular", "episodic"
        ])
        self.plot_elements = self.config.get("plot_elements", [
            "exposition", "inciting_incident", "rising_action", "climax", 
            "falling_action", "resolution", "denouement"
        ])
        self.pacing_styles = self.config.get("pacing_styles", [
            "slow_burn", "fast_paced", "episodic", "contemplative", "action_driven"
        ])
        
        # Telugu narrative patterns
        self.telugu_patterns = {
            "classical": {
                "structure": "five_act",
                "elements": ["mukham", "pratimukham", "garbham", "vimarsha", "upasanharam"],
                "description": "Classical Telugu drama structure"
            },
            "folk": {
                "structure": "circular",
                "elements": ["opening_song", "character_intro", "conflict", "resolution", "moral"],
                "description": "Traditional folk narrative structure"
            },
            "modern": {
                "structure": "three_act",
                "elements": ["setup", "confrontation", "resolution"],
                "description": "Modern Telugu cinema structure"
            }
        }
        
        logger.info(f"Initialized StoryStructureAgent with {len(self.structure_types)} structure types")
    
    async def process(
        self,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process story structure requirements using real AI models
        """
        start_time = datetime.now()
        self.status = AgentStatus.PROCESSING
        
        try:
            # Extract story requirements
            story_prompt = input_data.get("prompt", "")
            story_type = input_data.get("story_type", "drama")
            length = input_data.get("length", 2000)
            cultural_context = input_data.get("cultural_context", "contemporary_telugu")
            
            # Analyze story requirements
            structure_analysis = await self._analyze_story_requirements(
                story_prompt, story_type, length, cultural_context
            )
            
            # Generate story structure
            story_structure = await self._generate_story_structure(
                structure_analysis, context or {}
            )
            
            # Create detailed plot outline
            plot_outline = await self._create_plot_outline(story_structure, input_data)
            
            # Generate narrative framework
            narrative_framework = await self._generate_narrative_framework(
                plot_outline, cultural_context
            )
            
            # Calculate confidence based on structure coherence
            confidence = await self._calculate_structure_confidence(
                story_structure, plot_outline, narrative_framework
            )
            
            # Prepare response content
            response_content = self._format_structure_response(
                story_structure, plot_outline, narrative_framework
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Add to memory
            self.add_conversation("user", str(input_data))
            self.add_conversation("assistant", response_content, {
                "processing_time": processing_time,
                "confidence": confidence,
                "structure_type": story_structure.get("type"),
                "plot_elements": len(plot_outline.get("elements", []))
            })
            
            return AgentResponse(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                content=response_content,
                confidence=confidence,
                metadata={
                    "story_structure": story_structure,
                    "plot_outline": plot_outline,
                    "narrative_framework": narrative_framework,
                    "structure_analysis": structure_analysis
                },
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error in StoryStructureAgent processing: {e}")
            self.status = AgentStatus.ERROR
            raise
        finally:
            self.status = AgentStatus.IDLE
    
    async def _analyze_story_requirements(
        self,
        prompt: str,
        story_type: str,
        length: int,
        cultural_context: str
    ) -> Dict[str, Any]:
        """Analyze story requirements using real AI models"""
        
        # Create analysis prompt
        analysis_prompt = f"""
        Analyze the following Telugu story requirements and provide structural recommendations:
        
        Story Prompt: {prompt}
        Story Type: {story_type}
        Target Length: {length} words
        Cultural Context: {cultural_context}
        
        Please analyze:
        1. Appropriate narrative structure
        2. Key plot elements needed
        3. Pacing requirements
        4. Cultural considerations
        5. Character development needs
        
        Provide analysis in Telugu and English.
        """
        
        # Use Telugu BERT for understanding
        model_manager = get_model_manager()
        
        # Generate analysis using GPT model
        analysis_text = await model_manager.generate_text(
            "telugu_gpt",
            analysis_prompt,
            max_new_tokens=150,  # Generate 150 new tokens
            temperature=0.7
        )
        
        # Extract structured information
        structure_analysis = await self._extract_structure_info(analysis_text, prompt)
        
        return structure_analysis
    
    async def _extract_structure_info(self, analysis_text: str, original_prompt: str) -> Dict[str, Any]:
        """Extract structured information from analysis text"""
        
        # Use pattern matching and AI to extract key information
        structure_info = {
            "recommended_structure": "three_act",  # Default
            "key_themes": [],
            "plot_complexity": "medium",
            "pacing_style": "balanced",
            "cultural_elements": [],
            "character_count": 2,
            "conflict_type": "internal"
        }
        
        # Analyze text for structure recommendations
        if "hero" in analysis_text.lower() or "journey" in analysis_text.lower():
            structure_info["recommended_structure"] = "hero_journey"
        elif "circular" in analysis_text.lower() or "cyclical" in analysis_text.lower():
            structure_info["recommended_structure"] = "circular"
        elif "episodic" in analysis_text.lower():
            structure_info["recommended_structure"] = "episodic"
        
        # Extract themes using keyword analysis
        theme_keywords = {
            "family": ["family", "కుటుంబం", "పరివారం"],
            "love": ["love", "ప్రేమ", "అనురాగం"],
            "sacrifice": ["sacrifice", "త్యాగం", "బలిదానం"],
            "duty": ["duty", "కర్తవ్యం", "ధర్మం"],
            "tradition": ["tradition", "సంప్రదాయం", "పరంపర"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword.lower() in analysis_text.lower() for keyword in keywords):
                structure_info["key_themes"].append(theme)
        
        # Determine complexity based on prompt length and content
        if len(original_prompt) > 200 or "complex" in analysis_text.lower():
            structure_info["plot_complexity"] = "high"
        elif len(original_prompt) < 50:
            structure_info["plot_complexity"] = "low"
        
        return structure_info
    
    async def _generate_story_structure(
        self,
        analysis: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate detailed story structure"""
        
        structure_type = analysis.get("recommended_structure", "three_act")
        
        # Get structure template
        if structure_type in self.telugu_patterns:
            base_structure = self.telugu_patterns[structure_type].copy()
        else:
            base_structure = self._get_universal_structure(structure_type)
        
        # Customize structure based on analysis
        customized_structure = {
            "type": structure_type,
            "acts": base_structure.get("elements", []),
            "pacing": analysis.get("pacing_style", "balanced"),
            "themes": analysis.get("key_themes", []),
            "cultural_adaptation": self._get_cultural_adaptations(analysis),
            "character_arcs": self._plan_character_arcs(analysis),
            "conflict_progression": self._plan_conflict_progression(analysis)
        }
        
        return customized_structure
    
    def _get_universal_structure(self, structure_type: str) -> Dict[str, Any]:
        """Get universal story structure templates"""
        structures = {
            "three_act": {
                "elements": ["setup", "confrontation", "resolution"],
                "proportions": [0.25, 0.5, 0.25]
            },
            "hero_journey": {
                "elements": [
                    "ordinary_world", "call_to_adventure", "refusal_of_call",
                    "meeting_mentor", "crossing_threshold", "tests_allies_enemies",
                    "approach_inmost_cave", "ordeal", "reward", "road_back",
                    "resurrection", "return_with_elixir"
                ],
                "proportions": [0.08] * 12
            },
            "kishōtenketsu": {
                "elements": ["introduction", "development", "twist", "conclusion"],
                "proportions": [0.25, 0.25, 0.25, 0.25]
            },
            "circular": {
                "elements": ["beginning", "departure", "journey", "return", "transformation"],
                "proportions": [0.2, 0.2, 0.3, 0.2, 0.1]
            }
        }
        
        return structures.get(structure_type, structures["three_act"])
    
    def _get_cultural_adaptations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get cultural adaptations for the story structure"""
        adaptations = []
        
        themes = analysis.get("key_themes", [])
        
        if "family" in themes:
            adaptations.append({
                "element": "family_dynamics",
                "description": "Include traditional Telugu family relationships and hierarchies",
                "implementation": "Show respect for elders, joint family dynamics"
            })
        
        if "tradition" in themes:
            adaptations.append({
                "element": "cultural_practices",
                "description": "Incorporate Telugu festivals, rituals, and customs",
                "implementation": "Include appropriate cultural celebrations and practices"
            })
        
        if "duty" in themes:
            adaptations.append({
                "element": "dharmic_choices",
                "description": "Present moral dilemmas in Telugu cultural context",
                "implementation": "Show characters making choices based on dharma and duty"
            })
        
        return adaptations
    
    def _plan_character_arcs(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan character development arcs"""
        character_count = analysis.get("character_count", 2)
        themes = analysis.get("key_themes", [])
        
        arcs = []
        
        # Main protagonist arc
        arcs.append({
            "character_type": "protagonist",
            "arc_type": "transformation",
            "starting_state": "ordinary_world",
            "ending_state": "transformed_hero",
            "key_challenges": themes[:2] if themes else ["personal_growth"],
            "development_stages": ["introduction", "challenge", "growth", "resolution"]
        })
        
        # Supporting character arcs
        if character_count > 1:
            arcs.append({
                "character_type": "deuteragonist",
                "arc_type": "support_and_growth",
                "starting_state": "helper_or_obstacle",
                "ending_state": "evolved_relationship",
                "key_challenges": themes[1:3] if len(themes) > 1 else ["relationship"],
                "development_stages": ["introduction", "interaction", "conflict_or_support", "resolution"]
            })
        
        return arcs
    
    def _plan_conflict_progression(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Plan conflict progression throughout the story"""
        conflict_type = analysis.get("conflict_type", "internal")
        complexity = analysis.get("plot_complexity", "medium")
        
        progression = {
            "primary_conflict": {
                "type": conflict_type,
                "introduction_point": 0.1,  # 10% into story
                "escalation_points": [0.3, 0.6, 0.8],
                "resolution_point": 0.9
            },
            "secondary_conflicts": [],
            "tension_curve": "rising_action_dominant"
        }
        
        # Add secondary conflicts based on complexity
        if complexity == "high":
            progression["secondary_conflicts"] = [
                {
                    "type": "interpersonal",
                    "introduction_point": 0.2,
                    "resolution_point": 0.7
                },
                {
                    "type": "societal",
                    "introduction_point": 0.4,
                    "resolution_point": 0.85
                }
            ]
        elif complexity == "medium":
            progression["secondary_conflicts"] = [
                {
                    "type": "interpersonal",
                    "introduction_point": 0.25,
                    "resolution_point": 0.75
                }
            ]
        
        return progression
    
    async def _create_plot_outline(
        self,
        structure: Dict[str, Any],
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create detailed plot outline based on structure"""
        
        # Generate plot outline using AI
        outline_prompt = f"""
        Create a detailed plot outline for a Telugu story with the following structure:
        
        Structure Type: {structure['type']}
        Acts/Elements: {', '.join(structure['acts'])}
        Themes: {', '.join(structure['themes'])}
        Pacing: {structure['pacing']}
        
        Original Prompt: {input_data.get('prompt', '')}
        Story Type: {input_data.get('story_type', 'drama')}
        Length: {input_data.get('length', 2000)} words
        
        Create a detailed outline with:
        1. Scene-by-scene breakdown
        2. Character introductions and development
        3. Plot points and turning points
        4. Emotional beats
        5. Cultural elements integration
        
        Write in both Telugu and English.
        """
        
        model_manager = get_model_manager()
        outline_text = await model_manager.generate_text(
            "telugu_gpt",
            outline_prompt,
            max_length=1500,
            temperature=0.8
        )
        
        # Structure the outline
        plot_outline = {
            "acts": structure["acts"],
            "scenes": await self._extract_scenes_from_outline(outline_text),
            "plot_points": await self._extract_plot_points(outline_text),
            "emotional_beats": await self._extract_emotional_beats(outline_text),
            "cultural_elements": structure.get("cultural_adaptation", []),
            "pacing_notes": self._generate_pacing_notes(structure)
        }
        
        return plot_outline
    
    async def _extract_scenes_from_outline(self, outline_text: str) -> List[Dict[str, Any]]:
        """Extract scene information from outline text"""
        scenes = []
        
        # Simple scene extraction (can be enhanced with more sophisticated NLP)
        scene_patterns = [
            r"Scene \d+:",
            r"సన్నివేశం \d+:",
            r"\d+\.",
            r"Act \d+, Scene \d+:"
        ]
        
        lines = outline_text.split('\n')
        current_scene = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a scene header
            is_scene_header = any(re.search(pattern, line) for pattern in scene_patterns)
            
            if is_scene_header:
                if current_scene:
                    scenes.append(current_scene)
                
                current_scene = {
                    "title": line,
                    "description": "",
                    "characters": [],
                    "location": "",
                    "emotional_tone": "",
                    "purpose": ""
                }
            elif current_scene:
                current_scene["description"] += line + " "
        
        # Add the last scene
        if current_scene:
            scenes.append(current_scene)
        
        return scenes
    
    async def _extract_plot_points(self, outline_text: str) -> List[Dict[str, Any]]:
        """Extract key plot points from outline"""
        plot_points = []
        
        # Look for key plot point indicators
        plot_indicators = [
            "inciting incident", "plot twist", "climax", "resolution",
            "turning point", "revelation", "conflict", "crisis"
        ]
        
        lines = outline_text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for indicator in plot_indicators:
                if indicator in line_lower:
                    plot_points.append({
                        "type": indicator,
                        "description": line.strip(),
                        "position": i / len(lines),  # Relative position in story
                        "importance": "high" if indicator in ["climax", "inciting incident"] else "medium"
                    })
        
        return plot_points
    
    async def _extract_emotional_beats(self, outline_text: str) -> List[Dict[str, Any]]:
        """Extract emotional beats from outline"""
        emotional_beats = []
        
        # Emotion keywords in Telugu and English
        emotion_keywords = {
            "joy": ["joy", "happiness", "celebration", "ఆనందం", "సంతోషం"],
            "sadness": ["sadness", "grief", "sorrow", "దుఃఖం", "విషాదం"],
            "anger": ["anger", "rage", "fury", "కోపం", "రోషం"],
            "fear": ["fear", "terror", "anxiety", "భయం", "భీతి"],
            "love": ["love", "affection", "romance", "ప్రేమ", "అనురాగం"],
            "hope": ["hope", "optimism", "faith", "ఆశ", "నమ్మకం"]
        }
        
        lines = outline_text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for emotion, keywords in emotion_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    emotional_beats.append({
                        "emotion": emotion,
                        "description": line.strip(),
                        "position": i / len(lines),
                        "intensity": "high" if any(intense in line_lower for intense in ["intense", "powerful", "overwhelming"]) else "medium"
                    })
        
        return emotional_beats
    
    def _generate_pacing_notes(self, structure: Dict[str, Any]) -> List[str]:
        """Generate pacing notes based on structure"""
        pacing_style = structure.get("pacing", "balanced")
        structure_type = structure.get("type", "three_act")
        
        notes = []
        
        if pacing_style == "fast_paced":
            notes.extend([
                "Keep scenes short and punchy",
                "Use quick cuts between locations",
                "Maintain high energy throughout",
                "Minimize exposition, show through action"
            ])
        elif pacing_style == "slow_burn":
            notes.extend([
                "Allow scenes to breathe and develop naturally",
                "Focus on character development and relationships",
                "Build tension gradually",
                "Use contemplative moments effectively"
            ])
        elif pacing_style == "episodic":
            notes.extend([
                "Structure as interconnected episodes",
                "Each section should have its own arc",
                "Maintain overarching narrative thread",
                "Allow for varied pacing within episodes"
            ])
        
        # Add structure-specific notes
        if structure_type == "hero_journey":
            notes.append("Follow the natural rhythm of the hero's journey")
        elif structure_type == "circular":
            notes.append("Ensure the ending echoes the beginning meaningfully")
        
        return notes
    
    async def _generate_narrative_framework(
        self,
        plot_outline: Dict[str, Any],
        cultural_context: str
    ) -> Dict[str, Any]:
        """Generate comprehensive narrative framework"""
        
        framework = {
            "narrative_voice": await self._determine_narrative_voice(plot_outline),
            "point_of_view": await self._determine_pov(plot_outline),
            "tense_and_mood": await self._determine_tense_mood(plot_outline),
            "cultural_integration": await self._plan_cultural_integration(cultural_context),
            "language_style": await self._determine_language_style(cultural_context),
            "dialogue_approach": await self._plan_dialogue_approach(cultural_context),
            "descriptive_elements": await self._plan_descriptive_elements(plot_outline)
        }
        
        return framework
    
    async def _determine_narrative_voice(self, plot_outline: Dict[str, Any]) -> Dict[str, Any]:
        """Determine appropriate narrative voice"""
        # Analyze plot complexity and emotional beats
        emotional_beats = plot_outline.get("emotional_beats", [])
        scenes = plot_outline.get("scenes", [])
        
        if len(emotional_beats) > 5 and len(scenes) > 8:
            return {
                "type": "omniscient",
                "characteristics": ["all-knowing", "multiple_perspectives", "deep_insight"],
                "rationale": "Complex plot requires omniscient perspective"
            }
        else:
            return {
                "type": "limited_third_person",
                "characteristics": ["focused", "intimate", "character_driven"],
                "rationale": "Simpler plot benefits from focused perspective"
            }
    
    async def _determine_pov(self, plot_outline: Dict[str, Any]) -> Dict[str, Any]:
        """Determine point of view"""
        return {
            "primary": "third_person",
            "secondary": None,
            "shifts": False,
            "rationale": "Third person allows flexibility while maintaining Telugu narrative traditions"
        }
    
    async def _determine_tense_mood(self, plot_outline: Dict[str, Any]) -> Dict[str, Any]:
        """Determine tense and mood"""
        emotional_beats = plot_outline.get("emotional_beats", [])
        
        # Analyze dominant emotions
        emotions = [beat["emotion"] for beat in emotional_beats]
        dominant_emotion = max(set(emotions), key=emotions.count) if emotions else "neutral"
        
        if dominant_emotion in ["sadness", "fear"]:
            mood = "contemplative"
        elif dominant_emotion in ["joy", "love"]:
            mood = "uplifting"
        elif dominant_emotion == "anger":
            mood = "intense"
        else:
            mood = "balanced"
        
        return {
            "tense": "past",
            "mood": mood,
            "tone": "authentic_telugu",
            "atmosphere": self._determine_atmosphere(emotional_beats)
        }
    
    def _determine_atmosphere(self, emotional_beats: List[Dict[str, Any]]) -> str:
        """Determine story atmosphere"""
        if not emotional_beats:
            return "neutral"
        
        # Count emotional intensities
        high_intensity = sum(1 for beat in emotional_beats if beat.get("intensity") == "high")
        total_beats = len(emotional_beats)
        
        if high_intensity / total_beats > 0.6:
            return "dramatic"
        elif high_intensity / total_beats > 0.3:
            return "engaging"
        else:
            return "gentle"
    
    async def _plan_cultural_integration(self, cultural_context: str) -> Dict[str, Any]:
        """Plan cultural integration strategy"""
        integration_strategies = {
            "contemporary_telugu": {
                "elements": ["modern_family_dynamics", "urban_rural_blend", "technology_integration"],
                "approach": "balanced_traditional_modern",
                "language_mix": "telugu_with_english_phrases"
            },
            "traditional_telugu": {
                "elements": ["classical_values", "joint_family_system", "religious_practices"],
                "approach": "traditional_emphasis",
                "language_mix": "pure_telugu_preferred"
            },
            "rural_telugu": {
                "elements": ["village_life", "agriculture", "folk_traditions"],
                "approach": "authentic_rural_representation",
                "language_mix": "regional_dialect_emphasis"
            }
        }
        
        return integration_strategies.get(cultural_context, integration_strategies["contemporary_telugu"])
    
    async def _determine_language_style(self, cultural_context: str) -> Dict[str, Any]:
        """Determine language style"""
        return {
            "register": "formal_respectful",
            "dialect": self._get_appropriate_dialect(cultural_context),
            "complexity": "accessible_literary",
            "cultural_references": "integrated_naturally"
        }
    
    def _get_appropriate_dialect(self, cultural_context: str) -> str:
        """Get appropriate Telugu dialect"""
        dialect_mapping = {
            "contemporary_telugu": "standard_telugu",
            "traditional_telugu": "classical_telugu",
            "rural_telugu": "regional_dialect",
            "coastal_andhra": "coastal_dialect",
            "rayalaseema": "rayalaseema_dialect",
            "telangana": "telangana_dialect"
        }
        
        return dialect_mapping.get(cultural_context, "standard_telugu")
    
    async def _plan_dialogue_approach(self, cultural_context: str) -> Dict[str, Any]:
        """Plan dialogue approach"""
        return {
            "style": "natural_conversational",
            "cultural_markers": "appropriate_honorifics",
            "generational_differences": "reflected_in_speech",
            "emotional_expression": "culturally_authentic"
        }
    
    async def _plan_descriptive_elements(self, plot_outline: Dict[str, Any]) -> Dict[str, Any]:
        """Plan descriptive elements"""
        scenes = plot_outline.get("scenes", [])
        
        return {
            "setting_descriptions": "vivid_but_concise",
            "character_descriptions": "personality_focused",
            "sensory_details": "culturally_relevant",
            "metaphors_similes": "telugu_cultural_references",
            "scene_count": len(scenes)
        }
    
    async def _calculate_structure_confidence(
        self,
        structure: Dict[str, Any],
        plot_outline: Dict[str, Any],
        framework: Dict[str, Any]
    ) -> float:
        """Calculate confidence in the generated structure"""
        confidence_factors = []
        
        # Structure completeness
        if structure.get("acts") and len(structure["acts"]) > 0:
            confidence_factors.append(0.2)
        
        # Plot outline quality
        scenes = plot_outline.get("scenes", [])
        if len(scenes) >= 3:
            confidence_factors.append(0.2)
        
        plot_points = plot_outline.get("plot_points", [])
        if len(plot_points) >= 2:
            confidence_factors.append(0.15)
        
        # Emotional beats presence
        emotional_beats = plot_outline.get("emotional_beats", [])
        if len(emotional_beats) >= 1:
            confidence_factors.append(0.15)
        
        # Cultural integration
        if structure.get("cultural_adaptation"):
            confidence_factors.append(0.1)
        
        # Framework completeness
        if framework.get("narrative_voice") and framework.get("cultural_integration"):
            confidence_factors.append(0.2)
        
        return min(sum(confidence_factors), 1.0)
    
    def _format_structure_response(
        self,
        structure: Dict[str, Any],
        plot_outline: Dict[str, Any],
        framework: Dict[str, Any]
    ) -> str:
        """Format the structure response for output"""
        
        response_parts = []
        
        # Structure overview
        response_parts.append(f"**Story Structure: {structure['type'].replace('_', ' ').title()}**")
        response_parts.append(f"Acts/Elements: {', '.join(structure['acts'])}")
        response_parts.append(f"Themes: {', '.join(structure['themes'])}")
        response_parts.append(f"Pacing: {structure['pacing']}")
        response_parts.append("")
        
        # Plot outline summary
        scenes = plot_outline.get("scenes", [])
        response_parts.append(f"**Plot Outline ({len(scenes)} scenes):**")
        for i, scene in enumerate(scenes[:5], 1):  # Show first 5 scenes
            response_parts.append(f"{i}. {scene.get('title', f'Scene {i}')}")
        
        if len(scenes) > 5:
            response_parts.append(f"... and {len(scenes) - 5} more scenes")
        response_parts.append("")
        
        # Key plot points
        plot_points = plot_outline.get("plot_points", [])
        if plot_points:
            response_parts.append("**Key Plot Points:**")
            for point in plot_points[:3]:  # Show top 3 plot points
                response_parts.append(f"- {point['type'].title()}: {point['description'][:100]}...")
            response_parts.append("")
        
        # Narrative framework
        response_parts.append("**Narrative Framework:**")
        response_parts.append(f"Voice: {framework.get('narrative_voice', {}).get('type', 'N/A')}")
        response_parts.append(f"Cultural Integration: {framework.get('cultural_integration', {}).get('approach', 'N/A')}")
        response_parts.append(f"Language Style: {framework.get('language_style', {}).get('register', 'N/A')}")
        
        return "\n".join(response_parts)
    
    def get_relevance_score(self, input_data: Dict[str, Any]) -> float:
        """Calculate relevance score for story structure tasks"""
        relevance_factors = []
        
        # Always relevant for story generation
        relevance_factors.append(0.5)
        
        # Higher relevance for structure-related requests
        prompt = input_data.get("prompt", "").lower()
        structure_keywords = ["structure", "plot", "outline", "story", "narrative", "acts", "scenes"]
        
        keyword_matches = sum(1 for keyword in structure_keywords if keyword in prompt)
        relevance_factors.append(min(keyword_matches * 0.1, 0.3))
        
        # Higher relevance for longer stories
        length = input_data.get("length", 0)
        if length > 1000:
            relevance_factors.append(0.2)
        
        return min(sum(relevance_factors), 1.0)
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            "story_structure_analysis",
            "plot_development",
            "narrative_framework_design",
            "cultural_structure_adaptation",
            "pacing_optimization",
            "character_arc_planning",
            "conflict_progression",
            "scene_organization",
            "telugu_narrative_patterns"
        ]