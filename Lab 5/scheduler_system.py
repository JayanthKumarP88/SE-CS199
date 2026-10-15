"""Conference Room and Equipment Scheduler System.

This module provides functionality to schedule rooms, manage equipment
pools, record booking conflicts, cancel reservations, and export schedules.
"""

from datetime import datetime
import json

# Global state
reservations = {}
equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
conflicts = []
STATE = {"next_reservation": 1}

def schedule_room(room_id, time_slot, equipment_list=None):
    """Schedule a room for a designated time slot with optional equipment."""
    if equipment_list is None:
        equipment_list = []

    slot_str = str(time_slot)
    for res in reservations.values():
        if res["room"] == room_id and res["slot"] == slot_str:
            conflicts.append(f"{room_id} double-booked at {slot_str}")

    for item in equipment_list:
        if item in equipment_pool:
            equipment_pool[item] -= 1

    current_id = STATE["next_reservation"]
    reservations[current_id] = {
        "room": room_id,
        "slot": slot_str,
        "equipment": equipment_list,
    }
    STATE["next_reservation"] += 1
    return current_id

def cancel_reservation(reservation_id):
    """Cancel an existing reservation and return allocated equipment to pool."""
    if reservation_id not in reservations:
        return False

    for item in reservations[reservation_id]["equipment"]:
        if item in equipment_pool:
            equipment_pool[item] += 1
    del reservations[reservation_id]
    return True

def slot_hours(time_slot):
    """Calculate duration in hours for a time slot given as 'start-end'."""
    start, end = str(time_slot).split("-")
    return abs(int(end) - int(start))

def export_schedule(file="schedule.json"):
    """Export current reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as f_out:
        json.dump(reservations, f_out, indent=4)

def log_conflicts(file="conflicts.log"):
    """Log recorded booking conflicts to a file and display contents."""
    with open(file, "a", encoding="utf-8") as f_out:
        for conflict in conflicts:
            f_out.write(f"{datetime.now()} {conflict}\n")

    with open(file, "r", encoding="utf-8") as f_in:
        print(f_in.read(), end="")

def main():
    """Execute room scheduling operations and display results."""
    _ = schedule_room("Board-1", "09-11")
    _ = schedule_room("Board-1", "09-11")
    res_b = schedule_room("Huddle-3", "12-14")
    _ = schedule_room("Huddle-3", "15-17")

    print("Slot length for b:", slot_hours(reservations[res_b]["slot"]))
    cancel_reservation(77)

    prompt = "Slot for Board-2, like 10-12 (Enter for 10-12): "
    slot = input(prompt) or "10-12"
    schedule_room("Board-2", slot, ["projector", "webcam"])

    export_schedule()
    log_conflicts()
    print("Equipment left:", equipment_pool)
    print("Reservations:", reservations)

if __name__ == "__main__":
    main()
