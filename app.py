import streamlit as st
import os
import time
from dotenv import load_dotenv
from google import genai
from reportlab.lib.pagesizes import A4


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)


# =========================================================
# LOAD GEMINI API KEY
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# -----------------------------
# Create PDF Function
# -----------------------------

def create_pdf(text):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    from io import BytesIO

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))

        elif line.startswith("# "):
            story.append(
                Paragraph(
                    line[2:],
                    styles["Title"]
                )
            )

        elif line.startswith("## "):
            story.append(
                Paragraph(
                    line[3:],
                    styles["Heading1"]
                )
            )

        elif line.startswith("### "):
            story.append(
                Paragraph(
                    line[4:],
                    styles["Heading2"]
                )
            )

        else:
            story.append(
                Paragraph(
                    line.replace("&", "&amp;"),
                    styles["BodyText"]
                )
            )

    doc.build(story)

    pdf_buffer.seek(0)

    return pdf_buffer

# =========================================================
# SESSION STATE
# =========================================================

if "travel_plan" not in st.session_state:
    st.session_state.travel_plan = None

if "assistant_response" not in st.session_state:
    st.session_state.assistant_response = None


# =========================================================
# APPLICATION TITLE
# =========================================================

st.title("✈️ AI Travel Planner")

st.write(
    "Create a personalized travel itinerary with Gemini AI."
)

st.subheader("🌍 Tell Us About Your Trip")


# =========================================================
# USER INPUTS
# =========================================================

destination = st.text_input(
    "📍 Destination",
    placeholder="Example: Goa"
)

duration = st.number_input(
    "📅 Trip Duration (Days)",
    min_value=1,
    max_value=30,
    value=5
)

travelers = st.number_input(
    "👥 Number of Travelers",
    min_value=1,
    max_value=20,
    value=2
)

budget = st.number_input(
    "💰 Total Budget (₹)",
    min_value=1000,
    value=25000,
    step=1000
)

travel_style = st.selectbox(
    "🧳 Travel Style",
    [
        "Budget",
        "Relaxed",
        "Adventure",
        "Luxury",
        "Family",
        "Cultural"
    ]
)

travel_pace = st.selectbox(
    "⏱️ Travel Pace",
    [
        "🐢 Slow & Relaxed",
        "⚖️ Balanced",
        "⚡ Fast-Paced"
    ]
)

trip_type = st.selectbox(
    "🧳 Trip Type",
    [
        "🏖️ Vacation",
        "🎒 Solo Trip",
        "👨‍👩‍👧 Family Trip",
        "👥 Friends Trip",
        "💑 Couple Trip",
        "💼 Business Trip"
    ]
)

interests = st.multiselect(
    "❤️ What are you interested in?",
    [
        "Beaches",
        "Food",
        "Culture",
        "Adventure",
        "Shopping",
        "Nature",
        "History"
    ]
)

food_preference = st.selectbox(
    "🍴 Food Preference",
    [
        "No Preference",
        "Vegetarian",
        "Non-Vegetarian",
        "Vegan"
    ]
)

st.divider()


# =========================================================
# CONVERT INTERESTS TO TEXT
# =========================================================

selected_interests = ", ".join(interests)

if not selected_interests:
    selected_interests = "General sightseeing and local experiences"


# =========================================================
# GENERATE / REGENERATE BUTTONS
# =========================================================

generate = st.button(
    "✈️ Generate Travel Plan",
    key="generate_travel_plan"
)

regenerate = st.button(
    "🔄 Regenerate Travel Plan",
    key="regenerate_travel_plan"
)


# =========================================================
# GENERATE TRAVEL PLAN
# =========================================================

