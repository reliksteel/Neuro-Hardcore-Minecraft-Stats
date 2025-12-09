import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Neuro Hardcore Minecraft Stats",
    page_icon="🎮",
    layout="wide"
)

# Title
st.markdown("<h1 style='text-align: center;'>Neuro Hardcore Minecraft Stats</h1>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load the stats.ods file"""
    data = pd.read_excel('stats.ods', engine='odf')
    return data

# Load and display data
try:
    df = load_data()
    
    # ==================== DAY FILTER ====================
    st.markdown("### Filter by Day")
    unique_days = sorted(df['Day'].unique())
    day_options = ['All Days'] + [f'Day {day}' for day in unique_days]
    selected_day_option = st.radio(
        "Select which day's data to display (affects all charts and metrics below):",
        day_options,
        horizontal=True,
        key="global_day_filter"
    )
    
    # Filter dataframe based on selection
    if selected_day_option == 'All Days':
        filtered_df = df
    else:
        day_num = int(selected_day_option.split(' ')[1])
        filtered_df = df[df['Day'] == day_num]
    
    st.markdown("---")
    
    # ==================== SUMMARY STATISTICS ====================
    # Calculate key metrics using filtered data
    total_time = filtered_df['Approximate Duration (Minutes)'].sum()
    avg_duration = filtered_df['Approximate Duration (Minutes)'].mean()
    
    # Get completion time from final entry
    final_run_duration = filtered_df.iloc[-1]['Approximate Duration (Minutes)']
    
    # Get most common cause of death
    most_common_death = filtered_df['Cause of Death'].value_counts().idxmax()
    most_common_death_count = filtered_df['Cause of Death'].value_counts().max()
    
    # Display metrics with custom HTML/CSS for centering and animation
    st.markdown(f"""
        <style>
        .metric-container {{
            display: flex;
            justify-content: space-around;
            align-items: stretch;
            gap: 20px;
            margin: 30px 0 50px 0;
        }}
        .metric-box {{
            flex: 1;
            text-align: center;
            padding: 20px;
            background: #1b1d22;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .metric-label {{
            font-size: 18px;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 10px;
        }}
        .metric-label-emoji {{
            font-size: 30px;
            margin-bottom: 5px;
        }}
        .metric-value {{
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin: 10px 0;
        }}
        .metric-delta {{
            font-size: 14px;
            color: #00C853;
            margin-top: 5px;
        }}
        .counter {{
            display: inline-block;
        }}
        </style>
        
        <div class="metric-container">
            <div class="metric-box">
                <div class="metric-label-emoji">⏱️</div>
                <div class="metric-label">Total Time Played</div>
                <div class="metric-value"><span class="counter" data-target="{int(total_time)}">{int(total_time):,}</span> min</div>
                <div class="metric-delta">↗ {total_time/60:.1f} hours</div>
            </div>
            <div class="metric-box">
                <div class="metric-label-emoji">📊</div>
                <div class="metric-label">Average Run Duration</div>
                <div class="metric-value"><span class="counter" data-target="{int(avg_duration)}">{int(avg_duration)}</span> min</div>
                <div class="metric-delta">↗ {len(filtered_df)} total runs</div>
            </div>
            <div class="metric-box">
                <div class="metric-label-emoji">🚀</div>
                <div class="metric-label">Completion Run Duration</div>
                <div class="metric-value"><span class="counter" data-target="{int(final_run_duration)}">{int(final_run_duration)}</span> min</div>
                <div class="metric-delta">↗ Run #{filtered_df.iloc[-1]['Run']}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label-emoji">💀</div>
                <div class="metric-label">Most Common Death</div>
                <div class="metric-value">{most_common_death}</div>
                <div class="metric-delta">↗ {most_common_death_count} deaths</div>
            </div>
        </div>
        
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const counters = document.querySelectorAll('.counter');
            const speed = 1000; // Animation duration in ms
            
            counters.forEach(counter => {{
                const target = parseInt(counter.getAttribute('data-target'));
                if (isNaN(target)) return;
                
                const increment = target / (speed / 16); // 60fps
                let current = 0;
                
                const updateCounter = () => {{
                    current += increment;
                    if (current < target) {{
                        counter.textContent = Math.floor(current).toLocaleString();
                        requestAnimationFrame(updateCounter);
                    }} else {{
                        counter.textContent = target.toLocaleString();
                    }}
                }};
                
                updateCounter();
            }});
        }});
        </script>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== DEATH STATISTICS CHART ====================
    st.subheader("Who Dies the Most?")
    
    # Prepare data for stacked bar chart using filtered data
    death_data = filtered_df.groupby(['Player Death', 'Cause of Death']).size().reset_index(name='Deaths')
    
    # Get players sorted by total deaths (for Y-axis ordering)
    player_totals = death_data.groupby('Player Death')['Deaths'].sum().sort_values(ascending=True)
    players = player_totals.index.tolist()
    
    # Create figure
    fig = go.Figure()
    
    # Get unique causes for color mapping
    all_causes = death_data['Cause of Death'].unique()
    colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', 
              '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f', '#e5c494', '#b3e2cd',
              '#fdcdac', '#cbd5e8', '#f4cae4']
    color_map = {cause: colors[i % len(colors)] for i, cause in enumerate(all_causes)}
    
    # For each player, sort their causes by death count (highest first) and add as traces
    for player in players:
        player_data = death_data[death_data['Player Death'] == player].sort_values('Deaths', ascending=False)
        
        # Add each cause as a segment in the bar
        for idx, row in player_data.iterrows():
            cause = row['Cause of Death']
            deaths = row['Deaths']
            
            # Check if this cause already has a trace (for legend grouping)
            existing_trace = any(trace.name == cause for trace in fig.data)
            
            fig.add_trace(go.Bar(
                name=cause,
                x=[deaths],
                y=[player],
                orientation='h',
                marker=dict(color=color_map[cause]),
                text=cause,
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(size=20),
                hovertemplate=f'<b>{player}</b><br>Cause: {cause}<br>Deaths: {deaths}<extra></extra>',
                showlegend=not existing_trace,  # Only show in legend once
                legendgroup=cause  # Group all instances of this cause
            ))
    
    # Update layout
    fig.update_layout(
        barmode='stack',
        height=500,
        title='Total Deaths per Player (with Causes of Death)',
        title_font=dict(size=16),
        xaxis_title="Number of Deaths",
        yaxis_title="Player",
        font=dict(size=16),
        xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title_font=dict(size=18), tickfont=dict(size=16)),
        showlegend=False,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")  # Visual divider

    # ==================== TOTAL TIME LOST BY PLAYER ====================
    st.subheader("Total Time Lost by Player")
    st.caption("Sum of all run durations where each player died")
    
    # Get players sorted by total time lost - use filtered data
    player_totals = filtered_df.groupby('Player Death')['Approximate Duration (Minutes)'].sum().sort_values(ascending=True)
    players = player_totals.index.tolist()
    
    # Create figure
    fig_time = go.Figure()
    
    # Color palette for runs
    colors = ['#e74c3c', '#c0392b', '#e67e22', '#d35400', '#f39c12', '#f1c40f', 
              '#16a085', '#1abc9c', '#3498db', '#2980b9', '#9b59b6', '#8e44ad',
              '#34495e', '#95a5a6', '#7f8c8d']
    
    # For each player, get their runs sorted by duration (longest first) and add as stacked segments
    for player in players:
        player_runs = filtered_df[filtered_df['Player Death'] == player].sort_values('Approximate Duration (Minutes)', ascending=False)
        
        # Add each run as a segment in the bar
        for idx, (_, row) in enumerate(player_runs.iterrows()):
            run_num = row['Run']
            duration = row['Approximate Duration (Minutes)']
            
            # Determine text to display based on segment size
            # Show both run number and duration if segment is large enough (>20 minutes)
            if duration >= 30:
                display_text = f"Run {run_num}<br>{duration} min"
            else:
                display_text = f"Run {run_num}"
            
            fig_time.add_trace(go.Bar(
                name=f"Run {run_num}",
                x=[duration],
                y=[player],
                orientation='h',
                marker=dict(color=colors[idx % len(colors)]),
                text=display_text,
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(size=11),
                hovertemplate=f'<b>{player}</b><br>Run {run_num}<br>Duration: {duration} minutes<extra></extra>',
                showlegend=False,  # Don't show legend since there are too many runs
                legendgroup=f"Run {run_num}"
            ))
    
    fig_time.update_layout(
        barmode='stack',
        height=500,
        xaxis_title="Total Minutes Lost",
        yaxis_title="",
        font=dict(size=16),
        xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title_font=dict(size=18), tickfont=dict(size=16)),
        showlegend=False,
        hovermode='closest',
        margin=dict(t=20, b=40, l=40, r=40)
    )
    
    st.plotly_chart(fig_time, use_container_width=True)
    
    st.markdown("---")  # Visual divider

    # ==================== VERTICAL RUN TIMELINE ====================
    st.subheader("Run Timeline")
    st.caption("All runs stacked vertically in chronological order")
    
    # Determine grouping based on filter
    if selected_day_option == 'All Days':
        # Group by day when showing all days
        unique_days_timeline = sorted(filtered_df['Day'].unique())
        x_labels = [f"Day {day}" for day in unique_days_timeline]
        group_by_day = True
    else:
        # Show single bar when filtered to one day
        x_labels = ["All Runs"]
        group_by_day = False
    
    # Create figure
    fig_timeline_vert = go.Figure()
    
    # Color palette for runs
    colors_timeline_v = ['#e74c3c', '#c0392b', '#e67e22', '#d35400', '#f39c12', '#f1c40f', 
                         '#16a085', '#1abc9c', '#3498db', '#2980b9', '#9b59b6', '#8e44ad',
                         '#34495e', '#95a5a6', '#7f8c8d']
    
    if group_by_day:
        # For each day, create a vertical stacked bar
        for day in unique_days_timeline:
            day_runs = filtered_df[filtered_df['Day'] == day].sort_values('Run')
            
            # Add each run as a segment in the vertical bar
            for idx, (_, row) in enumerate(day_runs.iterrows()):
                run_num = row['Run']
                duration = row['Approximate Duration (Minutes)']
                player = row['Player Death']
                
                # Determine text to display based on segment size
                if duration >= 30:
                    display_text = f"Run {run_num}"
                else:
                    display_text = f""
                
                fig_timeline_vert.add_trace(go.Bar(
                    name=f"Run {run_num}",
                    x=[f"Day {day}"],
                    y=[duration],
                    marker=dict(color=colors_timeline_v[idx % len(colors_timeline_v)]),
                    text=display_text,
                    textposition='inside',
                    insidetextanchor='middle',
                    textfont=dict(size=11),
                    hovertemplate=f'<b>Run {run_num}</b><br>Day {day}<br>Player: {player}<br>Duration: {duration} minutes<extra></extra>',
                    showlegend=False
                ))
    else:
        # Single bar with all filtered runs
        runs_sorted = filtered_df.sort_values('Run')
        for idx, (_, row) in enumerate(runs_sorted.iterrows()):
            run_num = row['Run']
            duration = row['Approximate Duration (Minutes)']
            player = row['Player Death']
            
            # Determine text to display based on segment size
            if duration >= 30:
                display_text = f"Run {run_num}"
            else:
                display_text = f""
        
            fig_timeline_vert.add_trace(go.Bar(
                name=f"Run {run_num}",
                x=["All Runs"],
                y=[duration],
                marker=dict(color=colors_timeline_v[idx % len(colors_timeline_v)]),
                text=display_text,
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(size=11),
                hovertemplate=f'<b>Run {run_num}</b><br>Player: {player}<br>Duration: {duration} minutes<extra></extra>',
                showlegend=False
            ))
    
    fig_timeline_vert.update_layout(
        barmode='stack',
        height=600,
        xaxis=dict(
            title="",
            title_font=dict(size=18), 
            tickfont=dict(size=14),
            side='top'  # Move x-axis to top
        ),
        yaxis=dict(
            title="Duration (Minutes)",
            title_font=dict(size=18), 
            tickfont=dict(size=14),
            autorange='reversed'  # Bars go top to bottom
        ),
        font=dict(size=16),
        showlegend=False,
        hovermode='closest',
        margin=dict(t=60, b=40, l=60, r=40)
    )
    
    st.plotly_chart(fig_timeline_vert, use_container_width=True)
    
    st.markdown("---")  # Visual divider

    # ==================== ACHIEVEMENT DURATION PREDICTION ====================
    st.subheader("Time to Reach Milestone Achievements")
    st.caption("Average run duration where milestone achievements were completed")
    
    # Get achievement columns in order - use filtered data
    achievement_cols_pred = [col for col in filtered_df.columns if col.startswith('Achievement:')]
    
    # Calculate average duration for each achievement (only for completed ones)
    achievement_durations = []
    achievement_names_completed = []
    for idx, ach in enumerate(achievement_cols_pred):
        runs_with_ach = filtered_df[filtered_df[ach] == True]
        ach_name = ach.replace('Achievement: ', '')
        if len(runs_with_ach) > 0:
            avg_duration = runs_with_ach['Approximate Duration (Minutes)'].mean()
            achievement_durations.append(avg_duration)
            achievement_names_completed.append(ach_name)
    
    if len(achievement_durations) >= 2:
        import numpy as np
        from sklearn.linear_model import LinearRegression
        
        # Prepare data for linear regression
        X = np.array(range(len(achievement_durations))).reshape(-1, 1)
        y = np.array(achievement_durations)
        
        # Fit linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict for all achievements (including unachieved ones)
        all_achievement_names = [col.replace('Achievement: ', '') for col in achievement_cols_pred]
        X_all = np.array(range(len(all_achievement_names))).reshape(-1, 1)
        predictions = model.predict(X_all)
        
        # Create visualization
        fig_pred = go.Figure()
        
        # Add actual data points
        fig_pred.add_trace(go.Scatter(
            x=list(range(len(achievement_durations))),
            y=achievement_durations,
            mode='markers',
            name='Actual Average Duration',
            marker=dict(size=12, color='#4CAF50'),
            hovertemplate='<b>%{text}</b><br>Average Duration: %{y:.1f} minutes<extra></extra>',
            text=achievement_names_completed
        ))
        
        # Add single continuous trend line through all achievements
        fig_pred.add_trace(go.Scatter(
            x=list(range(len(predictions))),
            y=predictions,
            mode='lines',
            name='Trend Line',
            line=dict(color='#2196F3', width=2, dash='dash'),
            hoverinfo='skip'
        ))
        
        # Add predictions for unachieved achievements
        if len(predictions) > len(achievement_durations):
            fig_pred.add_trace(go.Scatter(
                x=list(range(len(achievement_durations), len(predictions))),
                y=predictions[len(achievement_durations):],
                mode='markers',
                name='Predicted Duration',
                marker=dict(size=12, color='#FF9800', symbol='diamond'),
                hovertemplate='<b>%{text}</b><br>Predicted Duration: %{y:.1f} minutes<extra></extra>',
                text=all_achievement_names[len(achievement_durations):]
            ))
        
        fig_pred.update_layout(
            height=400,
            xaxis_title="Achievement Progression",
            yaxis_title="Average Duration (Minutes)",
            font=dict(size=14),
            xaxis=dict(
                title_font=dict(size=16),
                tickfont=dict(size=12),
                tickmode='array',
                tickvals=list(range(len(all_achievement_names))),
                ticktext=all_achievement_names,
                tickangle=-45
            ),
            yaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
            hovermode='closest',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=20, b=120, l=60, r=40)
        )
        
        st.plotly_chart(fig_pred, use_container_width=True)
        
        # Show prediction details
        st.caption(f"Linear regression model (R² = {model.score(X, y):.3f})")
    else:
        st.info("Need at least 2 completed achievements to generate predictions.")
    
    st.markdown("---")  # Visual divider

    # ==================== ACHIEVEMENT COMPLETION RATE PIE CHART ====================
    st.subheader("Milestone Achievement Completion Rates")
    st.caption("Percentage of runs that reached each achievement milestone. Achievements marked with asterisk have not been completed in any run yet.")
    
    # Get achievement columns - use filtered data
    achievement_cols = [col for col in filtered_df.columns if col.startswith('Achievement:')]
    total_runs = len(filtered_df)
    
    # Calculate completion rates for each achievement
    pie_data = []
    for idx, ach in enumerate(achievement_cols):
        runs_with_ach = filtered_df[filtered_df[ach] == True]
        ach_name = ach.replace('Achievement: ', '')
        count = len(runs_with_ach)
        percentage = (count / total_runs) * 100
        
        # Mark achievements that haven't been completed yet
        if count == 0:
            label = f"{ach_name} *"
        else:
            label = ach_name
        
        pie_data.append({
            'Achievement': label,
            'Count': count,
            'Percentage': percentage,
            'Has Data': count > 0,
            'Order': idx  # Track achievement order
        })
    
    # Add "No Milestones" category - runs that didn't get any milestone achievements
    runs_with_no_achievements = filtered_df[~filtered_df[achievement_cols].any(axis=1)]
    no_ach_count = len(runs_with_no_achievements)
    no_ach_percentage = (no_ach_count / total_runs) * 100
    
    pie_data.append({
        'Achievement': 'No Milestone Achievements',
        'Count': no_ach_count,
        'Percentage': no_ach_percentage,
        'Has Data': True,
        'Order': -1  # Put at beginning
    })
    
    # Create DataFrame
    pie_df = pd.DataFrame(pie_data)
    
    # Create pie chart
    fig_pie = go.Figure()
    
    # Progressive monochrome color palette - lighter to darker
    # Early achievements (common) = lighter, later achievements (rare) = darker
    achievement_colors = [
        '#B2DFDB',  # No Milestone Achievements - light teal
        '#80CBC4',  # Acquire Hardware - light green-teal
        '#4DB6AC',  # We Need to Go Deeper - medium green-teal
        '#26A69A',  # A Terrible Fortress - darker green-teal
        '#00897B',  # Into Fire - deep green-teal
        '#00695C',  # Eye Spy - very dark green-teal
        '#004D40',  # The End? - darkest green-teal (not achieved)
        '#00251A'   # Free the end - extremely dark green-teal (not achieved)
    ]
    
    # Assign colors based on order
    colors = []
    for _, row in pie_df.iterrows():
        order = row['Order']
        if order == -1:
            colors.append(achievement_colors[0])  # No Achievements
        else:
            colors.append(achievement_colors[order + 1])
    
    fig_pie.add_trace(go.Pie(
        labels=pie_df['Achievement'],
        values=pie_df['Count'],
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(size=14),
        hovertemplate='<b>%{label}</b><br>Runs: %{value}<br>Percentage: %{percent}<extra></extra>'
    ))
    
    fig_pie.update_layout(
        height=500,
        font=dict(size=14),
        showlegend=False,
        margin=dict(t=20, b=40, l=40, r=40)
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")  # Visual divider


    # ==================== DAY-BY-DAY TRENDS ====================
    st.subheader("Performance Trends Across Days")
    st.caption("Track how key metrics evolved over each streaming day")
    
    # Only show this if "All Days" is selected
    if selected_day_option == 'All Days':
        # Calculate metrics for each day
        unique_days_trend = sorted(df['Day'].unique())
        day_trend_data = []
        
        achievement_cols_trend = [col for col in df.columns if col.startswith('Achievement:')]
        
        for day in unique_days_trend:
            day_df = df[df['Day'] == day]
            
            # Average run duration
            avg_run_duration = day_df['Approximate Duration (Minutes)'].mean()
            
            # Longest run duration
            max_run_duration = day_df['Approximate Duration (Minutes)'].max()
            
            # Average achievements per run
            avg_achievements = day_df[achievement_cols_trend].sum(axis=1).mean()
            
            # Furthest achievement reached (count of unique achievements completed)
            furthest_achievement_idx = -1
            for idx, ach in enumerate(achievement_cols_trend):
                if day_df[ach].any():
                    furthest_achievement_idx = idx
            
            day_trend_data.append({
                'Day': day,
                'Avg Duration': avg_run_duration,
                'Max Duration': max_run_duration,
                'Avg Milestone Achievements': avg_achievements,
                'Furthest Milestone Achievement': furthest_achievement_idx + 1
            })
        
        trend_df = pd.DataFrame(day_trend_data)
        
        # Create side-by-side charts using columns
        col1, col2 = st.columns(2)
        
        # LEFT CHART: Max/Peak Performance
        with col1:
            fig_max = go.Figure()
            
            # Max Duration
            fig_max.add_trace(go.Scatter(
                x=trend_df['Day'],
                y=trend_df['Max Duration'],
                mode='lines+markers',
                name='Longest Run Duration',
                line=dict(color='#4CAF50', width=3),
                marker=dict(size=10)
            ))
            
            # Furthest Achievement
            fig_max.add_trace(go.Scatter(
                x=trend_df['Day'],
                y=trend_df['Furthest Milestone Achievement'],
                mode='lines+markers',
                name='Furthest Milestone Achievement Reached',
                line=dict(color='#FF9800', width=3),
                marker=dict(size=10),
                yaxis='y2'
            ))
            
            fig_max.update_layout(
                title='Peak Performance by Day',
                title_font=dict(size=16),
                height=450,
                xaxis=dict(
                    title='Day',
                    tickmode='array',
                    tickvals=unique_days_trend,
                    ticktext=[f'Day {d}' for d in unique_days_trend],
                    title_font=dict(size=14),
                    tickfont=dict(size=12)
                ),
                yaxis=dict(
                    title='Duration (Minutes)',
                    title_font=dict(color='#4CAF50', size=14),
                    tickfont=dict(color='#4CAF50', size=11)
                ),
                yaxis2=dict(
                    title='Milestone Achievements',
                    title_font=dict(color='#FF9800', size=14),
                    tickfont=dict(color='#FF9800', size=11),
                    overlaying='y',
                    side='right'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(size=10)
                ),
                hovermode='x unified',
                margin=dict(t=60, b=60, l=60, r=60)
            )
            
            st.plotly_chart(fig_max, use_container_width=True)
        
        # RIGHT CHART: Average Performance
        with col2:
            fig_avg = go.Figure()
            
            # Average Duration
            fig_avg.add_trace(go.Scatter(
                x=trend_df['Day'],
                y=trend_df['Avg Duration'],
                mode='lines+markers',
                name='Average Run Duration',
                line=dict(color='#4CAF50', width=3),
                marker=dict(size=10)
            ))
            
            # Average Achievements
            fig_avg.add_trace(go.Scatter(
                x=trend_df['Day'],
                y=trend_df['Avg Milestone Achievements'],
                mode='lines+markers',
                name='Avg Milestone Achievements per Run',
                line=dict(color='#FF9800', width=3),
                marker=dict(size=10),
                yaxis='y2'
            ))
            
            fig_avg.update_layout(
                title='Average Performance by Day',
                title_font=dict(size=16),
                height=450,
                xaxis=dict(
                    title='Day',
                    tickmode='array',
                    tickvals=unique_days_trend,
                    ticktext=[f'Day {d}' for d in unique_days_trend],
                    title_font=dict(size=14),
                    tickfont=dict(size=12)
                ),
                yaxis=dict(
                    title='Duration (Minutes)',
                    title_font=dict(color='#4CAF50', size=14),
                    tickfont=dict(color='#4CAF50', size=11)
                ),
                yaxis2=dict(
                    title='Milestone Achievements',
                    title_font=dict(color='#FF9800', size=14),
                    tickfont=dict(color='#FF9800', size=11),
                    overlaying='y',
                    side='right'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(size=10)
                ),
                hovermode='x unified',
                margin=dict(t=60, b=60, l=60, r=60)
            )
            
            st.plotly_chart(fig_avg, use_container_width=True)
    else:
        st.info("📊 Select 'All Days' to see performance trends across days")
    
    st.markdown("---")  # Visual divider

    # ==================== FULL DATA TABLE ====================
    st.subheader("Run Data")
    
    # Create a copy of the filtered dataframe for display
    display_df = filtered_df.copy()
    
    # Separate basic stats and achievements
    basic_cols = ['Run', 'Day', 'Approximate Duration (Minutes)', 'Player Death', 'Cause of Death']
    achievement_cols_table = [col for col in display_df.columns if col.startswith('Achievement:')]
    
    # Rename achievement columns to remove "Achievement: " prefix
    rename_dict = {col: col.replace('Achievement: ', '' if display_df[col].any() else '') for col in achievement_cols_table}
    display_df = display_df.rename(columns=rename_dict)
    
    # Reorder columns: basic stats first, then achievements
    new_achievement_names = [rename_dict[col] for col in achievement_cols_table]
    display_df = display_df[basic_cols + new_achievement_names]
    
    # Configure column display
    column_config = {}
    
    # Style achievement columns with custom configuration
    for old_col, new_col in rename_dict.items():
        column_config[new_col] = st.column_config.CheckboxColumn(
            new_col,
            help=f"Achievement: {old_col.replace('Achievement: ', '')}",
            default=False,
        )
      
    # Use st.data_editor instead of st.dataframe to avoid internal scrolling
    st.data_editor(
        display_df,
        width="stretch",
        height="content",
        use_container_width=True,
        column_config=column_config,
        hide_index=True,
        disabled=True,
        num_rows="fixed"
    )
    
    # Show summary stats
    st.caption(f"Total Runs: {len(filtered_df)} | Total Players: {filtered_df['Player Death'].nunique()}")
    
except FileNotFoundError:
    st.error("Could not find 'stats.ods'. Please make sure the file is in the same directory as app.py")
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
