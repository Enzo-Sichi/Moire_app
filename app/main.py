from utils.vector_utils import *
from utils.visualization_utils import *
from utils.pattern_utils import *

def main():
    st.title("Grid Pattern and Frequency Domain Simulator")
    
    with st.sidebar:
        pattern_types = ["2 Vertical Grids", "3 Vertical Grids", "4 Vertical Grids",
                        "2 Dot Grids", "3 Dot Grids"]
        pattern_type = st.selectbox("Select Pattern Type", pattern_types)
        
        num_patterns = int(pattern_type[0])
        
        frequencies = []
        angles = []
        for i in range(num_patterns):
            freq = st.slider(f"Frequency {i+1}", 1.0, 40.0, 20.0, 0.1)
            angle = st.slider(f"Angle {i+1} (degrees)", 0.0, 360.0, i * (180/num_patterns), 1.0)
            frequencies.append(freq)
            angles.append(angle)
        
        visibility_radius = st.slider("Visibility Disk Radius", 1.0, 200.0, 100.0, 1.0)
        window_half_size = st.slider("Frequency range", 5.0, 200.0, 100.0, 5.0)
        
        view_option = st.radio("View Option",
                              ["Both", "Pattern Only", "Frequency Domain Only"])
    
    if view_option in ["Both", "Pattern Only"]:
        st.subheader("Pattern Visualization")
        pattern_size = 400
        combined_pattern = np.ones((pattern_size, pattern_size))
        for freq, angle in zip(frequencies, angles):
            combined_pattern *= create_pattern(pattern_size, freq, angle, pattern_type)

        pattern_fig = go.Figure(data=go.Heatmap(
            z=1 - combined_pattern,
            colorscale='Greys'
        ))
        pattern_fig.update_layout(
            width=None, height=600,
            xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(showticklabels=False, showgrid=False),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(pattern_fig, use_container_width=True)
    
    if view_option in ["Both", "Frequency Domain Only"]:
        st.subheader("Frequency Domain Visualization")  
        base_vectors = create_frequency_vectors(pattern_type, frequencies, angles)
        all_vectors = create_all_vectors(base_vectors, 4)
        freq_fig = frequency_domain_visualization(all_vectors, visibility_radius)
        
        freq_fig.update_xaxes(range=[-window_half_size, window_half_size])
        freq_fig.update_yaxes(range=[-window_half_size, window_half_size])
        freq_fig.update_layout(
            width=None, height=600,
            xaxis=dict(zeroline=True, zerolinewidth=1, zerolinecolor='black'),
            yaxis=dict(zeroline=True, zerolinewidth=1, zerolinecolor='black', scaleanchor="x", scaleratio=1),
            showlegend= False,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(freq_fig, use_container_width=True)

if __name__ == "__main__":
    main()