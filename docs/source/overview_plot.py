"""
Builds an animation of the format interchange process for the OMF library.

This script will be executed by the conf.py and the gif will be saved in the
docs/source/_static directory.

The plot is a DiGraph with a centre node called omf-io. Nodes on the left will indicate the formats
that are readable by the library and nodes on the right will indicate the formats that are writable by the library.

The source nodes and target nodes are the same (based on the design to support both io for a supported format).

The nodes should have a dotted edge if planned, or a solid edge if implemented.
The nodes should be colored based on the format being memory (objects) or file (on-disk).

"""
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

# 7N9GWW
# Define the formats dictionary
FORMATS = {
    'omf': {'status': 'In Progress', 'format_type': 'memory-file'},
    'pandas': {'status': 'In Progress', 'format_type': 'memory'},
    'geopandas': {'status': 'In Progress', 'format_type': 'memory'},
    'parquet': {'status': 'Planned', 'format_type': 'file'},
    'csv': {'status': 'In Progress', 'format_type': 'file'},
    'ply': {'status': 'In Progress', 'format_type': 'file'},
    'geojson': {'status': 'Planned', 'format_type': 'file'},
    'tiff': {'status': 'Planned', 'format_type': 'file'},
    'geoh5': {'status': 'Planned', 'format_type': 'file'},
    'pyvista(vtk)': {'status': 'Planned', 'format_type': 'memory-file'},
}

