# FinVoice - AI-Powered Financial Management & Advisory Assistant

FinVoice is a comprehensive financial management application that uses AI to help users track expenses, visualize spending patterns, receive personalized financial advice, and plan for financial goals.

## Features

- **Voice Input to Expense Logger**: Add expenses using voice commands
- **Expense Categorization**: Automatically categorize expenses using AI
- **Financial Dashboard**: Visualize spending patterns with interactive charts
- **AI Financial Advisor**: Get personalized financial advice based on spending habits
- **Goal Planner**: Set financial goals and track progress with SIP calculations

## Project Structure

```
FinVoice/
├── frontend/           # React web application
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── App.js      # Main application component
│   │   └── index.js    # Entry point
│   └── package.json    # Frontend dependencies
├── backend/            # Node.js Express server
│   ├── routes/         # API routes
│   ├── server.js       # Express server setup
│   └── package.json    # Backend dependencies
└── ml_service/         # Python FastAPI service for AI/ML
    ├── main.py         # FastAPI application
    ├── categorizer.py  # Expense categorization logic
    └── requirements.txt # Python dependencies
```

## Quick Start

### Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- npm or yarn
- OpenAI API Key (for ChatGPT integration)

### Running the Frontend

```bash
cd FinVoice/frontend
npm install

# Set up OpenAI API key for ChatGPT integration
cp .env.example .env
# Edit .env file and add your OpenAI API key

npm start
```

The frontend will be available at http://localhost:3000

#### ChatGPT Integration

To use the AI Financial Advisor with ChatGPT:
1. Get an API key from [OpenAI Platform](https://platform.openai.com/)
2. Create a `.env` file in the frontend directory (copy from `.env.example`)
3. Add your API key as `REACT_APP_OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx` (replace with your actual API key)
4. Restart the development server if it's already running

The application uses the latest OpenAI client format with the `responses.create` method and the GPT-5 model.

### Running the Backend

```bash
cd FinVoice/backend
npm install
npm start
```

The backend API will be available at http://localhost:5000

### Running the ML Service

```bash
cd FinVoice/ml_service
pip install -r requirements.txt
python main.py
```

The ML service will be available at http://localhost:8000

## Demo Flow

1. **Voice Input**: Navigate to the Voice Input tab and click "Start Voice Input" (or use the demo buttons)
2. **Add Expense**: Say "Add dinner 300" to log a new expense
3. **View Dashboard**: See your expense reflected in the dashboard charts
4. **Get AI Advice**: Ask the AI advisor about your spending habits
5. **Set Financial Goals**: Create a new financial goal and track your progress

## API Endpoints

### Backend (Express)

- `GET /api/expenses` - Get all expenses
- `POST /api/expenses` - Add a new expense
- `POST /api/expenses/parse-voice` - Parse voice input to extract expense details
- `GET /api/categories` - Get expense categories
- `GET /api/goals` - Get all financial goals
- `POST /api/goals` - Add a new financial goal
- `PATCH /api/goals/:id` - Update goal progress
- `POST /api/goals/calculate-sip` - Calculate SIP for a goal
- `POST /api/advisor` - Get financial advice

### ML Service (FastAPI)

- `POST /categorize` - Categorize an expense
- `POST /parse-voice-input` - Parse voice input
- `POST /financial-advice` - Generate financial advice

## Technologies Used

- **Frontend**: React
- **Backend**: Node.js, Express
- **Database**: Firebase Firestore (with mock data fallback)
- **ML Service**: Python, FastAPI
- **APIs**: OpenAI API, Google Speech-to-Text API

## Deployment

### Frontend

```bash
cd FinVoice/frontend
npm run build
```

Deploy the contents of the `build` folder to a static hosting service like Netlify, Vercel, or Firebase Hosting.

### Backend

Deploy to Heroku:

```bash
cd FinVoice/backend
heroku create
git push heroku main
```

### ML Service

Deploy to Heroku:

```bash
cd FinVoice/ml_service
heroku create
heroku buildpacks:add heroku/python
git push heroku main
```

## Environment Variables

Create a `.env` file in each directory with the following variables:

### Backend

```
PORT=5000
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_DATABASE_URL=your_firebase_database_url
OPENAI_API_KEY=your_openai_api_key
```

### ML Service

```
OPENAI_API_KEY=your_openai_api_key
```

## Hackathon Notes

This project was built for a hackathon in under 5 hours. It demonstrates:

1. Voice-based expense logging
2. AI-powered expense categorization
3. Visual financial dashboards
4. AI financial advisor
5. Goal planning with SIP calculations

The application uses mock data when APIs are not available, making it suitable for demonstration purposes without requiring actual API keys.