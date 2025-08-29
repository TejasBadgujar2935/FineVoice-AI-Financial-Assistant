import requests
import json

# Test the ML service endpoints
BASE_URL = "http://localhost:8000"

def test_stock_prediction():
    """Test stock prediction endpoint"""
    try:
        response = requests.post(f"{BASE_URL}/predict-stocks", json={
            "investment_amount": 50000,
            "investment_type": "stocks",
            "timeframe": "1 year"
        })
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Stock Prediction Test PASSED")
            print(f"   Investment: ₹{data['currentValue']:,.0f}")
            print(f"   Predicted Return: {data['predictedReturn']*100:.1f}%")
            print(f"   Predicted Value: ₹{data['predictedValue']:,.0f}")
            print(f"   Confidence: {data['confidence']*100:.0f}%")
            print(f"   Risk Level: {data['riskLevel']}")
            print(f"   Market Sentiment: {data['marketSentiment']}")
            print(f"   Recommendation: {data['recommendation']}")
        else:
            print(f"❌ Stock Prediction Test FAILED: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Stock Prediction Test ERROR: {e}")

def test_gold_prediction():
    """Test gold prediction endpoint"""
    try:
        response = requests.post(f"{BASE_URL}/predict-gold", json={
            "investment_amount": 10000,
            "investment_type": "gold",
            "timeframe": "1 year"
        })
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Gold Prediction Test PASSED")
            print(f"   Investment: ₹{data['currentValue']:,.0f}")
            print(f"   Predicted Return: {data['predictedReturn']*100:.1f}%")
            print(f"   Predicted Value: ₹{data['predictedValue']:,.0f}")
            print(f"   Confidence: {data['confidence']*100:.0f}%")
            print(f"   Risk Level: {data['riskLevel']}")
            print(f"   Market Sentiment: {data['marketSentiment']}")
            print(f"   Recommendation: {data['recommendation']}")
        else:
            print(f"❌ Gold Prediction Test FAILED: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Gold Prediction Test ERROR: {e}")

def test_general_prediction():
    """Test general investment prediction endpoint"""
    try:
        response = requests.post(f"{BASE_URL}/predict-investment", json={
            "investment_amount": 30000,
            "investment_type": "stocks",
            "timeframe": "1 year"
        })
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ General Investment Prediction Test PASSED")
            print(f"   Investment: ₹{data['currentValue']:,.0f}")
            print(f"   Predicted Return: {data['predictedReturn']*100:.1f}%")
            print(f"   Predicted Value: ₹{data['predictedValue']:,.0f}")
        else:
            print(f"❌ General Investment Prediction Test FAILED: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ General Investment Prediction Test ERROR: {e}")

if __name__ == "__main__":
    print("🧪 Testing FinVoice ML Service...")
    print("=" * 50)
    
    # Test if service is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ ML Service is running")
        else:
            print("❌ ML Service is not responding")
            exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to ML Service: {e}")
        print("Make sure the ML service is running on http://localhost:8000")
        exit(1)
    
    # Run tests
    test_stock_prediction()
    test_gold_prediction()
    test_general_prediction()
    
    print("\n" + "=" * 50)
    print("🎉 ML Service testing completed!")
