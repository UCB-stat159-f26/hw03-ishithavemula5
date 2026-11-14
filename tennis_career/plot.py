import matplotlib.pyplot as plt

def plot_player_matches(matches):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {"W": "#4acbed", "L": "#953a8c"}
    for result in ["W", "L"]:
        data = matches[matches["result"] == result]
        ax.scatter(data["player_age"], data["age_diff"],
                   color=colors[result], s=12, alpha=0.7,
                   label="Win" if result == "W" else "Loss")

    ax.axhline(0, color="gray", linewidth=0.8) 
    ax.set_xlabel("Player Age")
    ax.set_ylabel("Player Age - Opponent Age")
    ax.legend()
    return fig
