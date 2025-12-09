import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# Set page config
st.set_page_config(
    page_title="Neuro Hardcore Minecraft Stats",
    page_icon="🐉",
    layout="wide"
)

# Title
st.markdown("<h1 style='text-align: center;'>Neuro Hardcore Minecraft Stats</h1>", unsafe_allow_html=True)

# ==================== DATA LOADING & CLEANING ====================

def load_data():
    # raw_csv updated with Run #87 (Ender Dragon)
    raw_csv = """Day,Run ,Dead,Time Of Death (UTC),Cause Of Death,Notes,Run Length,Avg Run Length,Avg Run Length (per day),Neuro Deaths,Filian Deaths,Crelly Deaths,Vedal Deaths,Most Deaths,graphs
1,reset #1,neuro,19:25,creeper,,10 minutes,10 minutes,10 minutes,1,0,0,0,Neuro,
1,reset #2,neuro,19:29,creeper,,4 minutes,7 minutes,7 minutes,2,0,0,0,Neuro,
1,reset #3,neuro,20:02,spider,,33 minutes,16 minutes,16 minutes,3,0,0,0,Neuro,
1,death #1,filian,20:03,falling,,-,16 minutes,16 minutes,3,1,0,0,Neuro,
1,reset #4,filian,20:12,falling,,9 minutes,14 minutes,14 minutes,3,2,0,0,Neuro,
1,reset #5,filian,20:20,drowned w/ trident,,8 minutes,13 minutes,13 minutes,3,3,0,0,Neuro,
1,reset #6,vedal,20:33,creeper,,13 minutes,13 minutes,13 minutes,3,3,0,1,Neuro,
1,reset #7,vedal,20:52,enderman,,19 minutes,14 minutes,14 minutes,3,3,0,2,Neuro,
1,reset #8,crelly,21:04,zombie,,12 minutes,14 minutes,14 minutes,3,3,1,2,Neuro,
1,reset #9,filian/neuro,21:16,creeper ,(double kill),12 minutes,13 minutes,13 minutes,4,4,1,2,Neuro,
1,reset #10,crelly,22:08,PvP,Neuro killed,52 minutes,17 minutes,17 minutes,4,4,2,2,Neuro,
1,reset #11,neuro,22:20,falling,,12 minutes,17 minutes,17 minutes,5,4,2,2,Neuro,
1,reset #12,vedal,22:41,creeper,,21 minutes,17 minutes,17 minutes,5,4,2,3,Neuro,
1,reset #13,neuro,22:54,starved,,13 minutes,17 minutes,17 minutes,6,4,2,3,Neuro,
1,reset #14,filian, 0:37,piglin,,103 minutes,23 minutes,23 minutes,6,5,2,3,Neuro,
1,reset #15,filian, 1:02,iron golem,,26 minutes,23 minutes,23 minutes,6,6,2,3,Neuro,
1,reset #16,neuro, 2:09,zombie piglin,,67 minutes,26 minutes,26 minutes,7,6,2,3,Neuro,
1,reset #17,vedal, 2:21,skeleton,,12 minutes,25 minutes,25 minutes,7,6,2,4,Neuro,
1,reset #18,neuro, 2:41,skeleton,,19 minutes,25 minutes,25 minutes,8,6,2,4,Neuro,
1,reset #19,neuro, 2:43,drowning,,2 minutes,24 minutes,24 minutes,9,6,2,4,Neuro,
1,reset #20,vedal, 3:27,iron golem,,44 minutes,25 minutes,25 minutes,9,6,2,5,Neuro,
1,reset #21,neuro, 3:39,drowning,,12 minutes,24 minutes,24 minutes,10,6,2,5,Neuro,
1,reset #22,neuro, 3:47,drowning,sang so hard she drowned o7,8 minutes,23 minutes,23 minutes,11,6,2,5,Neuro,
1,reset #23,crelly, 3:54,PvP,NEURO PVP 2 ELECTRIC BOOGALOO,7 minutes,23 minutes,23 minutes,11,6,3,5,Neuro,
1,reset #24,crelly, 4:43,falling,,49 minutes,24 minutes,24 minutes,11,6,4,5,Neuro,
1,reset #25,crelly, 5:02,PvP,NEURO PVP - PART 3,18 minutes,23 minutes,23 minutes,11,6,5,5,Neuro,
1,reset #26,neuro, 5:22,zombie,went down fighting against so many mobs... ,20 minutes,23 minutes,23 minutes,12,6,5,5,Neuro,
1,reset #27,neuro, 5:39,skeleton,,17 minutes,23 minutes,23 minutes,13,6,5,5,Neuro,
1,reset #28,filian, 5:44,PvP,NEURO PVP FILIAN EDITION,5 minutes,22 minutes,22 minutes,13,7,5,5,Neuro,
1,reset #29,filian, 6:35,witch,,51 minutes,23 minutes,23 minutes,13,8,5,5,Neuro,
1,reset #30,filian, 6:44,PvP,Vedal vs Filian Duel,9 minutes,23 minutes,23 minutes,13,9,5,5,Neuro,
1,reset #31,neuro, 6:56,drowning,,12 minutes,23 minutes,23 minutes,14,9,5,5,Neuro,
1,reset #32,vedal, 7:04,creeper,,8 minutes,22 minutes,22 minutes,14,9,5,6,Neuro,
1,reset #33,neuro, 7:20,drowned w/ trident,,17 minutes,22 minutes,22 minutes,15,9,5,6,Neuro,
2,reset #34,neuro,18:14,falling,in nether,69 minutes,23 minutes,69 minutes,16,9,5,6,Neuro,
2,reset #35,neuro,18:32,creeper,,18 minutes,23 minutes,44 minutes,17,9,5,6,Neuro,
2,reset #36,neuro,18:46,skeleton,,14 minutes,23 minutes,34 minutes,18,9,5,6,Neuro,
2,reset #37,neuro,19:01,creeper,,15 minutes,23 minutes,29 minutes,19,9,5,6,Neuro,
2,reset #38,neuro,20:13,falling,in nether,73 minutes,24 minutes,38 minutes,20,9,5,6,Neuro,
2,death #2,filian,20:13,falling,in nether,-,24 minutes,38 minutes,20,10,5,6,Neuro,
2,reset #39,filian,20:16,lava,intentional reset cuz same seed,2 minutes,23 minutes,32 minutes,20,11,5,6,Neuro,
2,reset #40,vedal,20:57,creeper,insane god run,41 minutes,24 minutes,33 minutes,20,11,5,7,Neuro,
2,reset #41,neuro,21:31,zombie,,34 minutes,24 minutes,33 minutes,21,11,5,7,Neuro,
2,reset #42,neuro,21:48,drowning,underwater cave,17 minutes,24 minutes,31 minutes,22,11,5,7,Neuro,
2,reset #43,filian,22:07,zombie,,19 minutes,24 minutes,30 minutes,22,12,5,7,Neuro,
2,reset #44,neuro,22:09,drowning,,2 minutes,23 minutes,28 minutes,23,12,5,7,Neuro,
2,reset #45,neuro,22:16,drowning,,7 minutes,23 minutes,26 minutes,24,12,5,7,Neuro,
2,reset #46,vedal,22:22,iron golem,,6 minutes,23 minutes,24 minutes,24,12,5,8,Neuro,
2,reset #47,neuro,22:36,zombie,,14 minutes,22 minutes,24 minutes,25,12,5,8,Neuro,
2,death #3,filian,22:36,lava,,-,22 minutes,24 minutes,25,13,5,8,Neuro,
2,reset #48,neuro,23:00,zombie,,23 minutes,23 minutes,24 minutes,26,13,5,8,Neuro,
2,death #4,vedal,23:00,lava,,-,23 minutes,24 minutes,26,13,5,9,Neuro,
2,reset #49,neuro,23:54,lava,,54 minutes,23 minutes,26 minutes,27,13,5,9,Neuro,
2,reset #50,filian,23:57,zombie,,3 minutes,23 minutes,24 minutes,27,14,5,9,Neuro,
2,death #5,neuro,23:57,zombie,,-,23 minutes,24 minutes,28,14,5,9,Neuro,
2,death #6,crelly,23:57,creeper,,-,23 minutes,24 minutes,28,14,6,9,Neuro,
2,reset #51,vedal, 2:05,creeper,o7 such a good run,128 minutes,25 minutes,30 minutes,28,14,6,10,Neuro,
2,reset #52,crelly, 2:19,husk,,14 minutes,25 minutes,29 minutes,28,14,7,10,Neuro,
2,reset #53,neuro, 2:30,zombie,,11 minutes,24 minutes,28 minutes,29,14,7,10,Neuro,
2,death #7,vedal, 2:30,falling,,-,24 minutes,28 minutes,29,14,7,11,Neuro,
2,death #8,filian, 2:30,falling,,-,24 minutes,28 minutes,29,15,7,11,Neuro,
2,reset #54,neuro, 2:40,skeleton,,10 minutes,24 minutes,27 minutes,30,15,7,11,Neuro,
2,reset #55,neuro, 2:56,falling,,17 minutes,24 minutes,27 minutes,31,15,7,11,Neuro,
2,reset #56,crelly, 3:13,creeper,,17 minutes,24 minutes,26 minutes,31,15,8,11,Neuro,
2,reset #57,neuro, 3:37,zombie,,24 minutes,24 minutes,26 minutes,32,15,8,11,Neuro,
2,reset #58,neuro, 3:47,zombie,,10 minutes,24 minutes,26 minutes,33,15,8,11,Neuro,
2,death #9,vedal, 3:47,void,jumped off lobby AINTNEURWAY,-,24 minutes,26 minutes,33,15,8,12,Neuro,
2,reset #59,vedal, 3:53,falling,smh missed a jump,5 minutes,23 minutes,25 minutes,33,15,8,13,Neuro,
2,reset #60,neuro, 4:08,skeleton,,15 minutes,23 minutes,25 minutes,34,15,8,13,Neuro,
2,reset #61,vedal, 4:42,zombie,,35 minutes,23 minutes,25 minutes,34,15,8,14,Neuro,
2,reset #62,filian, 4:55,zombie,,13 minutes,23 minutes,25 minutes,34,16,8,14,Neuro,
2,death #10,crelly, 4:55,creeper,,-,23 minutes,25 minutes,34,16,9,14,Neuro,
2,reset #63,vedal, 5:02,skeleton,,7 minutes,23 minutes,24 minutes,34,16,9,15,Neuro,
2,reset #64,neuro, 6:34,iron golem,blaze rods obtained,92 minutes,24 minutes,26 minutes,35,16,9,15,Neuro,
2,reset #65,neuro, 6:37,zombie,,3 minutes,24 minutes,25 minutes,36,16,9,15,Neuro,
2,reset #66,neuro,10:21,guardian,STICKS STICKS STICKS,223 minutes,27 minutes,31 minutes,37,16,9,15,Neuro,
3,reset #ew,neuro,20:12,skeleton,glad we lost this one,11 minutes,26 minutes,11 minutes,38,16,9,15,Neuro,
3,reset #68,neuro,20:26,skeleton,,14 minutes,26 minutes,30 minutes,39,16,9,15,Neuro,
3,reset #69,crelly,20:42,zombie,,16 minutes,26 minutes,30 minutes,39,16,10,15,Neuro,
3,reset #70,neuro,20:45,drowning,that doesnt sound good- neuro_sama drowned,2 minutes,26 minutes,29 minutes,40,16,10,15,Neuro,
3,reset #71,neuro,20:51,falling,so dont throw this- neuro_sama fell from a high place,6 minutes,25 minutes,29 minutes,41,16,10,15,Neuro,
3,reset #72,filian,22:24,falling,another stick run,93 minutes,26 minutes,30 minutes,41,17,10,15,Neuro,
3,reset #73,neuro,22:37,zombie,early failed stick run,13 minutes,26 minutes,30 minutes,42,17,10,15,Neuro,
3,reset #74,neuro,23:03,enderman,,26 minutes,26 minutes,30 minutes,43,17,10,15,Neuro,
3,reset #75,neuro, 0:17,lava,o7,74 minutes,27 minutes,31 minutes,44,17,10,15,Neuro,
3,reset #76,neuro, 0:36,zombie,,20 minutes,27 minutes,30 minutes,45,17,10,15,Neuro,
3,reset #77,crelly, 0:43,lava,mild neuro sabotage,7 minutes,27 minutes,30 minutes,45,17,11,15,Neuro,
3,reset #78,neuro, 0:49,suffocation,s a n d,6 minutes,26 minutes,26 minutes,46,17,11,15,Neuro,
3,reset #79,filian, 1:23,skeleton,,34 minutes,26 minutes,26 minutes,46,18,11,15,Neuro,
3,reset #80,neuro, 4:56,zombie,THE ACTUAL GOD RUN,213 minutes,29 minutes,29 minutes,47,18,11,15,Neuro,
3,death #11,crelly, 4:56,zombie,protecting neuro o7,-,29 minutes,29 minutes,47,18,12,15,Neuro,
3,reset #81,crelly, 5:11,zombie,,15 minutes,29 minutes,29 minutes,47,18,13,15,Neuro,
3,death #12,neuro, 5:11,zombie,,-,29 minutes,29 minutes,48,18,13,15,Neuro,
3,death #13,vedal, 5:11,void,,-,29 minutes,29 minutes,48,18,13,16,Neuro,
3,reset #82,neuro, 7:00,falling,walked off blaze spawner,110 minutes,30 minutes,30 minutes,49,18,13,16,Neuro,
3,reset #83,vedal, 7:11,skeleton,,11 minutes,29 minutes,29 minutes,49,18,13,17,Neuro,
4,reset #84,filian,17:30,falling,,20 minutes,29 minutes,20 minutes,49,19,13,17,Neuro,
4,reset #85,crelly,18:26,PvP,NEURO MURDER AUTHORIZED BY VEDAL,56 minutes,29 minutes,38 minutes,49,19,14,17,Neuro,
4,reset #86,neuro,18:31,wolf,,6 minutes,29 minutes,27 minutes,50,19,14,17,Neuro,
4,reset #87,ender dragon, 1:51,vedal and filian,,319 minutes,33 minutes,100 minutes,50,19,14,17,Neuro,"""
    
    # Read the embedded CSV data
    data = pd.read_csv(io.StringIO(raw_csv))
    
    # 1. Clean Duration: Convert "10 minutes" -> 10.0
    data['Run Length'] = data['Run Length'].astype(str).str.replace(' minutes', '').replace('-', '0')
    data['Approximate Duration (Minutes)'] = pd.to_numeric(data['Run Length'], errors='coerce').fillna(0)
    
    # 2. Extract Run ID
    data['Run'] = data['Run '].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)
    
    # 3. Standardize Names (Capitalize)
    # Note: "ender dragon" in csv becomes "Ender dragon"
    data['Player Death'] = data['Dead'].astype(str).str.strip().str.capitalize()
    
    # 4. Standardize Causes
    data['Cause of Death'] = data['Cause Of Death'].astype(str).str.strip()
    
    return data

