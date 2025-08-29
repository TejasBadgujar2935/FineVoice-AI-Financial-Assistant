from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import json
from dotenv import load_dotenv
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="FinVoice ML Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define models
class ExpenseText(BaseModel):
    text: str

class Expense(BaseModel):
    description: str
    amount: float
    category: Optional[str] = None

class FinancialData(BaseModel):
    expenses: List[Dict]
    goals: Optional[List[Dict]] = None

class AdviceRequest(BaseModel):
    user_query: str
    financial_data: FinancialData

class InvestmentPredictionRequest(BaseModel):
    investment_amount: float
    investment_type: str  # "stocks" or "gold"
    timeframe: str = "1 year"

# Simple categorization dictionary
categories = {
    "food": ["grocery", "restaurant", "dinner", "lunch", "breakfast", "food", "meal", "snack", "coffee"],
    "travel": ["uber", "lyft", "taxi", "flight", "hotel", "airbnb", "car rental", "gas", "fuel", "train", "bus"],
    "bills": ["rent", "electricity", "water", "internet", "phone", "utility", "insurance", "bill", "subscription"],
    "entertainment": ["movie", "netflix", "spotify", "concert", "game", "entertainment", "music", "show", "theater"],
    "shopping": ["amazon", "clothing", "shoes", "electronics", "furniture", "shopping", "store", "mall"],
    "misc": []
}

class InvestmentPredictor:
    """ML-based investment prediction model"""
    
    def __init__(self):
        # Historical market data patterns (simplified)
        self.stock_historical_data = {
            'nifty50': [15000, 15200, 14800, 15500, 15800, 16200, 15900, 16500, 16800, 17200],
            'sensex': [50000, 50500, 49800, 51200, 51800, 52500, 52200, 53000, 53500, 54000]
        }
        
        self.gold_historical_data = {
            'price_per_gram': [4500, 4550, 4600, 4650, 4700, 4750, 4800, 4850, 4900, 4950]
        }
    
    def predict_stock_returns(self, investment_amount: float, timeframe: str = "1 year") -> Dict:
        """Predict stock market returns using ML model"""
        # Simulate ML model prediction
        # In a real implementation, this would use actual ML models trained on historical data
        
        # Calculate volatility and trend from historical data
        nifty_returns = np.diff(self.stock_historical_data['nifty50']) / self.stock_historical_data['nifty50'][:-1]
        avg_return = np.mean(nifty_returns)
        volatility = np.std(nifty_returns)
        
        # Add some randomness to simulate market uncertainty
        market_sentiment = random.uniform(0.8, 1.2)  # Bullish to bearish sentiment
        
        # Calculate predicted return (annualized)
        base_return = avg_return * 12 * market_sentiment  # Annualize monthly returns
        predicted_return = max(0.05, min(0.25, base_return))  # Cap between 5% and 25%
        
        # Calculate predicted value
        predicted_value = investment_amount * (1 + predicted_return)
        
        # Calculate confidence based on market stability
        confidence = max(0.6, 1 - volatility * 2)
        
        # Determine risk level
        if predicted_return < 0.08:
            risk_level = "Low"
        elif predicted_return < 0.15:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            "current_value": investment_amount,
            "predicted_return": predicted_return,
            "predicted_value": predicted_value,
            "confidence": confidence,
            "timeframe": timeframe,
            "risk_level": risk_level,
            "market_sentiment": "Bullish" if market_sentiment > 1.1 else "Bearish" if market_sentiment < 0.9 else "Neutral",
            "recommendation": self._get_stock_recommendation(predicted_return, confidence)
        }
    
    def predict_gold_returns(self, investment_amount: float, timeframe: str = "1 year") -> Dict:
        """Predict gold returns using ML model"""
        # Simulate ML model prediction for gold
        
        # Calculate gold price trend
        gold_returns = np.diff(self.gold_historical_data['price_per_gram']) / self.gold_historical_data['price_per_gram'][:-1]
        avg_gold_return = np.mean(gold_returns)
        gold_volatility = np.std(gold_returns)
        
        # Gold is generally more stable than stocks
        gold_sentiment = random.uniform(0.9, 1.1)  # More stable sentiment
        
        # Calculate predicted return (annualized)
        base_gold_return = avg_gold_return * 12 * gold_sentiment
        predicted_return = max(0.02, min(0.15, base_gold_return))  # Cap between 2% and 15%
        
        # Calculate predicted value
        predicted_value = investment_amount * (1 + predicted_return)
        
        # Gold has higher confidence due to stability
        confidence = max(0.7, 1 - gold_volatility * 1.5)
        
        return {
            "current_value": investment_amount,
            "predicted_return": predicted_return,
            "predicted_value": predicted_value,
            "confidence": confidence,
            "timeframe": timeframe,
            "risk_level": "Low",
            "market_sentiment": "Stable",
            "recommendation": self._get_gold_recommendation(predicted_return, confidence)
        }
    
    def _get_stock_recommendation(self, predicted_return: float, confidence: float) -> str:
        """Generate stock investment recommendation"""
        if predicted_return > 0.15 and confidence > 0.7:
            return "Strong Buy - High growth potential with good confidence"
        elif predicted_return > 0.10 and confidence > 0.6:
            return "Buy - Good growth potential"
        elif predicted_return > 0.05:
            return "Hold - Moderate growth expected"
        else:
            return "Consider alternatives - Low growth potential"
    
    def _get_gold_recommendation(self, predicted_return: float, confidence: float) -> str:
        """Generate gold investment recommendation"""
        if predicted_return > 0.10 and confidence > 0.8:
            return "Strong Buy - Excellent hedge with good returns"
        elif predicted_return > 0.05 and confidence > 0.7:
            return "Buy - Good hedge against inflation"
        else:
            return "Hold - Stable but low returns"

