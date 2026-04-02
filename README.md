# Mentor Scoring System

## Project Structure

```id="tree123"
.
├── data/
│   ├── mentors.csv
│   ├── students.csv
│   ├── interactions.csv
│   ├── feedbacks.csv
│
├── Engagement.py
├── Responsiveness.py
├── student_progress.py
├── feedback.py
├── main.py
├── requirements.txt
└── mentor_scores.csv
```

---

## Setup Instructions

1. Clone the repository:

   ```
   git clone git@github.com:Yash-debug404/Mentor_feedback_WNCC.git
   cd Mentor_feedback_WNCC
   ```

---

## How to Run

Run main.py script:

```id="run123"
python main.py
```

---

## Output

The program will generate `mentor_scores.csv` in the current directory:

* `mentor_scores.csv` contains:

  * MentorID
  * Name
  * Final Mentor Score
  * Rank
