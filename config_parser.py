from typing import Dict, Any


def is_valid_coord(coord: tuple, width: int, height: int) -> bool:
    x, y = coord
    return 0 <= x < width and 0 <= y < height


def parse_config(config_file: str) -> Dict[str, Any]:
    configs: Dict[str, Any] = {}

    try:
        with open(config_file, "r") as f:
            for line in f:
                clean_line = line.split("#")[0].strip()
                if not clean_line:
                    continue

                if "=" not in clean_line:
                    print(f"Invalid line: {clean_line}")
                    exit(1)

                parts = clean_line.split("=")
                if len(parts) != 2:
                    print(f"Invalid line: {clean_line}")
                    exit(1)

                key = parts[0].strip().upper()
                value = parts[1].strip()

                if not key or not value:
                    print("KEY and VALUE cannot be empty")
                    exit(1)

                configs[key] = value

        required_keys = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        ]

        for key in required_keys:
            if key not in configs:
                print(f"Missing key: {key}")
                exit(1)

        try:
            configs["WIDTH"] = int(configs["WIDTH"])
            configs["HEIGHT"] = int(configs["HEIGHT"])
        except ValueError:
            print("WIDTH and HEIGHT must be numbers")
            exit(1)

        if configs["WIDTH"] < 10 or configs["HEIGHT"] < 10:
            print("WIDTH and HEIGHT must be 10 or more")
            exit(1)

        try:
            entry_parts = configs["ENTRY"].split(",")
            exit_parts = configs["EXIT"].split(",")

            if len(entry_parts) != 2 or len(exit_parts) != 2:
                print("ENTRY and EXIT must be in x,y format")
                exit(1)

            entry = (int(entry_parts[0]), int(entry_parts[1]))
            exit_coord = (int(exit_parts[0]), int(exit_parts[1]))
        except ValueError:
            print("ENTRY and EXIT must contain valid integers")
            exit(1)

        if not is_valid_coord(entry, configs["WIDTH"], configs["HEIGHT"]):
            print("ENTRY is outside maze bounds")
            exit(1)

        if not is_valid_coord(exit_coord, configs["WIDTH"], configs["HEIGHT"]):
            print("EXIT is outside maze bounds")
            exit(1)

        if entry == exit_coord:
            print("ENTRY and EXIT cannot be the same")
            exit(1)

        configs["ENTRY"] = entry
        configs["EXIT"] = exit_coord
        perfect_value = configs["PERFECT"].lower()
        if perfect_value == "true":
            configs["PERFECT"] = True
        elif perfect_value == "false":
            configs["PERFECT"] = False
        else:
            print("PERFECT must be True or False")
            exit(1)

        if "SEED" in configs:
            try:
                configs["SEED"] = int(configs["SEED"])
            except ValueError:
                print("SEED must be a number")
                exit(1)
        else:
            configs["SEED"] = None

        return configs

    except FileNotFoundError:
        print(f"File not found: {config_file}")
        exit(1)
    except PermissionError:
        print("Permission denied")
        exit(1)