orange_rgb = (218 / 255, 114 / 255, 55 / 255)
ANIMATION_DICT = {
    'step0': {'subtitle': '[1] Create OMF assets'},
    'step1': {('from_ply', 'omf-io'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
              'subtitle': '[1] Create OMF assets'},
    'step2': {('omf-io', 'to_omf'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
              'subtitle': '[1] Create OMF assets'},
    'step3': {('from_tiff', 'omf-io'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
              'subtitle': '[1] Create OMF assets'},
    'step4': {('from_parquet', 'omf-io'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
              'subtitle': '[1] Create OMF assets'},
    'step5': {'subtitle': '[2] Export OMF assets', 'reset': True},
    'step6': {('from_omf', 'omf-io'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
              'subtitle': '[2] Export OMF assets'},
    'step7': {('omf-io', 'to_ply'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
              'subtitle': '[2] Export OMF assets'},
    'step8': {('omf-io', 'to_tiff'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
              'subtitle': '[2] Export OMF assets'},
    'step9': {('omf-io', 'to_parquet'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
              'subtitle': '[2] Export OMF assets'},
    'step10': {'subtitle': '[3] Adhoc Conversion (non-OMF)', 'reset': True},
    'step11': {('from_pandas', 'omf-io'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
               'subtitle': '[3] Adhoc Conversion (non-OMF)'},
    'step12': {('omf-io', 'to_pyvista(vtk)'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
               'subtitle': '[3] Adhoc Conversion (non-OMF)'},
    'step13': {('from_parquet', 'omf-io'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
               'subtitle': '[3] Adhoc Conversion (non-OMF)'},
    'step14': {('from_tiff', 'omf-io'): {'color': orange_rgb, 'style': 'solid', 'width': 4},
               'subtitle': '[3] Adhoc Conversion (non-OMF)'},
}

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D


class OMFIOPlot:
    def __init__(self, formats):
        """
        Initialize the OMFIOPlot instance.

        Args:
            formats (dict): Dictionary defining the formats and their properties.
        """
        self.formats = formats
        self.G = nx.DiGraph()
        self.pos = {}
        self.node_colors = {}
        self.edge_styles = []

        self._build_graph()
        self._define_layout()
        self._define_styles()

    def _build_graph(self):
        """Build the directed graph."""
        self.G.add_node('omf-io', format_type='center')
        for format_name, properties in self.formats.items():
            self.G.add_node(f"from_{format_name}", status=properties['status'], format_type=properties['format_type'])
            self.G.add_node(f"to_{format_name}", status=properties['status'], format_type=properties['format_type'])
            self.G.add_edge(f"from_{format_name}", 'omf-io')
            self.G.add_edge('omf-io', f"to_{format_name}")

    def _define_layout(self):
        """Define the layout for the graph."""
        x_offset = -1
        for i, format_name in enumerate(reversed(self.formats.keys())):
            self.pos[f"from_{format_name}"] = (x_offset, i)
        x_offset = 1
        for i, format_name in enumerate(reversed(self.formats.keys())):
            self.pos[f"to_{format_name}"] = (x_offset, i)
        self.pos['omf-io'] = (0, len(self.formats) / 2)

    def _define_styles(self):
        """Define node colors and edge styles."""
        for node, data in self.G.nodes(data=True):
            if data['format_type'] == 'memory':
                self.node_colors[node] = '#87CEEB'
            elif data['format_type'] == 'file':
                self.node_colors[node] = '#98FB98'
            elif data['format_type'] == 'memory-file':
                self.node_colors[node] = '#FFD580'
            elif node == 'omf-io':
                self.node_colors[node] = '#FF7F50'

        for edge in self.G.edges:
            if edge[1] == 'omf-io':
                status = self.G.nodes[edge[0]].get('status')
            else:
                status = self.G.nodes[edge[1]].get('status')

            if status == 'Complete':
                self.edge_styles.append(('solid', 'green'))
            elif status == 'In Progress':
                self.edge_styles.append(('solid', 'black'))
            elif status == 'Planned':
                self.edge_styles.append(('solid', 'grey'))

    def plot_static(self, highlight_edges=None, ax=None):
        """
        Generate a static plot with optional edge highlighting.

        Args:
            highlight_edges (dict, optional): Dictionary of edges to highlight with their styles.
                                               Example: {('from_omf', 'omf-io'): {'color': 'red', 'style': 'dashed'}}
            ax (matplotlib.axes.Axes, optional): The axes object to draw the plot on.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 8))  # Create a new figure and axes if none are provided

        # Turn off the axis box
        ax.axis('off')

        # Set axis box color to grey
        for spine in ax.spines.values():
            spine.set_edgecolor('lightgrey')
            spine.set_linewidth(1.5)

        # Draw edges with styles
        for edge, (style, color) in zip(self.G.edges, self.edge_styles):
            edge_style = style
            edge_color = color
            edge_width = 1.0

            # Apply highlighting if the edge is in the highlight_edges dictionary
            if highlight_edges and edge in highlight_edges:
                edge_style = highlight_edges[edge].get('style', style)
                edge_color = highlight_edges[edge].get('color', color)
                edge_width = highlight_edges[edge].get('width', edge_width)

            nx.draw_networkx_edges(
                self.G, self.pos, edgelist=[edge], style=edge_style, edge_color=edge_color, arrows=True,
                width=edge_width, connectionstyle="arc3,rad=0.2", arrowsize=30, ax=ax
            )

        # Draw labels and other elements on the provided ax
        for node, (x, y) in self.pos.items():
            label = node
            if node == 'omf-io':
                ax.text(
                    x, y, label, fontsize=10, ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.6", edgecolor='black', facecolor=self.node_colors[node], pad=1.0)
                )
            elif node.startswith('from_') or node.startswith('to_'):
                ax.text(
                    x, y, label, fontsize=10, ha='right' if node.startswith('from_') else 'left', va='center',
                    bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor=self.node_colors[node], pad=0.5)
                )

        # Set axis limits and legends
        x_values, y_values = zip(*self.pos.values())
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        padding = 1.0
        ax.set_xlim(x_min - padding, x_max + padding)
        ax.set_ylim(y_min - padding, y_max + padding)

        # Add legends and remove ticks
        format_legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Memory', markerfacecolor='#87CEEB', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='File', markerfacecolor='#98FB98', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Memory/File', markerfacecolor='#FFD580', markersize=10),
        ]
        status_legend_elements = [
            Line2D([0], [0], color='green', lw=2, linestyle='solid', label='Complete'),
            Line2D([0], [0], color='black', lw=2, linestyle='solid', label='In Progress'),
            Line2D([0], [0], color='grey', lw=2, linestyle='solid', label='Planned'),
        ]

        legend1 = ax.legend(handles=format_legend_elements, loc='upper left', fontsize=10, title="Format Type")
        ax2 = ax.twinx()
        ax2.legend(handles=status_legend_elements, loc='upper right', fontsize=10, title="Development Status")
        ax2.axis('off')
        ax.set_xticks([])
        ax.set_yticks([])

        # Set the title directly on the axes
        ax.set_title("OMF-IO Format Interchange Overview", fontsize=16, pad=50)

        # Adjust layout with more space at the top
        plt.tight_layout(rect=[0, 0, 1, 0.95])

    def create_animation(self, animation_dict, output_file, framerate: float=1.0):
        """
        Create an animated GIF with optional subtitles for each step.

        Args:
            animation_dict (dict): Dictionary defining the animation steps and optional subtitles.
                                   Example: {'step1': {('from_omf', 'omf-io'): {'color': 'red', 'style': 'dashed'}, 'subtitle': 'Step 1'}}
            output_file (str): Path to save the animated GIF.
           framerate (int): Number of frames per second for the animation.
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        cumulative_highlights = {}  # To store all highlights cumulatively

        # Add a suptitle placeholder
        fig.suptitle("OMF-IO Format Interchange Overview", fontsize=16, y=0.98)

        def update(frame):
            ax.clear()
            for spine in ax.spines.values():
                spine.set_edgecolor('lightgrey')

            frame_data = animation_dict[frame]

            # Reset highlights if 'reset' is True
            if frame_data.get('reset', False):
                cumulative_highlights.clear()
            else:
                cumulative_highlights.update({k: v for k, v in frame_data.items() if k not in ['subtitle', 'reset']})

            self.plot_static(highlight_edges=cumulative_highlights, ax=ax)

            subtitle = frame_data.get('subtitle', '')
            ax.set_title(subtitle, fontsize=14, pad=20)
            ax.set_xticks([])
            ax.set_yticks([])
            plt.tight_layout()

        # Create the animation
        anim = FuncAnimation(
            fig, update, frames=list(animation_dict.keys()), interval=int(1000 / framerate), repeat=False
        )
        anim.save(output_file, writer='imagemagick')


if __name__ == '__main__':
    # Create an instance of the OMFIOPlot class
    omf_plot = OMFIOPlot(FORMATS)

    # Generate a static plot
    # Set a custom figure size
    omf_plot.plot_static()
    plt.savefig('omf-io-plot.png')

    # Create an animated GIF
    omf_plot.create_animation(ANIMATION_DICT, "omf_io_animation.gif", framerate=0.5)