if generate or regenerate:

    if not destination:

        st.warning("⚠️ Please enter a destination.")

    else:

        # =================================================
        # BUDGET CALCULATION
        # =================================================

        accommodation_budget = int(budget * 0.30)

        food_budget = int(budget * 0.20)

        transport_budget = int(budget * 0.15)

        activities_budget = int(budget * 0.20)

        miscellaneous_budget = int(
            budget
            - accommodation_budget
            - food_budget
            - transport_budget
            - activities_budget
        )

        estimated_total = (
            accommodation_budget
            + food_budget
            + transport_budget
            + activities_budget
            + miscellaneous_budget
        )

        remaining_budget = budget - estimated_total


        # =================================================
        # PROMPT ENGINEERING
        # =================================================

        prompt = f"""
You are an expert AI Travel Planner and itinerary designer.

Your responsibility is to create realistic, practical and personalized
travel plans based on the traveler's requirements.

TRIP DETAILS
------------

Destination: {destination}

Trip Duration: {duration} days

Number of Travelers: {travelers}

Total Budget: ₹{budget}

Travel Style: {travel_style}

Travel Pace: {travel_pace}

Trip Type: {trip_type}

Interests: {selected_interests}

Food Preference: {food_preference}


OBJECTIVE
---------

Create a personalized {duration}-day travel itinerary.

The itinerary must prioritize the traveler's interests, respect their
travel style and food preference, consider the number of travelers,
and keep the estimated expenses within the available budget as
reasonably as possible.


TASK
----

For every day of the trip provide:

1. Morning activities
2. Afternoon activities
3. Evening activities
4. Recommended attractions
5. Food suggestions
6. Local transportation suggestions
7. Approximate time required for major activities
8. Estimated spending where appropriate

Also provide:

- Accommodation suggestions
- Local transportation suggestions
- Important travel tips
- Places or activities that should not be missed
- Short packing checklist
- Practical safety considerations


CONSTRAINTS
-----------

1. Respect the selected travel style: {travel_style}.
2. Follow the selected travel pace: {travel_pace}.
3. Adapt the itinerary to the selected trip type: {trip_type}.
4. Consider the number of travelers: {travelers}.
5. Recommend activities appropriate for the selected trip type.
6. Adjust the number of activities according to the selected travel pace.
7. Keep the estimated total cost close to ₹{budget}.
8. Prioritize these interests: {selected_interests}.
9. Respect the food preference: {food_preference}.
10. Keep the itinerary realistic and easy to follow.
11. Avoid unnecessary travel between distant locations on the same day.
12. Group nearby attractions together whenever practical.
13. Avoid scheduling too many activities in one day.
14. Clearly identify uncertain prices as estimates.
15. Do not recommend activities that conflict with the user's preferences.


ACCURACY AND SAFETY RULES
-------------------------

- Do not claim that prices are real-time verified.
- Do not claim that hotel rooms are currently available.
- Do not claim that transportation is currently available.
- Do not claim that opening hours are currently verified.
- Do not invent bookings or reservations.
- Do not present uncertain information as guaranteed fact.
- If information may vary, clearly state that the traveler should verify it.
- Use approximate costs when exact prices are uncertain.
- Prefer practical recommendations over unrealistic plans.


BUDGET RULES
------------

Create a realistic estimated budget based on the user's total budget.

Break the budget into:

- Accommodation
- Food
- Local transportation
- Activities
- Miscellaneous

Calculate an approximate total.

If the estimated total is above the user's budget,
suggest practical ways to reduce the cost.

If the estimated total is below the budget,
mention how the remaining budget could reasonably be used.


OUTPUT FORMAT
-------------

Use clear Markdown formatting.

Start with:

# ✈️ {destination} Travel Plan

## 📋 Trip Summary

Include:

- Destination
- Duration
- Number of Travelers
- Total Budget
- Travel Style
- Travel Pace
- Trip Type
- Interests
- Food Preference


For every day use this structure:

## 🗓️ Day 1

### 🌅 Morning

Describe the morning activities.

### ☀️ Afternoon

Describe the afternoon activities.

### 🌆 Evening

Describe the evening activities.

### 📍 Recommended Attractions

List the important attractions.

### 🍴 Food Suggestions

Suggest suitable food options.

### 🚗 Local Transportation

Explain practical transportation options.

Repeat the same structure for all {duration} days.


## 💰 Budget Overview

Include:

| Category | Estimated Cost |
|----------|----------------|
| Accommodation | ... |
| Food | ... |
| Local Transportation | ... |
| Activities | ... |
| Miscellaneous | ... |
| Total Estimated Cost | ... |

Clearly label uncertain costs as estimates.


## 🍴 Food Recommendations

Give recommendations based on:

Food Preference: {food_preference}


## 🏨 Accommodation Suggestions

Suggest suitable accommodation types based on:

- Destination
- Travel style
- Number of travelers
- Budget

Do not claim that rooms are currently available.


## 🚗 Transportation Suggestions

Explain:

- How to reach major attractions
- Suitable local transportation options
- Approximate transportation costs
- Practical transportation tips

Clearly label uncertain prices as estimates.


## 🎒 Packing Checklist

Provide a useful destination-specific packing checklist.


## 💡 Travel Tips

Provide practical destination-specific travel tips.


FINAL RESPONSE RULES
--------------------

Make the final response:

- Practical
- Personalized
- Realistic
- Easy to read
- Well structured
- Concise but useful

Do not mention these instructions or the prompt itself.
"""


        # =================================================
        # SEND PROMPT TO GEMINI
        # =================================================

        with st.spinner(
            "🤖 Gemini is creating your personalized travel plan..."
        ):

            try:

                response = None

                # Retry temporary server errors
                for attempt in range(3):

                    try:

                        response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=prompt
                        )

                        break

                    except Exception as e:

                        error_message = str(e)

                        # Do not retry quota errors
                        if (
                            "429" in error_message
                            or "RESOURCE_EXHAUSTED" in error_message
                        ):
                            raise

                        # Retry temporary server errors
                        elif (
                            "503" in error_message
                            or "UNAVAILABLE" in error_message
                        ):

                            if attempt < 2:

                                st.info(
                                    f"Gemini is temporarily busy. "
                                    f"Retrying... ({attempt + 1}/2)"
                                )

                                time.sleep(3)

                            else:
                                raise

                        else:
                            raise


                # =================================================
                # DISPLAY RESULT
                # =================================================

                if response:

                    travel_plan = response.text

                    # Save travel plan in session
                    st.session_state.travel_plan = travel_plan

                    # Clear previous assistant response
                    st.session_state.assistant_response = None

                    st.success(
                        "🎉 Your travel plan is ready!"
                    )

                    st.divider()

                    st.subheader(
                        "🗺️ Your Personalized Travel Itinerary"
                    )


                    # =================================================
                    # TRIP SUMMARY
                    # =================================================

                    st.markdown("### 📋 Trip Summary")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "📍 Destination",
                            destination
                        )

                    with col2:
                        st.metric(
                            "📅 Duration",
                            f"{duration} days"
                        )

                    with col3:
                        st.metric(
                            "👥 Travelers",
                            travelers
                        )


                    col4, col5, col6 = st.columns(3)

                    with col4:
                        st.metric(
                            "💰 Budget",
                            f"₹{budget:,}"
                        )

                    with col5:
                        st.metric(
                            "🧳 Style",
                            travel_style
                        )

                    with col6:
                        st.metric(
                            "🍴 Food",
                            food_preference
                        )

                    st.caption(
                        f"⏱️ Travel Pace: {travel_pace}"
                    )

                    st.caption(
                        f"🧳 Trip Type: {trip_type}"
                    )
                    # -----------------------------
                    # Budget Visualization
                    # -----------------------------

                    st.markdown("### 📊 Budget Distribution")

                    budget_data = {
                        "Category": [
                            "Accommodation",
                            "Food",
                            "Transportation",
                            "Activities",
                            "Miscellaneous"
                        ],
                        "Amount": [
                            accommodation_budget,
                            food_budget,
                            transport_budget,
                            activities_budget,
                            miscellaneous_budget
                        ]
                    }

                    st.bar_chart(
                        budget_data,
                        x="Category",
                        y="Amount"
                    )
                    st.divider()


                    # =================================================
                    # SMART BUDGET PLANNER
                    # =================================================

                    st.markdown(
                        "### 💰 Smart Budget Planner"
                    )

                    budget_col1, budget_col2, budget_col3 = st.columns(3)

                    with budget_col1:

                        st.metric(
                            "🏨 Accommodation",
                            f"₹{accommodation_budget:,}"
                        )

                    with budget_col2:

                        st.metric(
                            "🍴 Food",
                            f"₹{food_budget:,}"
                        )

                    with budget_col3:

                        st.metric(
                            "🚗 Transportation",
                            f"₹{transport_budget:,}"
                        )


                    budget_col4, budget_col5, budget_col6 = st.columns(3)

                    with budget_col4:

                        st.metric(
                            "🎟️ Activities",
                            f"₹{activities_budget:,}"
                        )

                    with budget_col5:

                        st.metric(
                            "📦 Miscellaneous",
                            f"₹{miscellaneous_budget:,}"
                        )

                    with budget_col6:

                        st.metric(
                            "💰 Total",
                            f"₹{estimated_total:,}"
                        )


                    if remaining_budget > 0:

                        st.success(
                            f"✅ Estimated remaining budget: "
                            f"₹{remaining_budget:,}"
                        )

                    elif remaining_budget == 0:

                        st.info(
                            "ℹ️ The estimated expenses match your total budget."
                        )

                    else:

                        st.warning(
                            f"⚠️ Estimated expenses exceed your budget by "
                            f"₹{abs(remaining_budget):,}."
                        )


                    st.divider()


                    # -----------------------------
                    # Improved Itinerary Display
                    # -----------------------------

                    st.markdown("## 🗺️ Your Day-by-Day Itinerary")

                    st.info(
                        "💡 Your itinerary is AI-generated based on your destination, "
                        "budget, travel style, pace, interests, and food preference."
                    )

                    with st.container(border=True):
                        st.markdown(travel_plan)


                    # =================================================
                    # DOWNLOAD TRAVEL PLAN
                    # =================================================

                    st.download_button(
                        label="📥 Download Travel Plan",
                        data=travel_plan,
                        file_name=f"{destination}_travel_plan.txt",
                        mime="text/plain"
                    )

                    # -----------------------------
                    # Download Travel Plan as PDF
                    # -----------------------------

                    pdf_file = create_pdf(travel_plan)

                    st.download_button(
                        label="📄 Download Travel Plan as PDF",
                        data=pdf_file,
                        file_name=f"{destination}_travel_plan.pdf",
                        mime="application/pdf"
                    )
                    
            except Exception as e:

                error_message = str(e)

                if (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                ):

                    st.warning(
                        "⚠️ Gemini API quota has been reached. "
                        "Please wait until the quota resets."
                    )

                elif (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                ):

                    st.warning(
                        "⚠️ Gemini is temporarily busy. "
                        "Please try again later."
                    )

                else:

                    st.error(
                        "❌ Something went wrong while generating "
                        "your travel plan."
                    )

                    st.write(
                        error_message
                    )