# Initialize predictor
predictor = InvestmentPredictor()

@app.get("/")
def read_root():
    return {"message": "FinVoice ML Service is running"}

@app.post("/categorize")
def categorize_expense(expense: ExpenseText):
    """Categorize an expense based on its description"""
    text = expense.text.lower()
    
    # Extract amount and description
    words = text.split()
    amount = None
    description = ""
    
    for word in words:
        if word.replace('.', '', 1).isdigit():
            amount = float(word)
        else:
            description += word + " "
    
    description = description.strip()
    
    # If we couldn't extract an amount, check for patterns like "add dinner 300"
    if amount is None:
        for i, word in enumerate(words):
            if i < len(words) - 1 and word.lower() == "add":
                description = words[i+1]
                if i + 2 < len(words) and words[i+2].replace('.', '', 1).isdigit():
                    amount = float(words[i+2])
                    break
    
    # Categorize based on keywords
    category = "misc"  # Default category
    for cat, keywords in categories.items():
        for keyword in keywords:
            if keyword in description:
                category = cat
                break
        if category != "misc":
            break
    
    return {
        "description": description,
        "amount": amount,
        "category": category
    }

@app.post("/parse-voice-input")
def parse_voice_input(expense: ExpenseText):
    """Parse voice input to extract expense details"""
    text = expense.text.lower()
    
    # Simple parsing logic for "add [description] [amount]"
    words = text.split()
    amount = None
    description = ""
    
    # Check for "add" pattern
    if len(words) >= 3 and words[0].lower() == "add":
        description = words[1]
        try:
            amount = float(words[2])
        except ValueError:
            pass
    
    # If the above pattern doesn't match, try to find any number in the text
    if amount is None:
        for word in words:
            if word.replace('.', '', 1).isdigit():
                amount = float(word)
                # Remove the amount from the description
                words.remove(word)
                break
    
    # If we still don't have a description, use all words except "add" and the amount
    if not description:
        description = " ".join([w for w in words if w.lower() != "add" and not w.replace('.', '', 1).isdigit()])
    
    # Categorize the expense
    category = "misc"  # Default category
    for cat, keywords in categories.items():
        for keyword in keywords:
            if keyword in description.lower():
                category = cat
                break
        if category != "misc":
            break
    
    return {
        "description": description.strip(),
        "amount": amount,
        "category": category
    }

@app.post("/financial-advice")
def get_financial_advice(request: AdviceRequest):
    """Generate financial advice based on user query and financial data"""
    # Mock advice responses
    advice_templates = [
        "Based on your spending, you could save {amount} on {category} by reducing expenses by 20%.",
        "I notice you spent {total} on {category} last month. Consider setting a budget of {budget}.",
        "To reach your {goal_name} goal faster, try redirecting {amount} from {category} to savings.",
        "Your spending in {category} is {percentage}% higher than average. Look for ways to reduce these expenses.",
        "Great job keeping your {category} expenses low! You're saving {amount} compared to last month."
    ]
    
    # Extract categories and total spending
    category_totals = {}
    for expense in request.financial_data.expenses:
        category = expense.get("category", "misc")
        amount = expense.get("amount", 0)
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    
    # Find highest spending category
    highest_category = max(category_totals.items(), key=lambda x: x[1]) if category_totals else ("misc", 0)
    
    # Generate advice
    import random
    advice_template = random.choice(advice_templates)
    
    # Fill in template
    advice = advice_template.format(
        category=highest_category[0],
        amount=round(highest_category[1] * 0.2),  # 20% of highest spending
        total=highest_category[1],
        budget=round(highest_category[1] * 0.8),  # 80% of current spending
        goal_name=request.financial_data.goals[0].get("name", "savings") if request.financial_data.goals else "savings",
        percentage=random.randint(15, 30)  # Random percentage for demonstration
    )
    
    return {
        "advice": advice,
        "category_insights": [
            {"category": cat, "amount": amt, "percentage": round(amt / sum(category_totals.values()) * 100) if sum(category_totals.values()) > 0 else 0}
            for cat, amt in category_totals.items()
        ]
    }

@app.post("/predict-investment")
def predict_investment(request: InvestmentPredictionRequest):
    """Predict investment returns using ML models"""
    try:
        if request.investment_type.lower() == "stocks":
            prediction = predictor.predict_stock_returns(request.investment_amount, request.timeframe)
        elif request.investment_type.lower() == "gold":
            prediction = predictor.predict_gold_returns(request.investment_amount, request.timeframe)
        else:
            raise HTTPException(status_code=400, detail="Invalid investment type. Use 'stocks' or 'gold'")
        
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict-stocks")
def predict_stocks(request: InvestmentPredictionRequest):
    """Predict stock market returns"""
    try:
        prediction = predictor.predict_stock_returns(request.investment_amount, request.timeframe)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stock prediction failed: {str(e)}")

@app.post("/predict-gold")
def predict_gold(request: InvestmentPredictionRequest):
    """Predict gold returns"""
    try:
        prediction = predictor.predict_gold_returns(request.investment_amount, request.timeframe)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gold prediction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)