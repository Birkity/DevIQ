import csv
from collections import Counter

def analyze_feedback(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        feedback_data = list(reader)

    # Extract ratings and feedback
    ratings = [int(row[2]) for row in feedback_data if row[2].isdigit()]
    feedback_texts = [row[3] for row in feedback_data]

    # Calculate average rating
    average_rating = sum(ratings) / len(ratings) if ratings else 0

    # Find common feedback themes
    feedback_counter = Counter(feedback_texts)
    common_feedback = feedback_counter.most_common(5)

    # Output results to a file
    with open('feedback_analysis.txt', 'w') as f:
        f.write(f"Average Rating: {average_rating}\n")
        f.write("Common Feedback Themes:\n")
        for feedback, count in common_feedback:
            f.write(f"- {feedback} ({count} times)\n")

    return average_rating, common_feedback

if __name__ == "__main__":
    analyze_feedback('feedback.csv') 