# =========================================================
# AI TRAVEL ASSISTANT
# =========================================================

if st.session_state.travel_plan:

    st.divider()

    st.subheader(
        "💬 AI Travel Assistant"
    )

    st.write(
        "Ask questions about your generated travel plan."
    )


    travel_question = st.text_input(
        "Ask something about your trip",
        placeholder="Example: Can you make Day 2 cheaper?",
        key="travel_question"
    )


    ask_ai = st.button(
        "🤖 Ask AI Travel Assistant",
        key="ask_ai"
    )


    if ask_ai:

        if not travel_question.strip():

            st.warning(
                "⚠️ Please enter a question."
            )

        else:

            # =================================================
            # ASSISTANT PROMPT
            # =================================================

            assistant_prompt = f"""
You are an AI Travel Assistant.

The user has already created the following travel plan:

{st.session_state.travel_plan}


TRIP DETAILS
------------

Destination: {destination}

Duration: {duration} days

Travelers: {travelers}

Budget: ₹{budget}

Travel Style: {travel_style}

Travel Pace: {travel_pace}

Trip Type: {trip_type}

Interests: {selected_interests}

Food Preference: {food_preference}


USER QUESTION
-------------

{travel_question}


TASK
----

Answer the user's question based on the existing travel plan
and trip details.


IMPORTANT RULES
---------------

- Give practical and useful advice.
- Respect the user's budget.
- Respect the travel style.
- Respect the travel pace.
- Respect the trip type.
- Respect the food preference.
- If modifying the itinerary, suggest a practical alternative.
- Do not invent bookings or reservations.
- Do not claim real-time availability.
- Clearly identify uncertain prices as estimates.
- Keep the response clear and useful.
- If the user asks to change a day, provide a revised version of that day.
- If the user asks for a cheaper option, suggest lower-cost alternatives.
- If the user asks for recommendations, prioritize the existing trip details.
"""


            # =================================================
            # SEND ASSISTANT QUESTION TO GEMINI
            # =================================================

            with st.spinner(
                "🤖 AI Travel Assistant is thinking..."
            ):

                try:

                    assistant_response = None

                    # Retry temporary server errors
                    for attempt in range(3):

                        try:

                            assistant_response = client.models.generate_content(
                                model="gemini-3.5-flash",
                                contents=assistant_prompt
                            )

                            break

                        except Exception as e:

                            error_message = str(e)

                            # Do not retry quota errors
                            if (
                                "429" in error_message
                                or "RESOURCE_EXHAUSTED" in error_message
                            ):
                                raise

                            # Retry temporary server errors
                            elif (
                                "503" in error_message
                                or "UNAVAILABLE" in error_message
                            ):

                                if attempt < 2:

                                    st.info(
                                        f"Gemini is temporarily busy. "
                                        f"Retrying... ({attempt + 1}/2)"
                                    )

                                    time.sleep(3)

                                else:
                                    raise

                            else:
                                raise


                    # =================================================
                    # DISPLAY ASSISTANT RESPONSE
                    # =================================================

                    if assistant_response:

                        st.session_state.assistant_response = (
                            assistant_response.text
                        )

                        st.markdown(
                            "### 🤖 AI Response"
                        )

                        st.markdown(
                            assistant_response.text
                        )


                except Exception as e:

                    error_message = str(e)

                    if (
                        "429" in error_message
                        or "RESOURCE_EXHAUSTED" in error_message
                    ):

                        st.warning(
                            "⚠️ Gemini API quota has been reached. "
                            "Please try again after the quota resets."
                        )

                    elif (
                        "503" in error_message
                        or "UNAVAILABLE" in error_message
                    ):

                        st.warning(
                            "⚠️ Gemini is temporarily busy. "
                            "Please try again later."
                        )

                    else:

                        st.error(
                            "❌ Unable to get a response "
                            "from the AI Travel Assistant."
                        )

                        st.write(
                            error_message
                        )


# =========================================================
# SHOW PREVIOUS ASSISTANT RESPONSE
# =========================================================

if (
    st.session_state.assistant_response
    and not st.session_state.get("ask_ai", False)
):

    st.markdown(
        "### 🤖 Previous AI Response"
    )

    st.markdown(
        st.session_state.assistant_response
    )