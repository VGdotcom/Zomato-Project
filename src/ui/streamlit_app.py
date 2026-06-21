import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from src.models.preferences import UserPreferences
from src.services.recommendation import RecommendationService

st.set_page_config(page_title="Zomato AI Recommender", page_icon="🍔", layout="wide")

@st.cache_resource
def get_service():
    return RecommendationService()

service = get_service()

st.title("Zomato AI Restaurant Recommender")
st.markdown("Find the perfect place to eat based on your specific preferences!")

with st.sidebar:
    st.header("Your Preferences")
    
    location = st.text_input("Location", placeholder="e.g. Indiranagar")
    budget = st.selectbox("Budget", options=["low", "medium", "high"])
    min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
    cuisine = st.text_input("Preferred Cuisine (Optional)", placeholder="e.g. Italian, Chinese")
    notes = st.text_area("Custom Notes (Optional)", placeholder="e.g. Looking for a romantic place...")
    
    submit = st.button("Find Restaurants")

if submit:
    if not location:
        st.error("Please enter a location!")
    else:
        prefs = UserPreferences(
            location=location,
            budget=budget,
            min_rating=min_rating,
            cuisine=cuisine if cuisine else None,
            custom_notes=notes if notes else None
        )
        
        with st.spinner("Analyzing top candidates with AI..."):
            try:
                response, fallbacks = service.get_recommendations(prefs)
                
                if fallbacks.get("cuisine_dropped"):
                    st.warning("⚠️ Couldn't find exact cuisine matches. Broadened search.")
                if fallbacks.get("rating_dropped"):
                    st.warning("⚠️ Couldn't meet minimum rating. Lowered rating threshold.")
                
                if not response.recommendations:
                    st.error("No restaurants found matching your criteria in this location.")
                else:
                    st.success("Here are your top recommendations!")
                    
                    for rec in response.recommendations:
                        with st.container():
                            st.subheader(f"#{rec.rank} {rec.name}")
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.metric("Rating", f"{rec.rating} ⭐")
                                st.write(f"**Cost:** ₹{rec.cost}")
                                st.write(f"**Cuisine:** {rec.cuisine}")
                            with col2:
                                st.info(f"**Why we recommend this:**\n\n{rec.rationale}")
                            st.divider()
            except Exception as e:
                st.error(f"An error occurred: {e}")
