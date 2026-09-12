# ✈️ AI Travel Planner

An AI-powered travel planning application that generates personalized trip itineraries using **Google Gemini AI** and **Streamlit**.

The application allows users to provide their destination, trip duration, number of travelers, budget, travel style, interests, travel pace, trip type, and food preference. Gemini AI then generates a personalized travel plan based on the user's requirements.

## 🚀 Live Demo

**Live Application:**
https://theerthapn-ai-travel-planner.streamlit.app/

## 📌 Project Overview

Planning a trip manually can require significant time and effort. Travelers need to research destinations, activities, food, transportation, accommodation, budgets, and daily schedules.

The **AI Travel Planner** simplifies this process by using Prompt Engineering and Generative AI to create a personalized travel itinerary.

Users enter their travel preferences, and the application generates a structured travel plan with:

* 📅 Daily itinerary
* 🏝️ Recommended attractions
* 🍴 Food recommendations
* 🏨 Accommodation guidance
* 🚗 Local transportation suggestions
* 💰 Budget planning
* 🎒 Packing checklist
* 💡 Travel tips
* 🤖 AI Travel Assistant

## ✨ Key Features

### 1. Personalized AI Travel Planning

Users can specify:

* Destination
* Number of days
* Number of travelers
* Budget
* Travel style
* Travel pace
* Trip type
* Interests
* Food preference

Gemini generates a customized itinerary based on these inputs.

### 2. 🗓️ Daily Itinerary Generation

The AI generates a structured itinerary containing:

* Morning activities
* Afternoon activities
* Evening activities
* Attractions
* Food suggestions
* Local transportation
* Estimated time
* Estimated spending

### 3. 💰 Smart Budget Planner

The application provides an estimated budget distribution across:

* Accommodation
* Food
* Transportation
* Activities
* Miscellaneous expenses

### 4. 🔄 Regenerate Travel Plan

Users can regenerate the itinerary when they want an alternative plan.

### 5. 🤖 AI Travel Assistant

After generating a travel plan, users can ask follow-up questions such as:

* "Can you make Day 2 cheaper?"
* "Suggest more food options."
* "Can I add another beach?"
* "Make this trip more relaxed."
* "Suggest activities for children."
* "Reduce the transportation cost."

The AI assistant uses the generated travel plan as context when answering follow-up questions.

### 6. 🍴 Food Preference Support

Users can select:

* No Preference
* Vegetarian
* Non-Vegetarian
* Vegan

The generated travel recommendations take the selected food preference into consideration.

### 7. 📥 Download Travel Plan

Users can download the generated travel itinerary as a text file.

## 🧠 Prompt Engineering Techniques

This project demonstrates several Prompt Engineering concepts:

### Role Engineering

The AI is instructed to act as an experienced travel planner.

### Context Engineering

The prompt provides the AI with:

* Destination
* Duration
* Budget
* Travelers
* Interests
* Travel style
* Travel pace
* Trip type
* Food preference

### Constraint-Based Prompting

The AI is given constraints for:

* Budget
* Itinerary structure
* Estimated costs
* Travel duration
* Personal preferences

### Structured Output

The prompt requests specific sections such as:

* Daily itinerary
* Attractions
* Food
* Transportation
* Budget
* Packing checklist
* Travel tips

### Follow-Up Prompting

The AI Travel Assistant allows users to refine the generated plan using follow-up questions.

## 🏗️ Application Architecture

```text
User
  │
  ▼
Streamlit Web Interface
  │
  ▼
Travel Preferences
  │
  ▼
Prompt Engineering Layer
  │
  ▼
Google Gemini API
  │
  ▼
AI Generated Travel Plan
  │
  ├── Daily Itinerary
  ├── Budget Planner
  ├── Food Recommendations
  ├── Transportation
  ├── Packing Checklist
  └── Travel Tips
  │
  ▼
AI Travel Assistant
  │
  ▼
Refined Travel Recommendations
```

## 🛠️ Technology Stack

| Technology                | Purpose                               |
| ------------------------- | ------------------------------------- |
| Python                    | Application development               |
| Streamlit                 | Web application interface             |
| Google Gemini API         | Generative AI                         |
| Google GenAI SDK          | Gemini API integration                |
| python-dotenv             | Local environment variable management |
| Git                       | Version control                       |
| GitHub                    | Source code repository                |
| Streamlit Community Cloud | Application deployment                |

## 📂 Project Structure

```text
ai-travel-planner/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

> `.env` contains the local Gemini API key and is intentionally excluded from GitHub using `.gitignore`.

For deployment, the Gemini API key is stored securely using Streamlit Secrets.

## ⚙️ Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/theerthapn/ai-travel-planner.git
```

### 2. Open the project

```bash
cd ai-travel-planner
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Create a `.env` file in the project folder:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔐 Security

The Gemini API key is **not stored in the GitHub repository**.

For local development, the key is stored in `.env`.

For Streamlit deployment, the key is stored using Streamlit Secrets.

This prevents sensitive credentials from being committed to the public repository.

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

The GitHub repository acts as the source repository, and changes pushed to the repository can be reflected in the deployed application. Streamlit Community Cloud uses the repository's dependency file to install Python packages required by the application.

## 🎯 Learning Outcomes

This project demonstrates practical knowledge of:

* Prompt Engineering
* Generative AI
* Google Gemini API
* Python
* Streamlit
* API integration
* Context engineering
* Constraint-based prompting
* Structured AI output
* Session state
* Git and GitHub
* Cloud deployment
* API key security

## 🔮 Future Enhancements

Possible future improvements include:

* 🗺️ Interactive maps
* 🌦️ Real-time weather information
* ✈️ Flight information integration
* 🏨 Hotel API integration
* 🚆 Transportation API integration
* 💱 Multi-currency support
* 🌍 Multi-language travel planning
* 📍 Location-based recommendations
* 📱 Mobile-friendly enhancements
* 🧠 More advanced itinerary optimization

## 👨‍💻 Project

**AI Travel Planner – Gemini-Powered Trip Planner & Itinerary Assistant**

Built as a Prompt Engineering and Generative AI capstone project.

---

⭐ If you find this project useful, consider giving the repository a star!
