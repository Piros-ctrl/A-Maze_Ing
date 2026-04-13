from typing import Any, Dict, Tuple


def _is_valid_coord(
    coord: Tuple[int, int],
    width: int,
    height: int,
) -> bool:
    """Return True if coord is inside maze bounds."""
    row, col = coord
    return 0 <= row < height and 0 <= col < width


def parse_config(config_file: str) -> Dict[str, Any]:
    """Parse and validate a maze configuration file."""
    raw: Dict[str, str] = {}
    ALLOWED_KEYS = {
                    "WIDTH", "HEIGHT", "ENTRY", "EXIT",
                    "OUTPUT_FILE", "PERFECT", "SEED",
                }
    NOT_ALLOWED_NAME = {
        "a_maze_ing.py", "generator.py", "config_parser.py",
        "README.md", "requirements.txt", "pyproject.toml",
        "config.txt", "Makefile", ".gitignore", "__init__.py"
    }

    try:
        with open(config_file, "r") as f:
            for line_num, line in enumerate(f, start=1):
                # Remove inline comments and whitespace
                clean = line.split("#")[0].strip()
                if not clean:
                    continue

                if "=" not in clean:
                    raise ValueError(
                        f"Line {line_num}: invalid format '{clean}' "
                        "(expected KEY=VALUE)"
                    )

                key, _, value = clean.partition("=")
                key = key.strip().upper()
                value = value.strip()

                if not key or not value:
                    raise ValueError(
                        f"Line {line_num}: KEY and VALUE cannot be empty."
                    )

                if key not in ALLOWED_KEYS:
                    raise ValueError(
                        f"Line {line_num}: unknown key '{key}'. "
                        f"Allowed keys: {', '.join(sorted(ALLOWED_KEYS))}"
                    )

                if key == "OUTPUT_FILE":
                    if value in NOT_ALLOWED_NAME:
                        raise ValueError(
                            f"OUTPUT_FILE '{value}' is not allowed. "
                            f"Choose a different filename."
                        )

                if key in raw:
                    raise ValueError(
                        f"Line {line_num}: duplicate key '{key}' "
                        f"(already defined with value '{raw[key]}')."
                    )

                raw[key] = value

    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: '{config_file}'")
    except PermissionError:
        raise PermissionError(
            f"Permission denied when reading: '{config_file}'"
        )

    # --- Check mandatory keys -----------------------------------------------
    mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in mandatory:
        if key not in raw:
            raise ValueError(f"Missing mandatory key: {key}")

    config: Dict[str, Any] = {}

    # --- WIDTH and HEIGHT -------------------------------------------------
    try:
        config["WIDTH"] = int(raw["WIDTH"])
        config["HEIGHT"] = int(raw["HEIGHT"])
    except ValueError:
        raise ValueError("WIDTH and HEIGHT must be integers.")

    if config["WIDTH"] < 3 or config["HEIGHT"] < 3:
        raise ValueError("WIDTH and HEIGHT must be at least 3.")
    # --- ENTRY and EXIT -------------------------------------------------
    for key in ("ENTRY", "EXIT"):
        parts = raw[key].split(",")
        if len(parts) != 2:
            raise ValueError(
                f"{key} must be in 'row,col' format. Got: '{raw[key]}'"
            )
        try:
            coord: Tuple[int, int] = (int(parts[0]), int(parts[1]))
        except ValueError:
            raise ValueError(
                f"{key} must contain valid integers. Got: '{raw[key]}'"
            )

        if not _is_valid_coord(coord, config["WIDTH"], config["HEIGHT"]):
            raise ValueError(
                f"{key} {coord} is out of bounds for a "
                f"{config['WIDTH']}x{config['HEIGHT']} maze."
            )

        config[key] = coord

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT must be different cells.")

    # --- OUTPUT_FILE -------------------------------------------------
    config["OUTPUT_FILE"] = raw["OUTPUT_FILE"]

    # --- PERFECT -------------------------------------------------
    perfect_val = raw["PERFECT"].lower()
    if perfect_val in ("true", "1", "yes"):
        config["PERFECT"] = True
    elif perfect_val in ("false", "0", "no"):
        config["PERFECT"] = False
    else:
        raise ValueError(
            f"PERFECT must be True or False. Got: '{raw['PERFECT']}'"
        )

    # --- SEED (optional) -------------------------------------------------
    if "SEED" in raw:
        try:
            config["SEED"] = int(raw["SEED"])
        except ValueError:
            raise ValueError(
                f"SEED must be an integer. Got: '{raw['SEED']}'"
            )
    else:
        config["SEED"] = None

    return config
