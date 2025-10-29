import plotly.graph_objects as go
import plotly.express as px

# Create a professional flowchart using plotly for the sentiment analysis workflow
fig = go.Figure()

# Define node positions and labels with proper workflow structure
nodes = [
    {"x": 0.5, "y": 0.95, "text": "User Input<br>Stock Symbol", "type": "input", "width": 0.12, "height": 0.06},
    {"x": 0.5, "y": 0.85, "text": "Data Collection", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.5, "y": 0.75, "text": "Yahoo Finance<br>API", "type": "decision", "width": 0.12, "height": 0.06},
    {"x": 0.25, "y": 0.65, "text": "Stock Data<br>Retrieval", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.75, "y": 0.65, "text": "News Data<br>Retrieval", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.5, "y": 0.55, "text": "Data Processing", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.25, "y": 0.45, "text": "Stock Metrics<br>Calculation", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.75, "y": 0.45, "text": "News Text<br>Preprocessing", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.75, "y": 0.35, "text": "TextBlob NLP<br>Processing", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.5, "y": 0.25, "text": "Sentiment<br>Analysis", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.5, "y": 0.15, "text": "Visualization<br>Generation", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.25, "y": 0.05, "text": "Charts &<br>Gauges", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.75, "y": 0.05, "text": "Data<br>Tables", "type": "process", "width": 0.12, "height": 0.06},
    {"x": 0.5, "y": -0.05, "text": "Streamlit<br>Dashboard", "type": "output", "width": 0.12, "height": 0.06}
]

# Define colors for different node types
colors = {
    "input": "#1FB8CD",
    "process": "#2E8B57", 
    "decision": "#DB4545",
    "output": "#5D878F"
}

# Add shapes for each node
for i, node in enumerate(nodes):
    if node["type"] == "decision":
        # Create diamond shape for decision nodes
        x_center, y_center = node["x"], node["y"]
        diamond_size = 0.06
        fig.add_shape(
            type="path",
            path=f"M {x_center},{y_center+diamond_size} L {x_center+diamond_size},{y_center} L {x_center},{y_center-diamond_size} L {x_center-diamond_size},{y_center} Z",
            fillcolor=colors[node["type"]],
            line=dict(color="#13343B", width=2)
        )
    else:
        # Rectangle for all other nodes
        fig.add_shape(
            type="rect",
            x0=node["x"]-node["width"]/2, y0=node["y"]-node["height"]/2,
            x1=node["x"]+node["width"]/2, y1=node["y"]+node["height"]/2,
            fillcolor=colors[node["type"]],
            line=dict(color="#13343B", width=2),
            layer="below"
        )

# Add text labels for each node
for node in nodes:
    fig.add_annotation(
        x=node["x"], y=node["y"],
        text=node["text"],
        showarrow=False,
        font=dict(size=11, color="white", family="Arial Black"),
        xanchor="center",
        yanchor="middle"
    )

# Define arrows between nodes
arrows = [
    (0, 1),   # User Input -> Data Collection
    (1, 2),   # Data Collection -> Yahoo Finance API
    (2, 3),   # Yahoo Finance API -> Stock Data
    (2, 4),   # Yahoo Finance API -> News Data
    (3, 5),   # Stock Data -> Data Processing
    (4, 5),   # News Data -> Data Processing
    (5, 6),   # Data Processing -> Stock Metrics
    (5, 7),   # Data Processing -> News Text Preprocessing
    (7, 8),   # News Text Preprocessing -> TextBlob NLP
    (6, 9),   # Stock Metrics -> Sentiment Analysis
    (8, 9),   # TextBlob NLP -> Sentiment Analysis
    (9, 10),  # Sentiment Analysis -> Visualization
    (10, 11), # Visualization -> Charts & Gauges
    (10, 12), # Visualization -> Data Tables
    (11, 13), # Charts & Gauges -> Streamlit Dashboard
    (12, 13)  # Data Tables -> Streamlit Dashboard
]

# Add arrows
for start_idx, end_idx in arrows:
    start_node = nodes[start_idx]
    end_node = nodes[end_idx]
    
    # Calculate arrow positions
    start_x, start_y = start_node["x"], start_node["y"]
    end_x, end_y = end_node["x"], end_node["y"]
    
    # Adjust start and end points to node boundaries
    if start_y > end_y:  # Arrow going down
        start_y -= start_node["height"]/2
        end_y += end_node["height"]/2
    elif start_y < end_y:  # Arrow going up
        start_y += start_node["height"]/2
        end_y -= end_node["height"]/2
    
    if start_x != end_x:  # Horizontal component
        if start_x > end_x:  # Arrow going left
            start_x -= start_node["width"]/2
            end_x += end_node["width"]/2
        else:  # Arrow going right
            start_x += start_node["width"]/2
            end_x -= end_node["width"]/2
    
    fig.add_annotation(
        x=end_x, y=end_y,
        ax=start_x, ay=start_y,
        xref="x", yref="y",
        axref="x", ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2.5,
        arrowcolor="#13343B"
    )

# Update layout
fig.update_layout(
    title="Stock Sentiment Analysis Workflow",
    xaxis=dict(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False, visible=False),
    yaxis=dict(range=[-0.1, 1], showgrid=False, showticklabels=False, zeroline=False, visible=False),
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# Save the chart as both PNG and SVG
fig.write_image('sentiment_workflow.png')
fig.write_image('sentiment_workflow.svg', format='svg')

print("Professional flowchart created successfully!")
print("Chart saved as sentiment_workflow.png and sentiment_workflow.svg")