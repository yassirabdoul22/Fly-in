# Fly_in_main.py
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from src.parser.lexer import Lexer
from src.parser.parser import Parser
from src.models.zone import ZoneType

ZONE_COLOR = {
    ZoneType.NORMAL:     "#00bcd4",
    ZoneType.PRIORITY:   "#4caf50",
    ZoneType.RESTRICTED: "#f44336",
    ZoneType.BLOCKED:    "#616161",
}
START_COLOR = "#69f0ae"
GOAL_COLOR  = "#ffd740"
ZONE_RADIUS = 0.5


def plot_graph(config: object) -> None:
    """
    Display the drone network as a matplotlib window.

    Each zone is a colored circle with its name centered inside.
    Connections are drawn as dashed lines between zones.

    Args:
        config: ParsedConfig object from the parser.
    """
    graph      = config.graph       # type: ignore[union-attr]
    start_zone = config.start_zone  # type: ignore[union-attr]
    goal_zone  = config.goal_zone   # type: ignore[union-attr]

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")
    ax.set_title("Drone Network Map", color="white", fontsize=14, fontweight="bold")
    ax.set_xlabel("X", color="white")
    ax.set_ylabel("Y", color="white")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444466")

    # ── Connexions ────────────────────────────────────────────────────────────
    visited: set = set()
    for zone_name, neighbours in graph.connections.items():
        z1 = graph.zones[zone_name]
        for neighbour_name in neighbours:
            edge = (min(zone_name, neighbour_name), max(zone_name, neighbour_name))
            if edge in visited:
                continue
            visited.add(edge)
            z2 = graph.zones[neighbour_name]
            ax.plot(
                [z1.x, z2.x], [z1.y, z2.y],
                color="#aaaacc", linewidth=1.5, linestyle="--", zorder=1,
            )

    # ── Zones ─────────────────────────────────────────────────────────────────
    for zone in graph.zones.values():
        if zone == start_zone:
            color = START_COLOR
        elif zone == goal_zone:
            color = GOAL_COLOR
        else:
            color = ZONE_COLOR.get(zone.z_type, "#00bcd4")

        circle = plt.Circle(
            (zone.x, zone.y), ZONE_RADIUS,
            color=color, ec="white", lw=1.5, zorder=2,
        )
        ax.add_patch(circle)
        ax.text(
            zone.x, zone.y, zone.name,
            ha="center", va="center",
            fontsize=8, fontweight="bold", color="white", zorder=3,
        )

    # ── Légende ───────────────────────────────────────────────────────────────
    legend_items = [
        mpatches.Patch(color=START_COLOR, label="Start"),
        mpatches.Patch(color=GOAL_COLOR,  label="Goal"),
        mpatches.Patch(color=ZONE_COLOR[ZoneType.NORMAL],     label="Normal"),
        mpatches.Patch(color=ZONE_COLOR[ZoneType.PRIORITY],   label="Priority"),
        mpatches.Patch(color=ZONE_COLOR[ZoneType.RESTRICTED], label="Restricted"),
        mpatches.Patch(color=ZONE_COLOR[ZoneType.BLOCKED],    label="Blocked"),
    ]
    ax.legend(
        handles=legend_items, loc="upper left",
        facecolor="#2a2a4a", labelcolor="white", fontsize=9,
    )

    all_x = [z.x for z in graph.zones.values()]
    all_y = [z.y for z in graph.zones.values()]
    pad = 1.5
    ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
    ax.set_ylim(min(all_y) - pad, max(all_y) + pad)
    ax.set_aspect("equal")
    plt.tight_layout()
    plt.show()


def main() -> None:
    """Entry point: parse the map file and display the network as a plot."""
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "map.txt"
    )
    lexer = Lexer(config_path)
    lexer.read_file()
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    config = parser.parse()

    plot_graph(config)


if __name__ == "__main__":
    main()