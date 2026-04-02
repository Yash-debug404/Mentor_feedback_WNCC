# Ideation Document – Mentor Scoring System

## 1. Overview

The scoring system scores mentors using four parameters:

* Student Progress (P)
* Responsiveness (R)
* Engagement (E)
* Feedback (F)

The final score is a weighted sum:

M(m) = 0.3P + 0.275R + 0.275E + 0.15F

---

## 2. Student Progress Score (P)

For each student:

p = MilestonesCompleted / TotalMilestones

Each mentor’s score is the **average progress of their mentees**.

### Reasoning:

* For each student, p is computed as a ratio to ensure uniformity across mentees with different project sizes.
* Averaging ensures fairness across mentors with different mentee counts

---

## 3. Engagement Score (E)

Engagement is computed using three signals:

* Code Reviews (C)
* Meetings (M)
* Messages (Msg)

### Saturation Function

Each component uses a logarithmic saturation:

S(x) = log(1 + x) / (log(1 + x) + k)

Where k is a constant specific to each activity:

* Code Reviews → k = log(1 + 3)
* Meetings → k = log(1 + 5)
* Messages → k = log(1 + 32)
* Saturation is done to prevent mentors from gaming the system by excessive low quality interaction
* S(x)=0.5 for x=k,hence k is choosen to represent typical(median like) expected level of that activity

### Combined Engagement

E_raw = 0.45·C + 0.35·M + 0.2·Msg

* E_raw is calculated for each mentee

Final score is:

E = max(0, mean − 0.5·std)

* Where mean is mean of E_raw over all mentees and std is the standard deviation.

### Reasoning:

* Saturation ensures diminishing returns, preventing excessive activity from being over-rewarded.
* (mean - 0.5*std) penalizes inconsistency, rewarding mentors who perform uniformly well across all mentees.

---

## 4. Responsiveness Score (R)

Response time t for a mentor with a particular mentee is mapped to R_raw:

R_raw = sin^2( (π/2) / ( (t/12)^2 + 1 ) )

### Properties:

* Fast response → value close to 1
* Very slow responses are heavily penalized
* Smooth and bounded in [0,1]

Final aggregation:

R = max(0, mean − 0.5·std)

* Where mean is the mean of R_raw over all mentees of the mentor,and std is the standard deviation.

### Reasoning:

* The function is designed such that:
    * R(0) = 1 and R(t) → 0 as t → ∞
    * The derivative is small for both very low and very high values of time,so that   the scores of mentors responding close to zero doesn't change much. 
* There is a strong penalty beyond ~12 hours (chosen as a critical threshold, inflection point is close to 12)
* Sample values:
  * R(6) ≈ 0.9
  * R(12) ≈ 0.5
  * R(16) ≈ 0.28
  * R(24) ≈ 0.09
* This ensures that response times beyond 12 hours are significantly penalized.
* (mean − 0.5·std) penalizes inconsistency, rewarding mentors who respond uniformly across mentees.

---

## 5. Feedback Score (F)

### Step 1: Z-score based weighting

For each rating r:

z = (r − mean) / (std + 0.01)

Weight:

w = 1 / (1 + max(0, |z| − 2))

### Step 2: Weighted Average

F_raw = weighted mean of r with weight w.

The resulting value (originally in the range [1, 5]) is then scaled to [0, 1].

### Step 3: Bayesian Adjustment

F = p·F_raw + q·R0

Where:

* p = n / (n + k)
* q = k / (n + k)
* k = 5
* R0 = 0.5

### Reasoning:

* Z is calculated to reduce the weight of ratings that deviate significantly(2*times more than the standard deviation)from the mean.
* Bayesian smoothing ensures that when the number of ratings is small, the feedback is not overly trusted and is pulled toward a neutral prior (R₀ = 0.5).
* As the number of ratings increases, the system places more trust in the observed feedback.

---

## 6. Final Score Weights

* P = 0.3 → Outcome (important but not dominant)
* R = 0.275 → Responsiveness
* E = 0.275 → Engagement
* F = 0.15 → Feedback (subjective, hence lower weight)

### Justification:

Higher weights are assigned almost equally across objective metrics (P, E, R), with a lower weight assigned to subjective feedback (F).

---

## 7. Normalization Across Mentors

* Progress is ratio-based and final score is averaged.
* Engagement is calculated over all activities per mentee as a single index E_raw which is then averaged over all mentees of the mentor.
* Feedback uses Bayesian scaling to ensure that the feedback is not fully trusted when the number of rating is small and lower weights are assigned to ratings that deviate significantly from the mean.
* No metric depends on absolute counts

---

## 8. Key Design Choices

* Logarithmic saturation to prevent excess activity from being over rewarding
* Variance penalty to enforce consistency
* Smooth response time function ensuring fair scoring for mentors.
* Bias-resistant feedback aggregation.

---


## 9. Score Evolution Over Time

Mentor performance may vary across evaluation periods. To account for this, we use exponential smoothing:

Mₜ₊₁ = (1 − α)·Mₜ + α·M_current

Where:

* α = 0.3

### Reasoning:

* Giving 70% to historical performances , 30% to current week , prevents a single bad week from tanking a good mentor's score.
* This also prevents a good week from inflating a consistently bad mentor.
* At the same time, recent performance is still incorporated, allowing the score to adapt gradually.
* This creates a stable yet responsive scoring system.

---

## 10. Activity Decay

If a mentor has no interaction for two consecutive evaluation periods, a decay is applied:

M_new = M_old · (1 − d)

Where:

* d = 0.15

### Reasoning:

* A decay rate of 15% ensures that inactive mentors are gradually penalized without abrupt drops.
* After 2 inactive weeks → score becomes ~72% of original
* After 4 inactive weeks → score becomes ~52% of original
* This discourages inactivity while still allowing mentors to recover their score upon re-engagement.
* A heigher d like 0.5 is too aggressive , a mentor who was excellent throughout months shouldn't drop to half score after 2 quiet weeks

---


## 11. Assumptions

* Interaction data is reliable
* Feedback contains noise but not extreme corruption

---

## 12. Conclusion

The system ensures:

* Fair comparison across mentors
* Resistance to manipulation
* Balanced evaluation of outcome, effort, and perception.

