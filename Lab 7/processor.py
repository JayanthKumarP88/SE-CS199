def validate_height_and_fastpass(rider_spec):
    if not isinstance(rider_spec, str):
        return "Invalid rider specification"

    cleaned = rider_spec.strip()
    if ":" not in cleaned:
        return "Invalid rider specification"

    parts = cleaned.split(":")
    if len(parts) != 2:
        return "Invalid rider specification"

    height_str, pass_str = parts[0].strip(), parts[1].strip().upper()
    try:
        height = int(height_str)
        if height <= 0 or height > 300:
            return "Invalid rider specification"
    except (ValueError, TypeError):
        return "Invalid rider specification"

    pass_map = {"YES": True, "NO": False}
    if pass_str not in pass_map:
        return "Invalid rider specification"

    has_fastpass = pass_map[pass_str]
    eligible = height >= 120
    status = "FastPass Priority" if has_fastpass else "Standard Entry"
    return f"Height {height}cm: {'Approved' if eligible else 'Denied'} ({status})"


def compute_dispatch_throughput(ride_metric_str):
    if not isinstance(ride_metric_str, str):
        return 0.0

    cleaned = ride_metric_str.strip()
    if "/" not in cleaned:
        return 0.0

    parts = cleaned.split("/")
    if len(parts) != 2:
        return 0.0

    try:
        riders = float(parts[0].strip())
        cycle_mins = float(parts[1].strip())
        if cycle_mins <= 0 or riders < 0:
            return 0.0
        rate = riders / cycle_mins
        return round(rate, 2)
    except (ValueError, ZeroDivisionError, OverflowError):
        return 0.0


def resolve_safety_restraint_code(zone_code):
    if not isinstance(zone_code, str):
        return "Unknown Restraint / Invalid Code"

    prefix = zone_code.strip().upper()[:3]
    restraint_types = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar",
    }
    return restraint_types.get(prefix, "Unknown Restraint / Invalid Code")


def main():
    print("==== Running validate_height_and_fastpass ====")
    r_input = input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    print(validate_height_and_fastpass(r_input))

    print("\n==== Running compute_dispatch_throughput ====")
    t_input = input("Enter riders/mins (e.g. 48/2.5): ")
    print("Throughput (riders/min):", compute_dispatch_throughput(t_input))

    print("\n==== Running resolve_safety_restraint_code ====")
    z_input = input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    print("Restraint:", resolve_safety_restraint_code(z_input))


if __name__ == "__main__":
    main()
