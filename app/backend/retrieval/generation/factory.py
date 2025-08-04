"""
Factory for creating text generators.
"""
from typing import Any
from backend.core.config import settings
from backend.retrieval.generation.openai_generator import OpenAIGenerator


def create_generator(generator_type: str = "openai", **kwargs) -> Any:
    """
    Factory function to create text generators.
    
    Args:
        generator_type: Type of generator to create
        **kwargs: Additional arguments for the generator
        
    Returns:
        Generator instance
        
    Raises:
        ValueError: If generator type is not supported
    """
    if generator_type.lower() == "openai":
        return OpenAIGenerator(**kwargs)
    else:
        raise ValueError(f"Unsupported generator type: {generator_type}")


# Create global generator instance
generator = create_generator(
    generator_type="openai",
    model=settings.OPENAI_MODEL,
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
    temperature=settings.GENERATION_TEMPERATURE,
    max_tokens=settings.GENERATION_MAX_TOKENS,
    top_p=settings.GENERATION_TOP_P
)
