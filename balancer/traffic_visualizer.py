import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from functools import partial


def init_plot(servers: dict, ax):
    ax.set_title('Traffic distribution')
    ax.set_xlabel('Servers')
    ax.set_ylabel('Connection')
    ax.set_ylim(bottom=0, top=max(4, max(servers.values())+2))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    addresses = []
    for address, connection_num in servers.items():
        addresses.append(address)
    bars = ax.bar(addresses, [0]*len(servers))
    return bars


def update_plot(frame, bars, servers: dict):
    for i, (address, connections_num) in enumerate(servers.items()):
        bars[i].set_height(connections_num)
    return bars


def plot_traffic(servers: dict):
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    bars = init_plot(servers, ax)

    update = partial(update_plot, bars=bars, servers=servers)

    ani = animation.FuncAnimation(fig, update, interval=100, blit=True, cache_frame_data=False, frames=None)
    plt.show()