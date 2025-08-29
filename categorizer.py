import re
from typing import Dict, List, Tuple

class ExpenseCategorizer:
    """Simple rule-based expense categorizer"""
    
    def __init__(self):
        # Define category keywords
        self.categories = {
            "food": ["grocery", "restaurant", "dinner", "lunch", "breakfast", "food", "meal", "snack", "coffee", "pizza", "burger"],
            "travel": ["uber", "lyft", "taxi", "flight", "hotel", "airbnb", "car rental", "gas", "fuel", "train", "bus", "travel"],
            "bills": ["rent", "electricity", "water", "internet", "phone", "utility", "insurance", "bill", "subscription"],
            "entertainment": ["movie", "netflix", "spotify", "concert", "game", "entertainment", "music", "show", "theater", "streaming"],
            "shopping": ["amazon", "clothing", "shoes", "electronics", "furniture", "shopping", "store", "mall", "online"],
            "health": ["doctor", "medicine", "pharmacy", "hospital", "clinic", "health", "medical", "fitness", "gym"],
            "education": ["book", "course", "tuition", "school", "college", "university", "education", "learning"],
            "misc": []
        }
    
    def categorize(self, description: str) -> str:
        """Categorize an expense based on its description"""
        description = description.lower()
        
        # Check each category's keywords
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in description:
                    return category
        
        # Default to misc if no match found
        return "misc"
    
    def parse_voice_input(self, text: str) -> Tuple[str, float, str]:
        """Parse voice input to extract expense details"""
        text = text.lower()
        
        # Extract amount using regex
        amount_match = re.search(r'\b(\d+(?:\.\d+)?)\b', text)
        amount = float(amount_match.group(1)) if amount_match else None
        
        # Extract description
        # Remove "add" and amount from text to get description
        description = text
        if "add" in description:
            description = description.replace("add", "", 1).strip()
        if amount_match:
            description = description.replace(amount_match.group(1), "", 1).strip()
        
        # Categorize the expense
        category = self.categorize(description)
        
        return description, amount, category
    
    def get_all_categories(self) -> List[str]:
        """Return all available categories"""
        return list(self.categories.keys())
    
    def get_category_keywords(self) -> Dict[str, List[str]]:
        """Return all category keywords"""
        return self.categories

# Example usage
if __name__ == "__main__":
    categorizer = ExpenseCategorizer()
    
    # Test categorization
    test_expenses = [
        "dinner at restaurant",
        "uber ride",
        "netflix subscription",
        "amazon purchase",
        "doctor visit"
    ]
    
    for expense in test_expenses:
        category = categorizer.categorize(expense)
        print(f"Expense: {expense} -> Category: {category}")
    
    # Test voice input parsing
    test_inputs = [
        "add dinner 300",
        "add taxi 150",
        "add netflix 199"
    ]
    
    for input_text in test_inputs:
        description, amount, category = categorizer.parse_voice_input(input_text)
        print(f"Input: {input_text} -> Description: {description}, Amount: {amount}, Category: {category}")