from .textprocessor import TextProcessor
from .zero_shot_classification import ZeroShotAnalyzer
from .bias_detection import BiasDetector
from .specificity_analyzer import SpecificityAnalyzer
from .recommendation_engine import RecommendationEngine
from .vectorstore import VectorStore
from .feedbacktype import FeedbackTypeAnalyzer
import re

class PerformanceReviewAnalyzer:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.zero_shot = ZeroShotAnalyzer()
        self.feedback_type = FeedbackTypeAnalyzer(self.zero_shot)
        self.bias_detector = BiasDetector(self.zero_shot)
        self.specificity_analyzer = SpecificityAnalyzer(self.zero_shot)
        self.vectorstore = VectorStore(host="localhost", port=8000)

    def analyze(self, review_text, objectives=None):
        if not review_text.strip():
            return {
                "error": "No review text provided"
            }

        # Process text
        processed = self.text_processor.preprocess(review_text)

        # Check alignment with objectives if provided
        objective_alignment = None

        # Combine all analysis results
        analysis_results = {
            "biases": self.bias_detector.detect_bias(processed),
            "specificities": self.specificity_analyzer.analyze_specificity(processed),
            "feedbacks": self.feedback_type.feedback_type(processed),
            "objectives": objective_alignment
        }

        # Generate recommendations
        recommender = RecommendationEngine(analysis_results)
        recommendations = {
            "bias": recommender.generate_table_bias(),
            "specificity": recommender.generate_table_specificity(),
            "feedback": recommender.generate_table_feedback()
        }

        return {
            "analysis": analysis_results,
            "recommendations": recommendations
        }

