"""
Cultural agent for the AI Emotional Engine for Telugu Story Creation.
"""

from loguru import logger

from src.agents.base_agent import BaseAgent


class CulturalAgent(BaseAgent):
    """
    Agent responsible for cultural adaptation and authenticity.
    """
    
    def __init__(self, config):
        """
        Initialize the cultural agent.
        
        Args:
            config (dict): Configuration dictionary.
        """
        super().__init__(config)
        
        # Get Telugu-specific configuration
        self.telugu_config = config.get("telugu", {})
        self.dialect = self.telugu_config.get("dialect", "standard")
        self.regional_variations = self.telugu_config.get("regional_variations", True)
        
        logger.info(f"Cultural agent initialized with dialect: {self.dialect}")
    
    def process(self, input_data, context=None):
        """
        Process input data and return results.
        
        Args:
            input_data: Input data to process.
            context: Optional context information.
        
        Returns:
            Processing results.
        """
        if isinstance(input_data, dict) and "parameters" in input_data:
            return self.analyze_cultural_context(input_data["parameters"])
        elif isinstance(input_data, str):
            return self.adapt_culturally(input_data, context)
        else:
            raise ValueError("Invalid input data for CulturalAgent")
    
    def analyze_cultural_context(self, parameters):
        """
        Analyze cultural context from story parameters.
        
        Args:
            parameters (dict): Story parameters.
        
        Returns:
            dict: Cultural context analysis.
        """
        logger.info("Analyzing cultural context")
        
        # Extract relevant parameters
        setting = parameters.get("setting", {})
        location = setting.get("location", "")
        time_period = setting.get("time_period", "")
        social_context = setting.get("social_context", "")
        
        # Determine region
        region = self._determine_region(location)
        
        # Determine time period context
        period_context = self._analyze_time_period(time_period)
        
        # Determine social context
        social_analysis = self._analyze_social_context(social_context)
        
        # Compile cultural elements
        cultural_elements = self._compile_cultural_elements(region, period_context, social_analysis)
        
        cultural_context = {
            "region": region,
            "period_context": period_context,
            "social_analysis": social_analysis,
            "cultural_elements": cultural_elements,
            "dialect_recommendations": self._recommend_dialect(region, social_analysis)
        }
        
        logger.debug(f"Analyzed cultural context for region: {region}")
        
        return cultural_context
    
    def adapt_culturally(self, story, parameters=None):
        """
        Adapt story to Telugu cultural context.
        
        Args:
            story (str): Story content.
            parameters (dict, optional): Story parameters.
        
        Returns:
            str: Culturally adapted story.
        """
        logger.info("Adapting story culturally")
        
        # In a real implementation, this would use an LLM to adapt the story
        # For now, we'll return the original story
        
        return story
    
    def _determine_region(self, location):
        """
        Determine Telugu region from location.
        
        Args:
            location (str): Location string.
        
        Returns:
            dict: Region information.
        """
        location_lower = location.lower()
        
        # Default region
        region = {
            "name": "General Telugu Region",
            "dialect": "standard",
            "cultural_specificity": "general"
        }
        
        # Check for specific regions
        if "coastal" in location_lower or "andhra" in location_lower:
            if "north coastal" in location_lower or "visakhapatnam" in location_lower or "vizag" in location_lower:
                region = {
                    "name": "North Coastal Andhra",
                    "dialect": "uttarandhra",
                    "cultural_specificity": "specific"
                }
            else:
                region = {
                    "name": "Coastal Andhra",
                    "dialect": "coastal",
                    "cultural_specificity": "specific"
                }
        elif "rayalaseema" in location_lower:
            region = {
                "name": "Rayalaseema",
                "dialect": "rayalaseema",
                "cultural_specificity": "specific"
            }
        elif "telangana" in location_lower:
            region = {
                "name": "Telangana",
                "dialect": "telangana",
                "cultural_specificity": "specific"
            }
        elif "hyderabad" in location_lower:
            region = {
                "name": "Hyderabad",
                "dialect": "hyderabadi",
                "cultural_specificity": "urban"
            }
        
        return region
    
    def _analyze_time_period(self, time_period):
        """
        Analyze time period context.
        
        Args:
            time_period (str): Time period string.
        
        Returns:
            dict: Time period context.
        """
        time_period_lower = time_period.lower()
        
        # Default period context
        period_context = {
            "era": "contemporary",
            "historical_significance": [],
            "cultural_markers": []
        }
        
        # Check for specific time periods
        if "ancient" in time_period_lower or "historical" in time_period_lower:
            period_context = {
                "era": "historical",
                "historical_significance": ["traditional values", "historical customs"],
                "cultural_markers": ["traditional attire", "historical language", "traditional practices"]
            }
        elif "colonial" in time_period_lower:
            period_context = {
                "era": "colonial",
                "historical_significance": ["british influence", "independence movement"],
                "cultural_markers": ["colonial architecture", "changing social structures"]
            }
        elif "post-independence" in time_period_lower:
            period_context = {
                "era": "post-independence",
                "historical_significance": ["nation building", "social reform"],
                "cultural_markers": ["emerging modernity", "traditional values"]
            }
        elif "1980s" in time_period_lower or "1990s" in time_period_lower:
            period_context = {
                "era": "late-20th-century",
                "historical_significance": ["economic changes", "technological transition"],
                "cultural_markers": ["changing family structures", "urban migration"]
            }
        elif "contemporary" in time_period_lower or "modern" in time_period_lower:
            period_context = {
                "era": "contemporary",
                "historical_significance": ["globalization", "technological advancement"],
                "cultural_markers": ["modern lifestyle", "traditional values tension"]
            }
        
        return period_context
    
    def _analyze_social_context(self, social_context):
        """
        Analyze social context.
        
        Args:
            social_context (str): Social context string.
        
        Returns:
            dict: Social context analysis.
        """
        social_context_lower = social_context.lower()
        
        # Default social analysis
        social_analysis = {
            "setting_type": "general",
            "socioeconomic_factors": [],
            "community_dynamics": []
        }
        
        # Check for specific social contexts
        if "rural" in social_context_lower or "village" in social_context_lower:
            social_analysis = {
                "setting_type": "rural",
                "socioeconomic_factors": ["agricultural economy", "traditional livelihoods"],
                "community_dynamics": ["close-knit community", "traditional hierarchies"]
            }
        elif "urban" in social_context_lower or "city" in social_context_lower:
            social_analysis = {
                "setting_type": "urban",
                "socioeconomic_factors": ["diverse economy", "class divisions"],
                "community_dynamics": ["individualism", "changing social norms"]
            }
        elif "fishing" in social_context_lower:
            social_analysis = {
                "setting_type": "coastal",
                "socioeconomic_factors": ["fishing economy", "seasonal challenges"],
                "community_dynamics": ["community interdependence", "traditional practices"]
            }
        elif "tribal" in social_context_lower or "adivasi" in social_context_lower:
            social_analysis = {
                "setting_type": "tribal",
                "socioeconomic_factors": ["traditional livelihoods", "economic marginalization"],
                "community_dynamics": ["strong cultural identity", "traditional governance"]
            }
        elif "middle class" in social_context_lower:
            social_analysis = {
                "setting_type": "middle-class",
                "socioeconomic_factors": ["stable income", "education focus"],
                "community_dynamics": ["family-oriented", "aspirational"]
            }
        
        return social_analysis
    
    def _compile_cultural_elements(self, region, period_context, social_analysis):
        """
        Compile cultural elements based on region, period, and social context.
        
        Args:
            region (dict): Region information.
            period_context (dict): Time period context.
            social_analysis (dict): Social context analysis.
        
        Returns:
            dict: Cultural elements.
        """
        # Compile cultural elements
        cultural_elements = {
            "festivals": self._get_regional_festivals(region["name"]),
            "cuisine": self._get_regional_cuisine(region["name"]),
            "traditions": self._get_regional_traditions(region["name"]),
            "language_patterns": self._get_language_patterns(region["dialect"]),
            "social_norms": self._get_social_norms(period_context["era"], social_analysis["setting_type"])
        }
        
        return cultural_elements
    
    def _recommend_dialect(self, region, social_analysis):
        """
        Recommend dialect based on region and social context.
        
        Args:
            region (dict): Region information.
            social_analysis (dict): Social context analysis.
        
        Returns:
            dict: Dialect recommendations.
        """
        dialect = region["dialect"]
        setting_type = social_analysis["setting_type"]
        
        # Adjust dialect based on setting type
        if setting_type == "urban" and dialect != "hyderabadi":
            dialect_mix = f"{dialect}-urban"
            formality = "mixed"
        elif setting_type == "rural":
            dialect_mix = dialect
            formality = "traditional"
        else:
            dialect_mix = dialect
            formality = "standard"
        
        return {
            "primary_dialect": dialect,
            "dialect_mix": dialect_mix,
            "formality": formality,
            "colloquialisms": self._should_use_colloquialisms(dialect, setting_type)
        }
    
    def _get_regional_festivals(self, region_name):
        """
        Get regional festivals.
        
        Args:
            region_name (str): Region name.
        
        Returns:
            list: Regional festivals.
        """
        # Common Telugu festivals
        common_festivals = ["Sankranti", "Ugadi", "Dasara", "Deepavali", "Vinayaka Chavithi"]
        
        # Region-specific festivals
        region_specific = []
        
        if "Coastal" in region_name:
            region_specific = ["Ganga Jatara", "Teppotsavam"]
        elif "Rayalaseema" in region_name:
            region_specific = ["Kadiri Lakshmi Narasimha Swamy Brahmotsavalu", "Penna Pushkaralu"]
        elif "Telangana" in region_name:
            region_specific = ["Bonalu", "Bathukamma"]
        elif "Hyderabad" in region_name:
            region_specific = ["Lal Darwaza Bonalu", "Deccan Festival"]
        
        return common_festivals + region_specific
    
    def _get_regional_cuisine(self, region_name):
        """
        Get regional cuisine.
        
        Args:
            region_name (str): Region name.
        
        Returns:
            list: Regional cuisine.
        """
        # Common Telugu cuisine
        common_cuisine = ["Pulihora", "Pappu", "Annam", "Perugu", "Pachadi"]
        
        # Region-specific cuisine
        region_specific = []
        
        if "Coastal" in region_name:
            region_specific = ["Pulasa Pulusu", "Royyala Iguru", "Pesarattu"]
        elif "Rayalaseema" in region_name:
            region_specific = ["Ragi Sangati", "Rayalaseema Karam", "Boti Curry"]
        elif "Telangana" in region_name:
            region_specific = ["Sakinalu", "Sarva Pindi", "Jonna Rotte"]
        elif "Hyderabad" in region_name:
            region_specific = ["Hyderabadi Biryani", "Haleem", "Irani Chai"]
        
        return common_cuisine + region_specific
    
    def _get_regional_traditions(self, region_name):
        """
        Get regional traditions.
        
        Args:
            region_name (str): Region name.
        
        Returns:
            list: Regional traditions.
        """
        # Common Telugu traditions
        common_traditions = ["Muggulu", "Bhogi Mantalu", "Gobbemmalu"]
        
        # Region-specific traditions
        region_specific = []
        
        if "Coastal" in region_name:
            region_specific = ["Teppotsavam", "Fishing rituals"]
        elif "Rayalaseema" in region_name:
            region_specific = ["Mattu Pongal", "Cattle decoration"]
        elif "Telangana" in region_name:
            region_specific = ["Bathukamma flower arrangements", "Bonalu processions"]
        elif "Hyderabad" in region_name:
            region_specific = ["Charminar visits", "Old City traditions"]
        
        return common_traditions + region_specific
    
    def _get_language_patterns(self, dialect):
        """
        Get language patterns for dialect.
        
        Args:
            dialect (str): Dialect name.
        
        Returns:
            dict: Language patterns.
        """
        patterns = {
            "standard": {
                "sentence_endings": ["andi", "garu"],
                "common_phrases": ["bagunara", "ela unnaru"],
                "formality_level": "formal"
            },
            "coastal": {
                "sentence_endings": ["ayya", "amma"],
                "common_phrases": ["entandi", "avasaram ledu"],
                "formality_level": "mixed"
            },
            "rayalaseema": {
                "sentence_endings": ["le", "ra"],
                "common_phrases": ["yemittra", "yela unnav"],
                "formality_level": "informal"
            },
            "telangana": {
                "sentence_endings": ["anna", "akka"],
                "common_phrases": ["nakka", "kaduludu"],
                "formality_level": "informal"
            },
            "hyderabadi": {
                "sentence_endings": ["bhai", "yaar"],
                "common_phrases": ["nakko", "hau", "kaiku"],
                "formality_level": "mixed"
            },
            "uttarandhra": {
                "sentence_endings": ["ra", "ri"],
                "common_phrases": ["yenti", "yela"],
                "formality_level": "informal"
            }
        }
        
        return patterns.get(dialect, patterns["standard"])
    
    def _get_social_norms(self, era, setting_type):
        """
        Get social norms based on era and setting type.
        
        Args:
            era (str): Time period era.
            setting_type (str): Setting type.
        
        Returns:
            dict: Social norms.
        """
        # Default social norms
        social_norms = {
            "family_structure": "traditional",
            "gender_roles": "traditional",
            "community_interactions": "collective",
            "religious_practices": "traditional"
        }
        
        # Adjust based on era
        if era == "contemporary":
            social_norms["family_structure"] = "evolving"
            social_norms["gender_roles"] = "changing"
        elif era == "late-20th-century":
            social_norms["family_structure"] = "transitional"
            social_norms["gender_roles"] = "transitional"
        
        # Adjust based on setting type
        if setting_type == "urban":
            social_norms["community_interactions"] = "individualistic"
            social_norms["religious_practices"] = "modern"
        elif setting_type == "middle-class":
            social_norms["family_structure"] = "nuclear"
            social_norms["community_interactions"] = "selective"
        
        return social_norms
    
    def _should_use_colloquialisms(self, dialect, setting_type):
        """
        Determine if colloquialisms should be used.
        
        Args:
            dialect (str): Dialect name.
            setting_type (str): Setting type.
        
        Returns:
            bool: Whether to use colloquialisms.
        """
        # Use colloquialisms for informal dialects and rural/coastal settings
        if dialect in ["rayalaseema", "telangana", "uttarandhra"]:
            return True
        elif setting_type in ["rural", "coastal", "tribal"]:
            return True
        elif dialect == "hyderabadi" and setting_type == "urban":
            return True
        else:
            return False