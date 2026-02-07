# classifier.py
from sentence_transformers import SentenceTransformer
import numpy as np

class EmailClassifier:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.categories = {
            "urgent": "This requires immediate attention and quick response",
            "support": "Customer needs help with a technical problem",
            "sales": "Sales inquiry or business opportunity",
            "meeting": "Meeting request or scheduling",
            "spam": "Promotional or unwanted content"
        }
        
        self.embeddings = {
            cat: self.model.encode(desc)
            for cat, desc in self.categories.items()
        }
    
    def classify(self, email_text):
        email_embedding = self.model.encode(email_text)
        
        scores = {}
        for category, cat_embedding in self.embeddings.items():
            similarity = np.dot(email_embedding, cat_embedding) / (
                np.linalg.norm(email_embedding) * np.linalg.norm(cat_embedding)
            )
            scores[category] = similarity
        
        return max(scores, key=scores.get), scores