import csv
import os
import json
from collections import Counter

FEEDBACK_FILE = "feedback.csv"
ANALYSIS_FILE = "feedback_analysis.json"

def analyze_feedback():
    """Analyze feedback data and store results in a JSON file."""
    try:
        # Ensure the feedback file exists
        if not os.path.exists(FEEDBACK_FILE):
            print("Feedback file does not exist. Skipping analysis.")
            return

        with open(FEEDBACK_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            feedback_data = list(reader)

        # Check if there's actual data (excluding header)
        if len(feedback_data) <= 1:
            print("No feedback data found. Skipping analysis.")
            return

        # Extract ratings and feedback text (skip the header row)
        ratings = []
        feedback_texts = []

        for row in feedback_data[1:]:  # Skip header
            if len(row) < 4:
                continue  # Skip incomplete rows
            
            # Extract rating
            try:
                rating = int(row[2])
                ratings.append(rating)
            except ValueError:
                continue  # Skip invalid ratings

            # Extract feedback text
            feedback_text = row[3].strip().lower()
            if feedback_text:
                feedback_texts.append(feedback_text)

        # Calculate average rating
        average_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

        # Identify common feedback themes
        feedback_counter = Counter(feedback_texts)
        common_feedback = feedback_counter.most_common(5)

        # Save analysis results to JSON
        analysis_results = {
            "average_rating": average_rating,
            "common_feedback": [{"feedback": fb, "count": count} for fb, count in common_feedback]
        }

        with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
            json.dump(analysis_results, f, indent=4)

        print("✅ Feedback Analysis Completed. Data Saved.")

    except Exception as e:
        print(f"❌ Error analyzing feedback: {e}")

def ensure_analysis_file():
    if not os.path.exists(ANALYSIS_FILE):
        with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
            json.dump({"average_rating": 0, "common_feedback": []}, f, indent=4)

if __name__ == "__main__":
    ensure_analysis_file()
    analyze_feedback()