df = load_data()

# ==================== APP LAYOUT ====================

if not df.empty:
    try:
        # Check if the Dragon has been defeated
        dragon_defeated = "Ender dragon" in df['Player Death'].values
        
        if dragon_defeated:
            st.balloons()
            st.success("🏆 VICTORY ACHIEVED! The Ender Dragon has been defeated!")
            
        # Filter Logic
        st.markdown("### Filter by Day")
        unique_days = sorted(df['Day'].unique())
        day_options = ['All Days'] + [f'Day {day}' for day in unique_days]
        selected_day_option = st.radio(
            "Select which day's data to display:",
            day_options,
            horizontal=True,
            key="global_day_filter"
        )
        
        if selected_day_option == 'All Days':
            filtered_df = df
        else:
            day_num = int(selected_day_option.split(' ')[1])
            filtered_df = df[df['Day'] == day_num]
        
        st.markdown("---")
        
        # ==================== METRICS ====================
        total_time = filtered_df['Approximate Duration (Minutes)'].sum()
        valid_runs = filtered_df[filtered_df['Approximate Duration (Minutes)'] > 0]
        avg_duration = valid_runs['Approximate Duration (Minutes)'].mean()
        
        # Most frequent victim (Exclude Ender Dragon from being called a 'victim')
        player_only_deaths = filtered_df[filtered_df['Player Death'] != 'Ender dragon']
        if not player_only_deaths.empty:
            most_frequent_victim = player_only_deaths['Player Death'].value_counts().idxmax()
            victim_count = player_only_deaths['Player Death'].value_counts().max()
            most_common_death = player_only_deaths['Cause of Death'].value_counts().idxmax()
            most_common_death_count = player_only_deaths['Cause of Death'].value_counts().max()
        else:
            most_frequent_victim = "N/A"
            victim_count = 0
            most_common_death = "N/A"
            most_common_death_count = 0

        # Display Metrics
        st.markdown(f"""
            <style>
            .metric-container {{
                display: flex;
                justify-content: space-around;
                align-items: stretch;
                gap: 20px;
                margin: 30px 0 50px 0;
                flex-wrap: wrap;
            }}
            .metric-box {{
                flex: 1;
                min-width: 200px;
                text-align: center;
                padding: 20px;
                background: #1b1d22;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            .metric-label {{ font-size: 18px; color: rgba(255, 255, 255, 0.7); margin-bottom: 10px; }}
            .metric-value {{ font-size: 36px; font-weight: bold; color: white; margin: 10px 0; }}
            .metric-delta {{ font-size: 14px; color: #00C853; margin-top: 5px; }}
            </style>
            
            <div class="metric-container">
                <div class="metric-box">
                    <div class="metric-label">⏱️ Total Playtime</div>
                    <div class="metric-value">{int(total_time):,} min</div>
                    <div class="metric-delta">{total_time/60:.1f} hours</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">📊 Avg Run Duration</div>
                    <div class="metric-value">{int(avg_duration)} min</div>
                    <div class="metric-delta">{len(valid_runs)} resets</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">💀 Most Common Death</div>
                    <div class="metric-value">{most_common_death}</div>
                    <div class="metric-delta">{most_common_death_count} times</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">🪦 Top Dead Streamer</div>
                    <div class="metric-value">{most_frequent_victim}</div>
                    <div class="metric-delta">{victim_count} deaths</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # ==================== DEATH CHART ====================
        st.subheader("Death Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Who Dies to What?")
            death_data = filtered_df.groupby(['Player Death', 'Cause of Death']).size().reset_index(name='Deaths')
            
            fig = go.Figure()
            all_causes = death_data['Cause of Death'].unique()
            colors = ['#EF5350', '#EC407A', '#AB47BC', '#7E57C2', '#5C6BC0', '#42A5F5', '#29B6F6', '#26C6DA', '#26A69A', '#66BB6A', '#9CCC65', '#D4E157', '#FFEE58', '#FFCA28', '#FFA726', '#FF7043']
            color_map = {cause: colors[i % len(colors)] for i, cause in enumerate(all_causes)}
            
            for player in death_data['Player Death'].unique():
                p_data = death_data[death_data['Player Death'] == player]
                for _, row in p_data.iterrows():
                    fig.add_trace(go.Bar(
                        name=row['Cause of Death'],
                        y=[player],
                        x=[row['Deaths']],
                        orientation='h',
                        marker=dict(color=color_map.get(row['Cause of Death'])),
                        showlegend=False,
                        hovertemplate=f"<b>{player}</b><br>Cause: {row['Cause of Death']}<br>Count: {row['Deaths']}<extra></extra>"
                    ))
            
            fig.update_layout(barmode='stack', height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Total Time Wasted by Player")
            time_data = filtered_df.groupby('Player Death')['Approximate Duration (Minutes)'].sum().sort_values()
            
            fig_time = go.Figure(go.Bar(
                x=time_data.values,
                y=time_data.index,
                orientation='h',
                marker=dict(color='#FFA726'),
                text=time_data.values,
                textposition='auto'
            ))
            fig_time.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0), xaxis_title="Minutes")
            st.plotly_chart(fig_time, use_container_width=True)

        st.markdown("---")

        # ==================== TIMELINE ====================
        st.subheader("Run Timeline")
        
        fig_timeline = go.Figure()
        
        # Sort by Run ID to ensure correct order
        timeline_df = filtered_df.sort_values('Run')
        
        # Create colors for players - ADDED PURPLE FOR DRAGON
        player_colors = {
            'Neuro': '#FF80AB',
            'Vedal': '#82B1FF',
            'Filian': '#CCFF90',
            'Crelly': '#FFD180',
            'Filian/neuro': '#A7FFEB',
            'Ender dragon': '#9C27B0' # Victory Color
        }
        
        for idx, row in timeline_df.iterrows():
            duration = row['Approximate Duration (Minutes)']
            if duration <= 0: continue # Skip mid-run deaths in timeline
            
            player = row['Player Death']
            color = player_colors.get(player, '#B0BEC5')
            
            fig_timeline.add_trace(go.Bar(
                name=f"Run {row['Run']}",
                y=[f"Day {row['Day']}"],
                x=[duration],
                orientation='h',
                marker=dict(color=color, line=dict(width=1, color='black')),
                text=f"Run {row['Run']}" if duration > 15 else "",
                textposition='inside',
                hovertemplate=f"<b>Run {row['Run']}</b><br>Player: {player}<br>Time: {duration}m<br>Cause: {row['Cause of Death']}<extra></extra>",
                showlegend=False
            ))
            
        fig_timeline.update_layout(
            barmode='stack', 
            height=400,
            yaxis=dict(autorange="reversed"),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # ==================== PROGRESSION CHARTS ====================
        st.markdown("---")
        st.subheader("Trends & Progression")
        
        tab1, tab2 = st.tabs(["☠️ The Death Race", "📈 Performance Trend"])
        
        with tab1:
            st.caption("Cumulative deaths over time (The Race to the Bottom)")
            fig_race = go.Figure()
            
            death_cols = {
                'Neuro Deaths': '#FF80AB', 
                'Filian Deaths': '#CCFF90', 
                'Vedal Deaths': '#82B1FF', 
                'Crelly Deaths': '#FFD180'
            }
            
            progression_df = df.sort_values('Run')
            
            for col_name, color in death_cols.items():
                fig_race.add_trace(go.Scatter(
                    x=progression_df['Run'],
                    y=progression_df[col_name],
                    mode='lines',
                    name=col_name.replace(' Deaths', ''),
                    line=dict(color=color, width=3),
                    hovertemplate=f"<b>{col_name.replace(' Deaths', '')}</b><br>Run %{{x}}<br>Total Deaths: %{{y}}<extra></extra>"
                ))
                
            fig_race.update_layout(
                xaxis_title="Run Number", 
                yaxis_title="Total Deaths",
                hovermode="x unified",
                height=400,
                margin=dict(l=0, r=0, t=20, b=0),
                legend=dict(orientation="h", y=1.1)
            )
            st.plotly_chart(fig_race, use_container_width=True)
            
        with tab2:
            st.caption("Average Run Length over time")
            fig_trend = go.Figure()
            
            progression_df['Avg_Clean'] = pd.to_numeric(
                progression_df['Avg Run Length'].astype(str).str.replace(' minutes', ''), 
                errors='coerce'
            )
            
            fig_trend.add_trace(go.Scatter(
                x=progression_df['Run'],
                y=progression_df['Avg_Clean'],
                mode='lines+markers',
                name='Global Average',
                line=dict(color='#00E676', width=3),
                fill='tozeroy',
                fillcolor='rgba(0, 230, 118, 0.1)'
            ))
            
            fig_trend.update_layout(
                xaxis_title="Run Number", 
                yaxis_title="Average Minutes",
                height=400,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown("---")

        # ==================== DATA TABLE ====================
        st.subheader("Detailed Run Log")
        
        display_cols = ['Day', 'Run', 'Dead', 'Time Of Death (UTC)', 'Cause Of Death', 'Run Length', 'Notes']
        
        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Run": st.column_config.NumberColumn(format="%d"),
            }
        )

    except Exception as e:
        st.error(f"Error processing data: {e}")
        st.code(str(e))
else:
    st.error("No data found.")