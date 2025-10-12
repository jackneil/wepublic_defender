import copy
import json
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

import json5
import openai
from openai import AzureOpenAI, OpenAI

logger = logging.getLogger(__name__)


class SettingsManager:
    def __init__(self, resource_dir: str, quality_setting: str = "best"):
        self.resource_dir = resource_dir
        self.quality_setting = quality_setting
        self.settings = None
        self.models_config = None
        self._specialty_cache: Dict[str, Dict] = {}  # Cache for merged specialty settings
        self._provider_clients: Dict[str, openai.OpenAI] = {}  # Store provider clients

    def load_settings(self, force_reload=False):
        """
        Load settings from all the json files. expected format is <specialty>_settings.json

        Args:
            force_reload: Whether to force reload the settings even if already loaded

        Returns:
            Dictionary with settings
        """
        if getattr(self, "settings", None) and not force_reload:
            return self.settings

        self.settings = defaultdict(dict)

        # Check for environment variable first, fallback to local settings directory
        settings_dir_env = os.getenv("KRAC_SETTINGS_DIR")
        if settings_dir_env and os.path.exists(settings_dir_env):
            self.settings_dir = settings_dir_env
            logger.info(
                f"Using settings directory from KRAC_SETTINGS_DIR env var: {self.settings_dir}"
            )
        else:
            self.settings_dir = os.path.join(os.path.dirname(__file__), "settings")
            if settings_dir_env:
                logger.warning(
                    f"KRAC_SETTINGS_DIR env var set to '{settings_dir_env}' but path doesn't exist. Using default: {self.settings_dir}"
                )
            else:
                logger.debug(
                    f"No KRAC_SETTINGS_DIR env var set. Using default settings directory: {self.settings_dir}"
                )
        for filepath in os.listdir(self.settings_dir):
            if filepath.endswith("_settings.json"):
                specialty = filepath.replace("_settings.json", "").split("_")[0].upper()
                quality = filepath.replace("_settings.json", "").split("_")[1].upper()
                mappings_file = os.path.join(self.settings_dir, filepath)
                try:
                    with open(mappings_file, "r") as f:
                        mappings_data = json5.load(f)
                        self.settings[specialty][quality] = mappings_data
                        logger.info(f"Loaded settings for {specialty} from {mappings_file}")
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    logger.error(
                        f"Error loading settings from {mappings_file}: {e}. Using default settings."
                    )
        with open(os.path.join(self.settings_dir, "llm_model_settings.json"), "r") as f:
            mappings_data = json5.load(f)
            self.settings.update(mappings_data)
            self.models_config = mappings_data.get("modelConfigurations", {})
            logger.info("Loaded settings from llm_model_settings.json")
        return self.settings

    def get_model_config(self, model_key: str):
        """Get model configuration by model key.

        Args:
            model_key: The model key (e.g., "gpt-oss-120b", "gpt-5-mini")

        Returns:
            Model configuration dict or None if not found
        """
        if not self.models_config:
            logger.warning(f"Model config not loaded. Cannot get model '{model_key}'.")
            return None
        if model_key not in self.models_config:
            available_models: list[str] = list(self.models_config.keys())
            logger.warning(
                f"Model '{model_key}' is not defined in self.models_config. Available models: {available_models}"
            )
            return None
        return self.models_config[model_key]

    def get_specialty_settings(self, specialty: str) -> Dict:
        if not self.settings:
            return {}
        return self.settings.get(specialty.upper(), {}).get(self.quality_setting.upper(), {})

    def get_setting(self, path: str, specialty: str = None, default=None):
        """
        Get a setting using dot notation path.

        Examples:
            # With specialty as parameter:
            get_setting('processingRules.noteTypes.LinesDrainsAirways.action', specialty='ANESTHESIA', default='allow')

            # With specialty in path:
            get_setting('ANESTHESIA.processingRules.noteTypes.LinesDrainsAirways.action', default='allow')

            # For top-level settings (not under specialty):
            get_setting('modelConfigurations.gpt-5-mini.temperature', default=0)

        Args:
            path: Dot-separated path to the setting
            specialty: Optional specialty (if not included in path)
            default: Default value if setting not found

        Returns:
            The setting value or default if not found
        """
        keys = path.split(".")

        # Check if first key is a specialty
        if self.settings and keys[0].upper() in self.settings and not specialty:
            # Specialty is in the path
            specialty = keys[0].upper()
            keys = keys[1:]  # Remove specialty from keys

            # Get the specialty settings for the current quality level
            if not self.settings:
                return default
            value: Any = self.settings.get(specialty, {}).get(self.quality_setting.upper(), {})
        elif specialty:
            # Specialty provided as parameter
            value = self.get_specialty_settings(specialty)
        else:
            # No specialty - look in top-level settings
            value = self.settings if self.settings else {}

        # Navigate through the keys
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    def get_code_group_settings(self, code_group: str, specialty: str) -> Optional[Dict]:
        """
        Get settings for a specific code group.

        Args:
            code_group: The code group to get settings for

        Returns:
            Dictionary with code group settings
        """
        if not self.settings:
            logger.error(
                f"No settings loaded. Cannot get code group settings for specialty: {specialty}"
            )
            return None

        mappings_data = self.settings.get(specialty.upper(), {}).get(
            self.quality_setting.upper(), {}
        )
        if not mappings_data:
            available_specialties: list[str] = list(self.settings.keys())
            logger.error(
                f"No settings found for specialty: {specialty}. Choices are {available_specialties}"
            )
            return None

        code_group_settings = mappings_data.get("codeGroupSettings", {})

        # If code group exists in settings, return those settings
        if code_group in code_group_settings:
            return code_group_settings[code_group]

        # Otherwise, return default settings
        return mappings_data.get("defaultCodeGroupSettings", {})

    def get_extraction_models_for_note_type(self, note_type: str, specialty: str) -> List[str]:
        """
        Get extraction model names for a specific note type.

        Args:
            note_type: The note type to get extraction models for
            specialty: The medical specialty

        Returns:
            List of extraction model names
        """
        if not self.settings:
            logger.error(
                f"No settings loaded. Cannot get extraction models for specialty: {specialty}"
            )
            return []

        mappings_data = self.settings.get(specialty.upper(), {}).get(
            self.quality_setting.upper(), {}
        )
        if not mappings_data:
            available_specialties: list[str] = list(self.settings.keys())
            logger.error(
                f"No settings found for specialty: {specialty}. Choices are {available_specialties}"
            )
            return []

        note_type_to_models = mappings_data.get("noteTypeToExtractionModels", {})

        # Check for direct match
        if note_type in note_type_to_models:
            return note_type_to_models[note_type]

        # Check for partial matches (similar to code group mapper)
        for key, value in note_type_to_models.items():
            if key in note_type:
                return value

        return []

    def get_extraction_model_settings(self, extraction_model: str, specialty: str) -> Dict:
        """
        Get settings for a specific extraction model.

        Args:
            extraction_model: The extraction model to get settings for
            specialty: The medical specialty

        Returns:
            Dictionary with extraction model settings
        """
        if not self.settings:
            logger.error(
                f"No settings loaded. Cannot get extraction model settings for specialty: {specialty}"
            )
            return {}

        mappings_data = self.settings.get(specialty.upper(), {}).get(
            self.quality_setting.upper(), {}
        )
        if not mappings_data:
            available_specialties: list[str] = list(self.settings.keys())
            logger.error(
                f"No settings found for specialty: {specialty}. Choices are {available_specialties}"
            )
            return {}

        extraction_settings = mappings_data.get("extractionModelSettings", {})

        # If extraction model exists in settings, return those settings
        if extraction_model in extraction_settings:
            return extraction_settings[extraction_model]

        # Otherwise, return default extraction settings (or empty dict)
        return extraction_settings.get("default", {})

    def get_customer_settings(self, customer_id: str, specialty: str) -> Optional[Dict]:
        """
        Get settings for a specific customer.

        Args:
            customer_id: The ID of the customer

        Returns:
            Dictionary with customer settings
        """
        if not self.settings:
            logger.error(
                f"No settings loaded. Cannot get customer settings for specialty: {specialty}"
            )
            return None

        mappings_data = self.settings.get(specialty.upper(), {}).get(
            self.quality_setting.upper(), {}
        )
        if not mappings_data:
            available_specialties: list[str] = list(self.settings.keys())
            logger.error(
                f"No settings found for specialty: {specialty}. Choices are {available_specialties}"
            )
            return None

        customer_settings = mappings_data.get("customerSettings", {})

        # If customer ID is provided and exists in settings, return those settings
        if customer_id in customer_settings:
            return customer_settings[customer_id]

        # Otherwise, return default settings
        return customer_settings.get("default", {})

    def get_model_within_customer_constraint(
        self, requested_model: str, customer_settings: Dict, specialty: str
    ):
        """
        Get the appropriate model within customer constraints.

        Args:
            requested_model: The model requested for use
            customer_settings: Dictionary with customer settings

        Returns:
            The appropriate model to use
        """
        max_model = customer_settings.get("maxModel")
        if not max_model:
            return requested_model

        if not self.settings:
            logger.error(
                f"No settings loaded. Cannot get model constraints for specialty: {specialty}"
            )
            return requested_model

        mappings_data = self.settings.get(specialty.upper(), {}).get(
            self.quality_setting.upper(), {}
        )
        if not mappings_data:
            available_specialties: list[str] = list(self.settings.keys())
            logger.error(
                f"No settings found for specialty: {specialty}. Choices are {available_specialties}"
            )
            return requested_model

        model_hierarchy = mappings_data.get("modelHierarchy", [])
        if not model_hierarchy:
            return requested_model

        try:
            requested_index = model_hierarchy.index(requested_model)
        except ValueError:
            # If requested model not in hierarchy, default to the first model
            requested_index = 0

        try:
            max_index = model_hierarchy.index(max_model)
        except ValueError:
            # If max model not in hierarchy, allow any model
            return requested_model

        # If requested model is higher in the hierarchy than the max allowed model,
        # return the max allowed model
        if requested_index > max_index:
            return max_model

        # Otherwise, return the requested model
        return requested_model

    def get_model_timeout(
        self,
        model_name: str,
        effort: Optional[str] = None,
        context_flags: Optional[List[str]] = None,
        service_tier: Optional[str] = None,
        input_size: Optional[int] = None,
    ) -> int:
        """
        Get the appropriate timeout for a model based on effort level, context, service tier, and input size.

        Args:
            model_name: The name of the model
            effort: The effort level (minimal, low, medium, high)
            context_flags: List of context flags that may affect timeout (e.g., ["file_search", "retry_attempt_2"])
            service_tier: The OpenAI service tier (flex, priority, standard, auto)
            input_size: Size of the input in characters (used to scale timeout)

        Returns:
            Timeout in seconds
        """
        # Ensure settings are loaded
        if not self.settings:
            self.load_settings()

        if self.settings is None:
            raise RuntimeError("Settings should be loaded")
        if self.models_config is None:
            raise RuntimeError("Models config should be loaded")

        # Get timeout config
        timeout_config: dict[str, Any] = self.settings.get("timeoutConfig", {})
        global_default = timeout_config.get("globalDefault", 120)
        multipliers = timeout_config.get("multipliers", {})
        max_timeout = timeout_config.get("maxTimeout", 900)

        # Get model config
        model_config: dict[str, Any] = self.models_config.get(model_name, {})
        model_timeouts = model_config.get("timeouts", {})

        # Get base timeout
        if effort and effort in model_timeouts:
            timeout = model_timeouts[effort]
        elif "default" in model_timeouts:
            timeout = model_timeouts["default"]
        else:
            timeout = global_default

        # Apply input size scaling
        # Scale timeout based on input size (e.g., add 1 second per 10,000 chars)
        if input_size:
            # Define scaling thresholds
            small_input = 10000  # 10k chars
            medium_input = 50000  # 50k chars
            large_input = 100000  # 100k chars

            if input_size > large_input:
                # For very large inputs, add significant extra time
                input_multiplier = 1.5 + (input_size - large_input) / 100000 * 0.5
            elif input_size > medium_input:
                # For medium-large inputs, moderate scaling
                input_multiplier = 1.2 + (input_size - medium_input) / 50000 * 0.3
            elif input_size > small_input:
                # For small-medium inputs, minor scaling
                input_multiplier = 1.0 + (input_size - small_input) / 40000 * 0.2
            else:
                # Small inputs, no scaling
                input_multiplier = 1.0

            timeout = timeout * input_multiplier

        # Apply service tier multiplier first
        if service_tier and "service_tier" in multipliers:
            service_tier_multipliers = multipliers.get("service_tier", {})
            if service_tier in service_tier_multipliers:
                timeout = timeout * service_tier_multipliers[service_tier]

        # Apply other multipliers
        if context_flags:
            for flag in context_flags:
                if flag in multipliers and flag != "service_tier":
                    timeout = timeout * multipliers[flag]
                # Handle retry attempts dynamically
                elif flag.startswith("retry_attempt_"):
                    attempt_num = flag.replace("retry_attempt_", "")
                    if f"retry_attempt_{attempt_num}" in multipliers:
                        timeout = timeout * multipliers[f"retry_attempt_{attempt_num}"]

        # Cap at maximum
        return min(int(timeout), max_timeout)

    def get_provider_config(self, provider_name: str) -> Optional[Dict]:
        """
        Get configuration for a specific provider.

        Args:
            provider_name: Name of the provider (e.g., 'openai', 'xai', 'groq')

        Returns:
            Provider configuration dictionary or None if not found
        """
        if not self.settings:
            self.load_settings()

        if self.settings is None:
            raise RuntimeError("Settings should be loaded")
        providers: dict[str, Any] = self.settings.get("providers", {})
        if provider_name not in providers:
            logger.error(f"Provider '{provider_name}' not found in configuration")
            return None

        return providers[provider_name]

    def get_model_provider(self, model_name: str) -> Optional[str]:
        """
        Get the provider name for a specific model.

        Args:
            model_name: Name of the model

        Returns:
            Provider name or None if not found
        """
        if not self.models_config:
            self.load_settings()

        if self.models_config is None:
            raise RuntimeError("Models config should be loaded")
        model_config: dict[str, Any] = self.models_config.get(model_name, {})
        return model_config.get(
            "provider", "openai"
        )  # Default to openai for backward compatibility

    def create_client_for_model(self, model_name: str) -> Optional[openai.OpenAI]:
        """
        Create an OpenAI client configured for the model's provider.

        Args:
            model_name: Name of the model to create client for

        Returns:
            Configured OpenAI client or None if configuration not found
        """
        # Get provider for this model
        provider_name = self.get_model_provider(model_name)
        if not provider_name:
            logger.error(f"No provider found for model '{model_name}'")
            return None

        # Get provider configuration
        provider_config = self.get_provider_config(provider_name)
        if not provider_config:
            return None

        # Get API key from environment
        api_key_env_var = provider_config.get("api_key_env_var")
        if not api_key_env_var:
            logger.error(
                f"No API key environment variable configured for provider '{provider_name}'"
            )
            return None

        api_key = os.getenv(api_key_env_var)
        if not api_key:
            logger.error(
                f"API key not found in environment variable '{api_key_env_var}' for provider '{provider_name}'"
            )
            return None

        # Create client based on provider type
        client_type = provider_config.get("client_type", "openai")

        if client_type == "openai":
            # Standard OpenAI-compatible client
            base_url = provider_config.get("base_url")
            client_params = {"api_key": api_key}
            if base_url:
                client_params["base_url"] = base_url

            logger.info(
                f"Creating OpenAI client for model '{model_name}' using provider '{provider_name}' with base_url: {base_url}"
            )
            return openai.OpenAI(**client_params)

        elif client_type == "azure_openai":
            # Azure OpenAI requires special handling
            endpoint = os.getenv(provider_config.get("endpoint_env_var", ""))
            if not endpoint:
                logger.error(f"Azure endpoint not found for provider '{provider_name}'")
                return None

            return AzureOpenAI(
                api_key=api_key,
                azure_endpoint=endpoint,
                api_version=provider_config.get("api_version", "2024-10-01-preview"),
            )

        else:
            logger.error(f"Unsupported client type '{client_type}' for provider '{provider_name}'")
            return None

    def check_feature_support(self, model_name: str, feature: str) -> bool:
        """
        Check if a model's provider supports a specific feature.

        Args:
            model_name: Name of the model
            feature: Feature to check (e.g., 'responses', 'file_search', 'reasoning')

        Returns:
            True if feature is supported, False otherwise
        """
        provider_name = self.get_model_provider(model_name)
        if not provider_name:
            return False

        provider_config = self.get_provider_config(provider_name)
        if not provider_config:
            return False

        supported_features = provider_config.get("supported_features", {})
        return supported_features.get(feature, False)

    def create_provider_clients(self) -> Dict:
        """
        Create clients for all configured providers.

        Returns:
            Dictionary mapping provider names to their client instances
        """

        if not self.settings:
            self.load_settings()

        if self.settings is None:
            raise RuntimeError("Settings should be loaded")

        provider_clients = {}
        providers: dict[str, Any] = self.settings.get("providers", {})

        for provider_name, provider_config in providers.items():
            api_key_env_var = provider_config.get("api_key_env_var")
            if not api_key_env_var:
                logger.warning(
                    f"No API key env var configured for provider {provider_name}, skipping"
                )
                continue

            # Check if API key exists in environment
            provider_api_key = os.getenv(api_key_env_var)

            if not provider_api_key:
                if provider_name == "openai":
                    provider_api_key = os.getenv("OPENAI_API_KEY")
                    if provider_api_key:
                        logger.info(
                            f"Using OPENAI_API_KEY env var for OpenAI provider because {api_key_env_var} env var not found"
                        )

            if not provider_api_key:
                logger.info(
                    f"API key not found for provider {provider_name} (env var: {api_key_env_var}), skipping"
                )
                continue

            # Create client based on provider type
            client_type = provider_config.get("client_type", "openai")

            try:
                if client_type == "openai":
                    # Standard OpenAI-compatible client
                    base_url = provider_config.get("base_url")
                    client_params = {"api_key": provider_api_key}
                    if base_url:
                        client_params["base_url"] = base_url

                    provider_clients[provider_name] = OpenAI(**client_params)
                    logger.info(f"Created {provider_name} client with base_url: {base_url}")

                elif client_type == "azure_openai":
                    # Azure OpenAI requires special handling
                    endpoint = os.getenv(provider_config.get("endpoint_env_var", ""))
                    if endpoint:
                        provider_clients[provider_name] = AzureOpenAI(
                            api_key=provider_api_key,
                            azure_endpoint=endpoint,
                            api_version=provider_config.get("api_version", "2024-10-01-preview"),
                        )
                        logger.info(f"Created Azure OpenAI client for {provider_name}")
                    else:
                        logger.warning(f"Azure endpoint not found for provider {provider_name}")

            except Exception as e:
                logger.error(f"Failed to create client for provider {provider_name}: {e}")
                continue

        return provider_clients

    def _deep_merge(self, base: dict, override: dict) -> dict:
        """
        Deep merge override into base, only replacing leaf values.

        Args:
            base: Base dictionary
            override: Override dictionary

        Returns:
            Merged dictionary (new instance)
        """
        result = copy.deepcopy(base)

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursive merge for nested dicts
                result[key] = self._deep_merge(result[key], value)
            else:
                # Replace leaf value
                result[key] = value

        return result

    def load_facility_settings(self, facility_id: str, specialty: str) -> Optional[dict]:
        """
        Load facility-specific settings from a JSON file.

        Args:
            facility_id: The facility ID (e.g., 'nph_elcm')
            specialty: The medical specialty (e.g., 'ANESTHESIA')

        Returns:
            Dictionary with facility settings or None if not found
        """

        if not facility_id:
            return None

        # Build the path to the facility config file
        facility_config_path = os.path.join(
            self.settings_dir, "facility_configs", specialty.upper(), f"{facility_id}.json"
        )

        if os.path.exists(facility_config_path):
            logger.info(f"Loading facility settings from: {facility_config_path}")
            with open(facility_config_path, "r") as f:
                facility_settings = json5.load(f)
            logger.info(
                f"Loaded facility settings for {facility_settings.get('facilityName', facility_id)}"
            )
            return facility_settings
        else:
            logger.warning(f"Facility config file not found: {facility_config_path}")
            return None

    def with_facility_overrides(
        self, facility_settings: Optional[dict], specialty: str
    ) -> "SettingsManager":
        """
        Create a new SettingsManager instance with facility overrides applied.
        Thread-safe - creates a new instance without modifying the original.

        Args:
            facility_settings: Facility-specific settings overrides
            specialty: The specialty to apply overrides for

        Returns:
            New SettingsManager instance with overrides applied
        """

        # Create new instance
        new_manager = SettingsManager(
            resource_dir=self.resource_dir, quality_setting=self.quality_setting
        )

        # Copy internal state
        new_manager.settings = copy.deepcopy(self.settings) if self.settings else None
        new_manager.models_config = (
            copy.deepcopy(self.models_config) if self.models_config else None
        )
        new_manager._provider_clients = self._provider_clients  # These are stateless, can share

        # Copy settings_dir if it exists, otherwise it will be set when load_settings is called
        if hasattr(self, "settings_dir"):
            new_manager.settings_dir = self.settings_dir

        # Get base specialty settings and merge with facility overrides
        if facility_settings and self.settings:
            base_settings = self.get_specialty_settings(specialty)
            merged_settings = self._deep_merge(base_settings, facility_settings)

            # Update the settings for this specialty in the new manager
            if specialty.upper() not in new_manager.settings:
                new_manager.settings[specialty.upper()] = {}
            new_manager.settings[specialty.upper()][self.quality_setting.upper()] = merged_settings

            # Cache the merged settings
            new_manager._specialty_cache[specialty] = merged_settings
        else:
            # Just copy the cache if no overrides
            new_manager._specialty_cache = self._specialty_cache.copy()

        return new_manager
