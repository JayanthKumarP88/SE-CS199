# Maze Runner

Navigate through a procedurally generated maze to reach the exit using **Pygame**.

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| W / UP | Move up |
| S / DOWN | Move down |
| A / LEFT | Move left |
| D / RIGHT | Move right |
| R | Generate new maze |

## Tasks to Complete

### Task 1: Shortest Path Hint
> Press H to show the solution path highlighted in the maze.

### Task 2: Fog of War
> Only show maze cells within a radius of 3 cells around the player; the rest is dark.

### Task 3: Timer Leaderboard
> Track the top 5 best completion times and display them after solving.

### Task 4: Larger Maze Difficulty Tiers
> Add Easy (10x8), Medium (15x13), Hard (20x18) options selectable at start.

## Folder Structure

```
maze-runner/
├── main.py
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── maze.py
│   └── player.py
└── README.md
```

## Submission Checklist

- [ ] All 4 tasks completed
- [ ] Maze is generated fresh each session (R key)
- [ ] Fog of war renders correctly
- [ ] Timer leaderboard persists to JSON
- [ ] Code reviewed with LLM (include chat link)
