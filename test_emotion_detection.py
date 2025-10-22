# test_emotion_detection.py [Task 5]
import unittest
from EmotionDetection import emotion_detector

class TestEmotionDetection(unittest.TestCase):
    """Test cases for emotion_detector function"""
    def test_dominant_emotions(self):
        """Check that correct dominant emotion is returned per test sentence"""
        cases = [
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear"),
        ]
        for text, expected in cases:
            with self.subTest(text=text, expected=expected):
                result = emotion_detector(text)
                # Basic structure checks
                self.assertIn("dominant_emotion", result, "Result missing 'dominant_emotion'")
                self.assertIn("anger", result)
                self.assertIn("disgust", result)
                self.assertIn("fear", result)
                self.assertIn("joy", result)
                self.assertIn("sadness", result)
                # Expected dominant emotion
                self.assertEqual(result["dominant_emotion"], expected)

if __name__ == "__main__":
    unittest.main(verbosity=2) # verbosity=2 prints test’s name, docstring and result [https://docs.python.org/3/library/unittest.html]