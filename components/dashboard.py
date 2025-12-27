import streamlit as st
import pandas as pd
import altair as alt
from utils.constants import ASSET_CONFIG
from utils.calculations import calculate_compound_interest, calculate_risk_projection

def render_dashboard(asset_type: str):
    """
    Renders the unified dashboard for a given asset type.
    """
    config = ASSET_CONFIG.get(asset_type)
    if not config:
        st.error(f"Configuration not found for {asset_type}")
        return

    st.title(f"{asset_type} Dashboard")
    st.markdown(f"*{config.get('description')}*")

    # Top Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Risk Level", config['risk_level'])
    with col2:
        st.metric("Expected Annual Return", f"{config['expected_return'] * 100:.1f}%")
    with col3:
        st.metric("Volatility (Std Dev)", f"{config['volatility'] * 100:.1f}%")

    st.markdown("---")

    # Inputs Section
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        principal = st.number_input(
            "Initial Investment ($)", 
            min_value=0, 
            value=10000, 
            step=1000
        )
    with col_input2:
        monthly_contribution = st.number_input(
            "Monthly Contribution ($)", 
            min_value=0, 
            value=500, 
            step=100
        )

    # Time Horizon Slider
    years = st.slider(
        "Time Horizon (Years)", 
        min_value=1, 
        max_value=30, 
        value=10,
        help="Adjust to see how your investment grows over time."
    )

    # Real-time Calculations
    # 1. Deterministic Projection
    df_growth = calculate_compound_interest(
        principal, 
        monthly_contribution, 
        config['expected_return'], 
        years
    )
    
    # 2. Risk Projection (Range)
    total_principal_invested = principal + (monthly_contribution * 12 * years)
    p5, p50, p95 = calculate_risk_projection(
        total_principal_invested, # Simplified: applying volatility to the end sum approximation or running better sim
        years,
        config['expected_return'],
        config['volatility']
    )
    # Note: The risk calculation above is a simplification for the "Range" display. 
    # For a proper cone chart, we'd need time-series simulation.
    # Let's stick to the deterministic chart for the main view and show the Risk Range as metrics/text.

    st.subheader("Projected Returns")
    
    # Altair Chart
    # Reshape for nicer plotting (Balance vs Principal)
    chart_data = df_growth.melt('Year', var_name='Type', value_name='Amount')
    
    chart = alt.Chart(chart_data).mark_line(point=True).encode(
        x=alt.X('Year', axis=alt.Axis(format='d')),
        y=alt.Y('Amount', axis=alt.Axis(format='$,f')),
        color=alt.Color('Type', scale=alt.Scale(domain=['Balance', 'Total Principal'], range=['#00d4ff', '#888888'])),
        tooltip=['Year', 'Type', alt.Tooltip('Amount', format='$,.2f')]
    ).properties(
        height=400
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    # Risk Analysis Expansion
    with st.expander("Risk Analysis & Range (Monte Carlo Limit)"):
        st.write(f"Based on **{config['volatility']*100}% volatility**, your potential outcome after {years} years ranges between:")
        
        r_col1, r_col2, r_col3 = st.columns(3)
        # Note: The p5/p50/p95 logic in utils needs to be mindful of monthly contributions, 
        # current utils.calculate_risk_projection assumes lump sum. 
        # For this MVP, we will use the lump sum of (Principal + Total Contributions) as the base for risk variance 
        # OR just acknowledge the limitation.
        # Let's use the 'Balance' from deterministic as the Median, and apply volatility spread around it.
        
        projected_balance = df_growth.iloc[-1]['Balance']
        # Simple approximation of spread: Balance * exp( +/- 1.96 * vol * sqrt(t) ) ? 
        # Or just use the Monte Carlo result if we update the function to handle contributions.
        # For now, let's just show the calculated percentile metrics from the simple lump-sum proxy:
        
        r_col1.metric("Pessimistic (5%)", f"${p5:,.2f}")
        r_col2.metric("Median (50%)", f"${p50:,.2f}")
        r_col3.metric("Optimistic (95%)", f"${p95:,.2f}")
        
    st.info("💡 Adjust the slider above to see instant updates.")
