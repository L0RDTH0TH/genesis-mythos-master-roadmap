"""
Config contract: parse snippet, confidence bands, fallbacks (Second-Brain-Config, Parameters).
"""


def get_confidence_band(confidence: int, config: dict | None = None) -> str:
    """
    Return 'high', 'mid', or 'low' per Parameters.md.
    Default: high >=85%, mid 72-84%, low <72%.
    Config overrides: confidence_bands.mid [min,max], confidence_bands.high_threshold.
    """
    if config and "confidence_bands" in config:
        cb = config["confidence_bands"]
        high_threshold = cb.get("high_threshold", 85)
        mid = cb.get("mid", [72, 84])
        mid_min, mid_max = mid[0], mid[1]
    else:
        high_threshold = 85
        mid_min, mid_max = 72, 84
    if confidence >= high_threshold:
        return "high"
    if mid_min <= confidence <= mid_max:
        return "mid"
    return "low"


def parse_config_snippet(content: str) -> dict:
    """
    Simple key-value parse from frontmatter-like snippet (no full YAML).
    Lines of form 'key: value' or 'key: 123'.
    """
    result = {}
    for line in content.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            idx = line.index(":")
            key = line[:idx].strip()
            value = line[idx + 1 :].strip()
            if value.isdigit():
                result[key] = int(value)
            elif value.startswith("[") and "]" in value:
                result[key] = value
            else:
                result[key] = value
    return result
