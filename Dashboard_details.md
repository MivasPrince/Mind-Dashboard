# MIND Dashboard - Complete Features & Use Cases Guide

## **Table of Contents**

1. [Executive Overview](#executive-overview)
2. [Student Dashboard](#student-dashboard)
3. [Faculty Dashboard](#faculty-dashboard)
4. [Developer Dashboard](#developer-dashboard)
5. [Admin Dashboard](#admin-dashboard)
6. [Cross-Dashboard Insights](#cross-dashboard-insights)

---

## **Executive Overview**

### **What is the MIND Dashboard?**

The MIND Unified Analytics Dashboard is a comprehensive data analytics platform designed for Miva Open University's MIND solution. It provides real-time insights into student performance, learning outcomes, system health, and institutional effectiveness across four specialized dashboards.

### **Dashboard Summary**

| Dashboard | Target Users | Primary Purpose | Key Metrics |
|-----------|-------------|-----------------|-------------|
| **Student** | Individual learners | Personal progress tracking | 8 KPIs, 5 charts |
| **Faculty** | Instructors, educators | Cohort management & assessment | 8 KPIs, 6 charts, 4 tables |
| **Developer** | Technical staff, IT | System health monitoring | 8 KPIs, 10 charts, 4 tables |
| **Admin** | Leadership, executives | Institution-wide analytics | 12 KPIs, 8 charts, 4 tables |

### **Platform-Wide Capabilities**

- **Real-time Analytics:** Live data updates with dynamic filtering
- **Role-Based Access:** Secure authentication with appropriate permissions
- **Export Functionality:** CSV downloads for all data tables
- **Interactive Visualizations:** 20+ Plotly charts with hover details
- **Multi-dimensional Filtering:** By cohort, department, campus, time period
- **Comprehensive Coverage:** Student performance, system health, environment quality

---

# **Student Dashboard**

## **Overview**

The Student Dashboard provides individuals with personalized insights into their learning journey, performance trends, and improvement opportunities. It helps students understand their strengths, identify areas for growth, and track progress over time.

### **Who Uses It:**
- Individual students
- Self-directed learners
- Students seeking performance insights

### **Primary Goals:**
1. Track personal performance over time
2. Identify improvement between attempts
3. Understand rubric-based feedback
4. Monitor engagement patterns
5. Optimize study habits

---

## **Key Performance Indicators (8 KPIs)**

### **1. Total Attempts**

**What it tracks:** Total number of case study attempts completed by the student

**Calculation:** `COUNT(attempts WHERE student_id = current_student)`

**Why it's useful:**
- Measures engagement level with the platform
- Indicates learning activity volume
- Higher numbers show consistent practice
- Helps assess time investment in learning

**Interpretation:**
- **High (10+):** Active, engaged learner
- **Medium (5-10):** Moderate engagement
- **Low (<5):** May need motivation or support

**Actionable Insights:**
- Low attempts? Set weekly goals for case study completion
- Compare with cohort average to gauge participation level

---

### **2. Average Score**

**What it tracks:** Mean performance score across all attempts (0-100%)

**Calculation:** `AVG(score) FROM all student attempts`

**Why it's useful:**
- Primary indicator of academic performance
- Shows overall competency level
- Benchmark for improvement goals
- Reflects mastery of learning objectives

**Interpretation:**
- **Excellent (80-100%):** Strong grasp of concepts
- **Good (70-79%):** Solid understanding
- **Fair (60-69%):** Basic competency, room for improvement
- **Needs Work (<60%):** Requires additional study/support

**Actionable Insights:**
- Below 70%? Review rubric feedback for common weaknesses
- Compare attempt 1 vs attempt 2 scores to see learning curve

---

### **3. Best Score**

**What it tracks:** Highest score achieved on any single attempt

**Calculation:** `MAX(score) FROM all student attempts`

**Why it's useful:**
- Shows peak performance capability
- Motivational indicator of potential
- Demonstrates what student can achieve
- Benchmark for consistency goals

**Interpretation:**
- Gap between best and average indicates consistency
- High best score (90+) with low average suggests inconsistency
- Consistently near best score shows reliable performance

**Actionable Insights:**
- Best score much higher than average? Work on consistency
- Use conditions from best attempt (time, environment) as model

---

### **4. Total Time Spent**

**What it tracks:** Cumulative time spent on all case studies (hours)

**Calculation:** `SUM(duration_seconds) / 3600 FROM all attempts`

**Why it's useful:**
- Measures time investment in learning
- Helps assess study habits
- Correlates time with performance outcomes
- Identifies efficient vs inefficient learners

**Interpretation:**
- **High time + High scores:** Thorough, diligent learner
- **High time + Low scores:** May need study strategy help
- **Low time + High scores:** Efficient learner
- **Low time + Low scores:** Under-engaged

**Actionable Insights:**
- Low time spent? May need to invest more in preparation
- High time with low scores? Seek tutoring or study strategy support
- Compare time-per-attempt with high performers

---

### **5. Average Improvement**

**What it tracks:** Mean score gain from Attempt 1 to Attempt 2 (percentage points)

**Calculation:** `AVG(attempt_2_score - attempt_1_score) WHERE student has both attempts`

**Why it's useful:**
- **Key indicator of learning effectiveness**
- Shows student's ability to learn from feedback
- Measures growth mindset and adaptability
- Validates the value of retry opportunities

**Interpretation:**
- **Strong improvement (>10 points):** Excellent learning from feedback
- **Moderate improvement (5-10 points):** Good learning curve
- **Minimal improvement (<5 points):** May not be applying feedback
- **Negative improvement:** Possible test anxiety or inconsistency

**Actionable Insights:**
- No improvement? Review rubric feedback more carefully before retry
- Strong improvement? Approach is working, continue pattern
- Share improvement strategies with peers

---

### **6. Completion Rate**

**What it tracks:** Percentage of started attempts that were completed (not abandoned)

**Calculation:** `(Completed attempts / Total attempts) × 100`

**Why it's useful:**
- Indicates persistence and follow-through
- Reflects technical issues or user experience problems
- Shows commitment level
- Predicts exam/assignment completion likelihood

**Interpretation:**
- **Excellent (90-100%):** Strong commitment, rare technical issues
- **Good (80-89%):** Generally completes work
- **Fair (70-79%):** Occasionally abandons attempts
- **Low (<70%):** Frequent incompletions, needs investigation

**Actionable Insights:**
- Low completion rate? Check for technical issues or time management
- Identify patterns: certain case studies more likely abandoned?
- Set completion goals before starting attempts

---

### **7. Cases Attempted**

**What it tracks:** Number of unique case studies the student has worked on

**Calculation:** `COUNT(DISTINCT case_id) FROM student attempts`

**Why it's useful:**
- Shows breadth of exposure to curriculum
- Indicates coverage of learning objectives
- Measures curriculum engagement diversity
- Helps ensure well-rounded learning

**Interpretation:**
- **Full coverage:** Attempted all available cases
- **Partial coverage:** Selective or still progressing
- **Narrow coverage:** May be focusing on easier cases

**Actionable Insights:**
- Not attempted all cases? Create schedule to cover remaining content
- Compare with required cases for course completion
- Identify if avoiding difficult topics

---

### **8. Average CES (Customer Effort Score)**

**What it tracks:** Self-reported ease of use rating (0-100)

**Calculation:** `AVG(ces_value) FROM all student attempts`

**Why it's useful:**
- **User experience indicator**
- Shows perceived difficulty vs actual difficulty
- Identifies usability issues
- Predicts platform adoption and satisfaction

**Interpretation:**
- **High CES (80-100):** Platform is easy to use
- **Medium CES (60-79):** Generally usable
- **Low CES (<60):** Significant usability issues

**Actionable Insights:**
- Low CES? Report technical difficulties to support
- High difficulty but high scores? Strong learner despite UX
- Low difficulty but low scores? Content issue vs technical issue

---

## **📈 Performance Visualizations (5 Charts)**

### **1. Score Trend Over Time**

**Chart Type:** Line chart

**What it shows:** Performance scores plotted chronologically

**Data Points:**
- X-axis: Attempt timestamp (date)
- Y-axis: Score percentage
- Line: Continuous trend of performance

**Why it's useful:**
- **Visualizes learning trajectory**
- Shows performance consistency or variability
- Identifies improvement trends or plateaus
- Reveals seasonal performance patterns

**How to interpret:**
- **Upward trend:** Improving, learning is working
- **Flat line:** Plateau, may need new strategies
- **Downward trend:** Declining performance, needs intervention
- **Zig-zag pattern:** Inconsistent performance

**Actionable Insights:**
- Declining trend? Take a break or seek help
- Plateau? Try new study techniques
- Upward trend? Current approach is working, continue
- Look for correlation with external factors (exams, work stress)

---

### **2. Improvement: Attempt 1 vs 2**

**Chart Type:** Bar chart (can show positive/negative values)

**What it shows:** Score change between first and second attempts per case study

**Data Points:**
- X-axis: Case study titles
- Y-axis: Score improvement (+ or - points)
- Color: Green for positive, red for negative

**Why it's useful:**
- **Measures learning from feedback**
- Shows which cases benefited most from retry
- Identifies cases where feedback wasn't helpful
- Validates learning loop effectiveness

**How to interpret:**
- **Positive bars:** Learning occurred between attempts
- **Negative bars:** Performance declined on retry
- **Tall positive bars:** Excellent learning on specific topics
- **Minimal change:** May not be reviewing feedback

**Actionable Insights:**
- Large improvements? Note what you did differently
- Negative improvements? Review approach to retries
- Some cases improve, others don't? Topic-specific study needed
- No improvement anywhere? Schedule feedback review session

---

### **3. Rubric Dimension Mastery**

**Chart Type:** Horizontal bar chart

**What it shows:** Performance across three assessment dimensions

**Data Points:**
- Y-axis: Rubric dimensions (Evidence-Based Reasoning, Communication, Analysis)
- X-axis: Average mastery percentage (0-100%)
- Bars: Horizontal bars showing strength in each dimension

**Why it's useful:**
- **Identifies specific skill strengths and weaknesses**
- Goes beyond overall score to skill-specific feedback
- Guides targeted improvement efforts
- Shows which competencies are mastered

**Dimensions Explained:**

**Evidence-Based Reasoning (40%):**
- Ability to support claims with data
- Use of research and clinical evidence
- Quality of source citations
- Logical argumentation

**Communication (30%):**
- Clarity of expression
- Professional writing style
- Organization and structure
- Audience-appropriate language

**Analysis (30%):**
- Critical thinking depth
- Problem-solving approach
- Synthesis of information
- Clinical reasoning quality

**How to interpret:**
- **Balanced bars:** Well-rounded competency
- **One strong dimension:** Natural strength, but others need work
- **One weak dimension:** Clear improvement target
- **All low (<60%):** Need comprehensive support

**Actionable Insights:**
- Weak in Evidence? Practice citing sources, research more
- Weak in Communication? Get writing tutoring, review examples
- Weak in Analysis? Practice critical thinking exercises
- Strong everywhere? Help peers, seek advanced challenges

---

### **4. Engagement by Action Type**

**Chart Type:** Pie chart

**What it shows:** Distribution of student activity types

**Data Points:**
- Slices: Different action types (Reading, Video watching, Case work, Testing, etc.)
- Percentages: Proportion of time spent on each activity
- Colors: Different color per activity type

**Why it's useful:**
- **Reveals study behavior patterns**
- Shows time allocation across activities
- Identifies if student is using all resources
- Helps optimize study strategy

**Common Action Types:**
- **Case Study Work:** Primary learning activity
- **Reading:** Consuming text materials
- **Video Review:** Watching instructional content
- **Assessment:** Taking tests/quizzes
- **Feedback Review:** Examining rubric scores

**How to interpret:**
- **Heavily skewed:** Over-reliance on one activity type
- **Balanced distribution:** Using diverse learning resources
- **Low case work %:** Not enough practice
- **High feedback review %:** Good reflection habits

**Actionable Insights:**
- Too much reading, not enough practice? Balance activities
- No video engagement? May be missing key content
- Low feedback review? Missing learning opportunities
- Compare with high-performing peers' patterns

---

### **5. Daily Engagement Activity**

**Chart Type:** Line chart

**What it shows:** Daily engagement duration over time (typically 30 days)

**Data Points:**
- X-axis: Dates
- Y-axis: Total engagement time (seconds or minutes)
- Line: Daily activity level

**Why it's useful:**
- **Tracks engagement consistency**
- Shows study habit patterns
- Identifies peak productivity times
- Reveals gaps in engagement

**How to interpret:**
- **Consistent daily activity:** Disciplined study habits
- **Weekend spikes:** Cramming behavior
- **Long gaps:** Disengagement periods
- **Declining trend:** Losing motivation

**Actionable Insights:**
- Inconsistent engagement? Set daily study schedule
- Weekend cramming? Distribute study more evenly
- Long gaps? Re-engage with easier content
- Evening spikes? That's your peak learning time, protect it

---

## **How Students Use This Dashboard**

### **Weekly Check-in Routine:**

1. **Review KPIs:** Check average score, improvement, completion rate
2. **Analyze trends:** Look at score trend over time for patterns
3. **Identify weak dimensions:** Use rubric mastery chart to target study
4. **Optimize engagement:** Review engagement patterns, adjust schedule
5. **Set goals:** Based on data, set specific improvement targets

### **Before Exams:**

1. Check cases attempted - ensure full curriculum coverage
2. Review improvement chart - identify weak topics
3. Note best scores - understand what conditions lead to success
4. Check rubric dimensions - focus final study on weakest dimension

### **After Receiving Grades:**

1. Compare actual vs predicted performance
2. Analyze what worked - correlate study patterns with outcomes
3. Adjust strategy for next period
4. Share successful approaches with peers

---

# **Faculty Dashboard**

## **Overview**

The Faculty Dashboard provides instructors with comprehensive insights into cohort performance, learning outcomes, and teaching effectiveness. It enables data-driven decisions about curriculum, assessment, and student support.

### **Who Uses It:**
- Course instructors
- Academic advisors
- Department heads
- Teaching assistants

### **Primary Goals:**
1. Monitor cohort-wide performance
2. Identify at-risk students early
3. Evaluate case study effectiveness
4. Track learning objective achievement
5. Inform instructional adjustments

---

## **📊 Key Performance Indicators (8 KPIs)**

### **1. Total Students**

**What it tracks:** Total number of students in filtered cohort/department

**Calculation:** `COUNT(DISTINCT students) matching filter criteria`

**Why it's useful:**
- Contextualizes all other metrics
- Shows cohort size for statistical validity
- Helps with resource planning
- Indicates class load

**Interpretation:**
- Large cohorts (100+): Need scalable interventions
- Small cohorts (<20): Can provide individualized attention
- Declining numbers: Potential retention issue

**Actionable Insights:**
- Large cohort with poor performance? Need systemic interventions
- Small cohort? Can implement personalized teaching strategies

---

### **2. Active Students**

**What it tracks:** Students who have completed at least one attempt in the filtered time period

**Calculation:** `COUNT(DISTINCT students with attempts) in date range`

**Why it's useful:**
- **Engagement indicator**
- Distinguishes enrolled vs participating students
- Early warning for disengagement
- Validates course relevance

**Interpretation:**
- **High activity (80-100%):** Strong engagement
- **Medium activity (60-79%):** Some disengagement
- **Low activity (<60%):** Significant engagement problem

**Actionable Insights:**
- Low active rate? Send engagement reminders, check barriers
- Compare with assignment due dates
- Inactive students? Reach out individually

---

### **3. Average Score**

**What it tracks:** Mean score across all attempts in cohort

**Calculation:** `AVG(scores) FROM all cohort attempts`

**Why it's useful:**
- **Primary learning outcomes measure**
- Indicates teaching effectiveness
- Benchmark for curriculum difficulty
- Grading fairness validator

**Interpretation:**
- **High average (80-90%):** Effective teaching or easy content
- **Moderate average (70-79%):** Appropriate challenge
- **Low average (<70%):** Content too hard or teaching issue

**Actionable Insights:**
- Low average? Review teaching methods, case difficulty
- Very high average? Content may be too easy, lack challenge
- Compare with previous cohorts for trends

---

### **4. Average Improvement**

**What it tracks:** Mean score gain from attempt 1 to attempt 2 across cohort

**Calculation:** `AVG(attempt_2 - attempt_1) for all students`

**Why it's useful:**
- **Feedback effectiveness measure**
- Shows if rubric guidance is helpful
- Validates formative assessment approach
- Indicates learning loop quality

**Interpretation:**
- **Strong improvement (>10 points):** Feedback is effective
- **Moderate improvement (5-10 points):** Decent learning
- **Minimal improvement (<5 points):** Feedback not helpful
- **Negative improvement:** Assessment inconsistency issue

**Actionable Insights:**
- No improvement? Revise rubric feedback quality
- Strong improvement? Share feedback approach with colleagues
- Some cases improve, others don't? Case-specific feedback issue

---

### **5. Completion Rate**

**What it tracks:** Percentage of started attempts that were completed

**Calculation:** `(Completed / Total attempts) × 100`

**Why it's useful:**
- User experience indicator
- Technical issue detector
- Engagement quality measure
- Assignment design validator

**Interpretation:**
- **High (90-100%):** Good UX, appropriate difficulty
- **Medium (80-89%):** Some abandonment
- **Low (<80%):** Serious UX or difficulty issues

**Actionable Insights:**
- Low completion? Survey students about barriers
- Check which cases have lowest completion
- Investigate technical issues vs difficulty

---

### **6. Students At Risk**

**What it tracks:** Number of students with average scores below 60%

**Calculation:** `COUNT(students WHERE avg_score < 60)`

**Why it's useful:**
- **Early intervention trigger**
- Identifies struggling learners
- Prevents failures
- Resource allocation guide

**Interpretation:**
- **No at-risk students:** Cohort doing well
- **Few at-risk (<10%):** Normal distribution
- **Many at-risk (>20%):** Systemic problem

**Actionable Insights:**
- At-risk students? Implement support program immediately
- Review at-risk students' rubric patterns for common issues
- Pair with high-performing peers for tutoring

---

### **7. Average CES**

**What it tracks:** Mean customer effort score (user experience rating)

**Calculation:** `AVG(ces_value) FROM cohort attempts`

**Why it's useful:**
- Platform usability feedback
- Student satisfaction indicator
- Technical issue detector
- Predicts platform adoption

**Interpretation:**
- **High (75-100):** Good user experience
- **Medium (60-74):** Acceptable usability
- **Low (<60):** Significant UX problems

**Actionable Insights:**
- Low CES? Report to IT/platform team
- Check if CES correlates with scores (low CES + low scores = UX hurting learning)
- Survey students about specific pain points

---

### **8. Average Time on Task**

**What it tracks:** Mean time spent per attempt

**Calculation:** `AVG(duration_seconds) / 60 FROM cohort attempts`

**Why it's useful:**
- Case study difficulty indicator
- Workload assessment
- Efficiency measure
- Pacing guide

**Interpretation:**
- **High time:** Complex cases or struggling students
- **Moderate time:** Appropriate difficulty
- **Low time:** Too easy or rushing

**Actionable Insights:**
- Very high time? Case may be too complex or unclear
- Very low time? Students may be rushing, consider minimums
- Compare time vs scores - should correlate positively

---

## **📊 Performance Analytics (6 Charts)**

### **1. Score Distribution by Case Study**

**Chart Type:** Bar chart

**What it shows:** Average score for each case study

**Data Points:**
- X-axis: Case study titles
- Y-axis: Average scores (0-100%)
- Bars: Color-coded by score level

**Why it's useful:**
- **Identifies difficult vs easy cases**
- Reveals curriculum balance
- Shows which content needs revision
- Validates learning objective alignment

**How to interpret:**
- **Consistent scores across cases:** Well-balanced curriculum
- **One case much lower:** That case needs review
- **One case much higher:** May be too easy or familiar
- **Wide variance:** Inconsistent difficulty

**Actionable Insights:**
- Low-scoring case? Add scaffolding, clearer instructions
- High-scoring case? Increase complexity or depth
- Pattern of low scores early? Need prerequisite review
- All cases similar difficulty? Good curriculum design

---

### **2. Performance by Department**

**Chart Type:** Colored bar chart with gradient

**What it shows:** Average scores by academic department

**Data Points:**
- X-axis: Department names (Nursing, Medicine, Pharmacy, etc.)
- Y-axis: Average scores
- Color: Gradient based on performance level

**Why it's useful:**
- **Inter-departmental comparison**
- Resource allocation guide
- Identifies high/low-performing groups
- Reveals program-specific needs

**How to interpret:**
- **Similar performance:** Consistent quality across departments
- **One department significantly lower:** Needs targeted support
- **One department significantly higher:** Share their best practices

**Actionable Insights:**
- Low-performing department? Investigate: teaching quality, resources, prerequisites
- High-performing department? Document and share successful practices
- Large gaps? May indicate inequitable resource distribution

---

### **3. Attempt 1 vs Attempt 2 Improvement**

**Chart Type:** Bar chart (positive/negative values)

**What it shows:** Score change from first to second attempt per case

**Data Points:**
- X-axis: Case study titles
- Y-axis: Improvement points (can be negative)
- Color: Green (positive), Red (negative)

**Why it's useful:**
- **Validates feedback quality**
- Shows which cases benefit from retry
- Identifies ineffective rubrics
- Measures learning loop effectiveness

**How to interpret:**
- **All positive bars:** Feedback consistently helps
- **Mixed bars:** Some rubrics better than others
- **All negative bars:** Serious assessment problem
- **Large variations:** Case-specific feedback issues

**Actionable Insights:**
- Negative improvement on a case? Review rubric clarity
- Some cases show no improvement? Feedback not actionable
- Consistent improvement? Feedback strategy is working
- Share high-improvement case rubrics as models

---

### **4. Performance by Campus**

**Chart Type:** Colored bar chart

**What it shows:** Average scores by campus/location

**Data Points:**
- X-axis: Campus names
- Y-axis: Average scores
- Color: Gradient by performance

**Why it's useful:**
- **Geographic performance comparison**
- Infrastructure/resource assessment
- Identifies location-specific issues
- Guides resource allocation

**How to interpret:**
- **Similar scores:** Equitable learning environments
- **One campus lower:** Location-specific issues (internet, facilities)
- **Rural vs urban differences:** Access or infrastructure issues

**Actionable Insights:**
- Low-performing campus? Investigate infrastructure, support staff quality
- Check environment metrics for that campus (internet, noise)
- May need campus-specific interventions

---

### **5. Rubric Mastery Heatmap**

**Chart Type:** Heatmap (color-coded grid)

**What it shows:** Performance on each rubric dimension across all case studies

**Data Points:**
- X-axis: Case study titles
- Y-axis: Rubric dimensions (Evidence, Communication, Analysis)
- Color: Red (low) to Green (high) performance

**Why it's useful:**
- **Multi-dimensional view of learning**
- Identifies skill gaps across curriculum
- Shows which cases test which skills
- Reveals competency distribution

**How to interpret:**
- **Green row:** Dimension is well-mastered
- **Red row:** Dimension needs curriculum attention
- **Green column:** Case shows good performance
- **Red cell:** Specific skill/case combination needs work

**Actionable Insights:**
- Red row (dimension)? Need curriculum-wide focus on that skill
- Red column (case)? That case needs revision or better preparation
- Scattered reds? Good distribution of assessment
- All green? May need more challenging content

---

### **6. Engagement Trends Over Time**

**Chart Type:** Line chart

**What it shows:** Daily active student count over time

**Data Points:**
- X-axis: Dates
- Y-axis: Number of active students
- Line: Trend of engagement

**Why it's useful:**
- **Tracks cohort engagement patterns**
- Shows response to interventions
- Identifies peak/low engagement periods
- Predicts retention issues

**How to interpret:**
- **Steady line:** Consistent engagement
- **Declining trend:** Losing students
- **Spikes:** Assignment due dates
- **Weekend peaks:** Cramming behavior

**Actionable Insights:**
- Declining trend? Implement re-engagement campaign
- Gaps in engagement? Add mid-term check-ins
- Cramming spikes? Adjust due date distribution
- Compare with calendar (exams, breaks) for context

---

## **Detailed Performance Data (4 Tables)**

### **1. Student Performance Summary**

**Columns:**
- student_id, name, cohort, department, campus
- cases_attempted, avg_score, min_score, max_score
- avg_ces, total_hours_spent

**Why it's useful:**
- **Comprehensive individual student view**
- Identifies students needing attention
- Shows engagement patterns
- Enables personalized interventions

**How to use:**
- Sort by avg_score to find struggling students
- Sort by cases_attempted to find disengaged students
- Export for academic advising meetings
- Track individual progress over time

**Actionable Insights:**
- Low attempts + low scores? Engagement AND performance issue
- High attempts + low scores? Needs academic support, showing effort
- Low attempts + high scores? Natural learner, but ensure engagement
- Export at-risk students for intervention program

---

### **2. Case Study Summary**

**Columns:**
- case_study, students_attempted, avg_score
- min_score, max_score, avg_ces
- avg_duration_min, retry_rate

**Why it's useful:**
- **Case study effectiveness measure**
- Identifies problematic content
- Shows workload distribution
- Guides content revision

**How to use:**
- Sort by avg_score to find difficult cases
- Check retry_rate for cases needing revision
- Compare avg_duration with complexity expectations
- Use for curriculum improvement planning

**Actionable Insights:**
- High retry rate + low improvement? Case needs revision
- Low avg_score + high avg_ces? Content issue, not UX
- Very high/low duration? Adjust expected time estimates
- Few students attempted? May need better introduction

---

### **3. At-Risk Students**

**Columns:**
- student_id, name, department, cohort
- avg_score, failing_attempts, last_attempt_date
- total_attempts, completion_rate

**Why it's useful:**
- **Intervention priority list**
- Early warning system
- Retention support
- Academic advising tool

**How to use:**
- Contact students with multiple failing attempts immediately
- Check last_attempt_date for disengaged students
- Sort by avg_score for severity
- Export for counseling referrals

**Actionable Insights:**
- Recent last_attempt but failing? Active but struggling - priority intervention
- Old last_attempt? Disengaged - need re-engagement first
- Low completion rate? May have technical/personal barriers
- Multiple failing attempts? Need strategy change, not just more practice

---

### **4. Rubric Details**

**Columns:**
- case_study, rubric_dimension
- avg_percentage, students_assessed
- needs_improvement_count, improvement_rate

**Why it's useful:**
- **Fine-grained competency analysis**
- Shows specific skill gaps
- Validates rubric effectiveness
- Guides teaching focus

**How to use:**
- Identify which skills need more instruction
- Compare improvement_rate across dimensions
- Check if rubrics are discriminating (not all same)
- Plan targeted skill workshops

**Actionable Insights:**
- Low avg_percentage on dimension? Need targeted teaching
- High needs_improvement_count? Common student weakness
- Low improvement_rate? Rubric feedback not helping
- Use to design remediation workshops

---

## **How Faculty Use This Dashboard**

### **Weekly Teaching Routine:**

**Monday:**
1. Check Active Students - identify disengaged
2. Review Average Score trend - assess teaching effectiveness
3. Check At-Risk Students table - plan interventions

**Wednesday:**
1. Review Rubric Mastery Heatmap - plan Friday's focus
2. Check Engagement Trends - adjust engagement strategies
3. Export data for department meeting

**Friday:**
1. Compare Department Performance - identify inequities
2. Review Case Study Summary - plan next week's cases
3. Set next week's teaching priorities

### **Before Assessments:**

1. Review Rubric Details - remind students of common weaknesses
2. Check Score Distribution - warn about difficult cases
3. Analyze Improvement patterns - encourage retries
4. Export Student Performance for grade predictions

### **After Assessments:**

1. Compare predicted vs actual outcomes
2. Identify students who underperformed expectations
3. Schedule office hours with struggling students
4. Adjust teaching for next cycle based on data

### **End of Semester:**

1. Export all tables for student records
2. Analyze cohort trends vs previous years
3. Document effective interventions
4. Plan curriculum revisions for next semester

---

# **Developer Dashboard**

## **Overview**

The Developer Dashboard provides technical staff with comprehensive insights into system health, API performance, and environmental factors affecting student learning. It ensures platform reliability, identifies technical issues early, and optimizes infrastructure.

### **Who Uses It:**
- Software developers
- DevOps engineers
- IT support staff
- Quality assurance teams
- System administrators

### **Primary Goals:**
1. Monitor system health and reliability
2. Identify and resolve performance issues
3. Track API latency and error rates
4. Analyze environmental impact on learning
5. Ensure optimal user experience

---

## **Key Performance Indicators (8 KPIs)**

### **1. Average API Latency**

**What it tracks:** Mean response time for all API calls (milliseconds)

**Calculation:** `AVG(latency_ms) FROM system_reliability WHERE timestamp in range`

**Why it's useful:**
- **Primary performance indicator**
- User experience directly correlates with latency
- SLA compliance measure
- Capacity planning input

**Interpretation:**
- **Excellent (<100ms):** Very responsive system
- **Good (100-200ms):** Acceptable performance
- **Fair (200-300ms):** Noticeable delay
- **Poor (>300ms):** Serious performance issue

**Thresholds:**
- Target: <150ms average
- Warning: 150-250ms
- Critical: >250ms

**Actionable Insights:**
- Rising latency? Check server load, database queries
- Spikes at certain times? Capacity issue
- Specific API slow? Code optimization needed
- Geographic variation? CDN or routing issue

---

### **2. Max Latency**

**What it tracks:** Highest latency spike observed in period

**Calculation:** `MAX(latency_ms) FROM system_reliability`

**Why it's useful:**
- Identifies worst-case user experience
- Detects anomalous performance events
- Timeout configuration guide
- Infrastructure stress test indicator

**Interpretation:**
- **Low max (<500ms):** Consistent performance
- **Moderate max (500-1000ms):** Occasional spikes
- **High max (>1000ms):** Serious reliability issues

**Actionable Insights:**
- Very high max? Investigate specific incidents
- Frequent high spikes? Underlying stability issue
- Max much higher than average? Outliers need investigation
- Compare max latency timing with user complaints

---

### **3. Average Error Rate**

**What it tracks:** Percentage of failed API requests

**Calculation:** `AVG(error_rate) FROM system_reliability`

**Why it's useful:**
- **System stability indicator**
- Directly impacts user experience
- Data integrity measure
- Development quality indicator

**Interpretation:**
- **Excellent (<0.5%):** Very stable system
- **Good (0.5-1%):** Acceptable reliability
- **Fair (1-2%):** Some stability issues
- **Poor (>2%):** Serious reliability problems

**Thresholds:**
- Target: <0.5%
- Warning: 0.5-1.5%
- Critical: >1.5%

**Actionable Insights:**
- Rising error rate? Check recent deployments
- Specific API errors? Bug in new code
- Geographic error patterns? Infrastructure issue
- Correlate with latency - often related

---

### **4. Average Reliability**

**What it tracks:** Overall system uptime/reliability index (0-100%)

**Calculation:** `AVG(reliability_index) FROM system_reliability`

**Why it's useful:**
- Comprehensive health metric
- SLA reporting measure
- Trust and satisfaction predictor
- Infrastructure investment justification

**Interpretation:**
- **Excellent (99-100%):** Five-nines reliability
- **Good (97-99%):** Acceptable uptime
- **Fair (95-97%):** Noticeable downtime
- **Poor (<95%):** Frequent outages

**Thresholds:**
- Target: >99%
- Warning: 97-99%
- Critical: <97%

**Actionable Insights:**
- Below 99%? Implement redundancy
- Declining reliability? Aging infrastructure
- Specific component failures? Upgrade priority
- Compare with industry benchmarks

---

### **5. API Services Count**

**What it tracks:** Number of distinct APIs being monitored

**Calculation:** `COUNT(DISTINCT api_name) FROM system_reliability`

**Why it's useful:**
- System complexity measure
- Coverage verification
- Monitoring completeness check
- Architecture understanding

**Interpretation:**
- Matches expected architecture? Good coverage
- Missing APIs? Monitoring gaps
- Unexpected APIs? Undocumented services

**Actionable Insights:**
- Fewer than expected? Add monitoring to missing APIs
- More than expected? Clean up deprecated services
- Ensure all critical APIs monitored
- Document all API purposes

---

### **6. Critical Alerts**

**What it tracks:** Number of critical severity incidents

**Calculation:** `COUNT(*) WHERE severity = 'Critical' IN time period`

**Why it's useful:**
- **Immediate attention indicator**
- Measures system stability
- Team workload predictor
- Process improvement input

**Interpretation:**
- **No critical alerts:** System is stable
- **1-3 alerts:** Normal operational issues
- **4-10 alerts:** Unstable period
- **>10 alerts:** Systemic problems

**Thresholds:**
- Acceptable: 0-1 per day
- Warning: 2-5 per day
- Critical: >5 per day

**Actionable Insights:**
- Any critical alert? Investigate immediately
- Frequent alerts? Underlying instability
- Same alert recurring? Permanent fix needed
- Alert fatigue? Review alert threshold settings

---

### **7. Warnings**

**What it tracks:** Number of warning-level incidents

**Calculation:** `COUNT(*) WHERE severity = 'Warning'`

**Why it's useful:**
- Early problem detection
- Preventive maintenance guide
- Trend indicator before critical issues
- Monitoring sensitivity check

**Interpretation:**
- **Low warnings (<10):** Stable or under-monitored
- **Moderate warnings (10-50):** Normal operations
- **High warnings (>50):** Lots of minor issues

**Actionable Insights:**
- Rising warnings? Preventive maintenance needed
- Warnings turning critical? Alert thresholds wrong
- No warnings? May need more monitoring
- Pattern of same warning? Address root cause

---

### **8. System Uptime**

**What it tracks:** Percentage of time system has been available

**Calculation:** `(Total time - Downtime) / Total time × 100`

**Why it's useful:**
- SLA compliance measure
- User trust indicator
- Infrastructure quality measure
- Business impact calculator

**Interpretation:**
- **99.9% (Three nines):** <9 hours downtime/year - Good
- **99.99% (Four nines):** <1 hour downtime/year - Excellent
- **99.999% (Five nines):** <5 min downtime/year - World-class

**Actionable Insights:**
- Below SLA? Implement redundancy, failover
- Calculate downtime cost (users × time × impact)
- Scheduled vs unscheduled downtime ratio
- Improve deployment processes to reduce downtime

---

## **API Performance Analytics (6 Charts)**

### **1. Latency by API Service**

**Chart Type:** Bar chart

**What it shows:** Average latency for each API endpoint

**Why it's useful:**
- **Identifies slow APIs**
- Optimization priority guide
- Compares relative performance
- Reveals architecture bottlenecks

**How to interpret:**
- **Consistent bars:** Well-balanced architecture
- **One tall bar:** That API needs optimization
- **All tall bars:** General performance issue

**Actionable Insights:**
- Slowest API? Profile code, check database queries
- Database API slow? Add indexes, optimize queries
- External API slow? Consider caching
- Gradually slowing? Database growth issue

---

### **2. Error Rate by API Service**

**Chart Type:** Bar chart (color-coded)

**What it shows:** Percentage of failed requests per API

**Why it's useful:**
- Identifies unreliable endpoints
- Bug detection
- Deployment verification
- Integration health check

**How to interpret:**
- **Most bars at zero:** Stable system
- **One high bar:** Specific API bug
- **Multiple high bars:** Systemic issue

**Actionable Insights:**
- High error rate after deployment? Rollback
- Specific errors (404, 500)? Different root causes
- Authentication API errors? Security issue
- Third-party API errors? Monitor their status

---

### **3. Performance by Location**

**Chart Type:** Bar chart (geographic)

**What it shows:** Average latency by geographic location/region

**Why it's useful:**
- **Infrastructure distribution assessment**
- CDN effectiveness measure
- Regional capacity planning
- User experience equity check

**How to interpret:**
- **Similar bars:** Good geographic distribution
- **One high bar:** That region needs attention
- **Rural vs urban gap:** Infrastructure disparity

**Actionable Insights:**
- High latency in one region? Add edge servers, CDN
- International latency high? Need global infrastructure
- Campus-specific issues? Local network problems
- Compare with internet quality metrics

---

### **4. Incidents by Severity**

**Chart Type:** Bar chart

**What it shows:** Count of incidents by severity level (Info/Warning/Critical)

**Why it's useful:**
- System stability overview
- Alert distribution validation
- Team workload indicator
- Monitoring effectiveness

**How to interpret:**
- **Pyramid shape (many info, few critical):** Good
- **Inverted pyramid (many critical):** Poor monitoring or stability
- **All same level:** Alert threshold misconfigured

**Actionable Insights:**
- Too many criticals? Review thresholds
- No criticals ever? Monitoring may be inadequate
- Warnings becoming criticals? Proactive maintenance needed
- Trend over time shows improvements?

---

### **5. Latency Trends Over Time**

**Chart Type:** Line chart

**What it shows:** Daily average API latency over selected period

**Why it's useful:**
- **Performance trend identification**
- Capacity planning
- Deployment impact assessment
- Seasonal pattern detection

**How to interpret:**
- **Flat line:** Consistent performance
- **Upward trend:** Degrading performance
- **Spikes:** Incidents or load spikes
- **Cyclical pattern:** Usage-based fluctuation

**Actionable Insights:**
- Gradual increase? Database growth, need scaling
- Sudden spike? Correlate with deployments
- Daily patterns? Load-based, scale accordingly
- Compare with user count growth

---

### **6. Environment Correlation Analysis (2 Scatter Plots)**

**Chart Type:** Scatter plots with bubble sizing

**Plot 1: Noise Level vs Student Performance**
- X-axis: Ambient noise level (dB)
- Y-axis: Student score (%)
- Bubble size: Connection drops
- Color: Internet stability

**Plot 2: Internet Stability vs Student Performance**
- X-axis: Internet stability score
- Y-axis: Student score (%)
- Bubble size: Connection drops
- Color: Noise level

**Why it's useful:**
- **Shows environmental impact on learning**
- Justifies infrastructure investment
- Identifies optimal learning conditions
- Validates quality requirements

**How to interpret:**
- **Negative correlation:** Environment hurts performance
- **No correlation:** Environment not a factor
- **Clustered patterns:** Threshold effects

**Actionable Insights:**
- Noise impacts scores? Recommend quiet environments
- Internet instability impacts scores? Invest in connectivity
- Large bubbles (many drops) + low scores? Connection critical
- Define minimum environment requirements

---

## **Environment Quality Analysis (4 Charts)**

### **1. Noise Level Distribution**

**Chart Type:** Bar chart (categorized)

**Categories:**
- Quiet (0-40 dB): Library-like
- Moderate (40-60 dB): Normal conversation
- Noisy (60-80 dB): Busy street
- Very Noisy (80+ dB): Construction site

**Why it's useful:**
- Shows where students typically work
- Validates audio quality requirements
- Guides student advice on optimal environments
- Microphone quality assessment

**Actionable Insights:**
- Most attempts in noisy environments? Need noise guidelines
- Correlate with performance to set recommendations
- High noise + low quality index? Microphone issue
- Develop "optimal learning environment" guide

---

### **2. Internet Stability by Device**

**Chart Type:** Bar chart

**What it shows:** Average internet stability score by device type

**Why it's useful:**
- **Device compatibility assessment**
- Minimum specification guide
- Support prioritization
- Platform optimization targets

**How to interpret:**
- **Desktop best:** Expected, more stable connections
- **Mobile worst:** Need mobile optimization
- **Large differences:** Device-specific issues

**Actionable Insights:**
- Mobile stability low? Optimize app for poor connections
- Tablet issues? Test on multiple tablet models
- Desktop problems? May be campus network issue
- Define supported devices clearly

---

### **3. Connection Drops Analysis**

**Chart Type:** Bar chart (categorized)

**Categories:**
- No Drops: Excellent connection
- 1-2 Drops: Minor issues
- 3-5 Drops: Moderate instability
- 6+ Drops: Severe problems

**Why it's useful:**
- Connection quality indicator
- User experience measure
- Infrastructure needs assessment
- Technical support workload predictor

**Actionable Insights:**
- Many drops? Investigate network infrastructure
- Correlate with ISP or campus network
- Drops during peak times? Bandwidth issue
- Attempt recovery features needed?

---

### **4. Signal Strength Distribution**

**Chart Type:** Bar chart

**Categories:**
- Excellent: Strong, reliable signal
- Good: Adequate signal
- Fair: Marginal signal
- Poor: Inadequate signal

**Why it's useful:**
- Wireless infrastructure assessment
- Campus coverage mapping
- Support ticket predictor
- Investment priority guide

**Actionable Insights:**
- Many poor signals? Add WiFi access points
- Specific buildings with poor signal? Infrastructure gap
- Compare performance by signal strength
- Create WiFi coverage map for students

---

## **📋 System Data Tables (4 Tables)**

### **1. System Reliability Log**

**Columns:**
- timestamp, api_name, latency_ms
- error_rate, reliability_index
- location, severity

**Why it's useful:**
- Incident investigation
- Performance debugging
- Trend analysis
- Audit trail

**How to use:**
- Filter by critical severity for immediate issues
- Sort by latency to find slow requests
- Export for detailed performance analysis
- Track specific API over time

---

### **2. Environment Metrics by Attempt**

**Columns:**
- attempt_id, device_type, microphone_type
- noise_level, noise_quality_index
- internet_latency, internet_stability
- connection_drops, signal_strength, student_score

**Why it's useful:**
- Correlate environment with performance
- Student support (identify tech barriers)
- Quality requirement validation
- Research and insights

**How to use:**
- Filter low scores to see environment factors
- Identify students with consistent poor conditions
- Export for statistical analysis
- Guide technical support priorities

---

### **3. Critical Incidents**

**Columns:**
- timestamp, api_name, latency
- error_rate, reliability_index
- location, severity (Critical only)

**Why it's useful:**
- **Immediate attention list**
- Post-incident review
- Pattern detection
- SLA violation tracking

**How to use:**
- Review daily for new critical issues
- Group by API to find problem areas
- Track resolution time
- Document and prevent recurrence

---

### **4. Performance Summary by API**

**Columns:**
- api_name, total_requests
- avg_latency, min_latency, max_latency
- avg_error_rate, avg_reliability
- critical_count, warning_count

**Why it's useful:**
- Comprehensive API health overview
- Optimization prioritization
- Architecture review input
- SLA reporting

**How to use:**
- Sort by avg_latency for optimization targets
- Check critical_count for stability issues
- Compare request volume with performance
- Export for executive reporting

---

## **⚙️ How Developers Use This Dashboard**

### **Daily Operations:**

**Morning Check (9 AM):**
1. Check Critical Alerts - any overnight issues?
2. Review System Uptime - any outages?
3. Check Average Latency - performance degradation?
4. Review Environment Metrics - user experience issues?

**Midday Review (1 PM):**
1. Monitor API Performance charts - any spikes?
2. Check Error Rates - any new issues?
3. Review Incident Log - patterns emerging?

**End of Day (5 PM):**
1. Export Critical Incidents for team meeting
2. Document any issues and resolutions
3. Set alerts for overnight monitoring
4. Plan next day's priorities

### **Weekly Technical Review:**

**Monday:**
1. Review weekend performance
2. Check Environment Correlation - any insights?
3. Plan week's optimization priorities

**Wednesday:**
1. Review Latency Trends - long-term patterns
2. Check Performance by Location - infrastructure needs
3. Update performance documentation

**Friday:**
1. Export weekly summary for management
2. Review all Critical Incidents for the week
3. Document resolutions and improvements
4. Plan next week's infrastructure work

### **Monthly Activities:**

1. Generate SLA compliance report
2. Review all environment metrics for trends
3. Plan infrastructure upgrades
4. Analyze cost vs performance trade-offs
5. Update capacity forecasts

### **Incident Response:**

**When Critical Alert Fires:**
1. Immediately open Critical Incidents table
2. Identify affected API and location
3. Check recent deployments (rollback if needed)
4. Review System Reliability Log for context
5. Implement fix and monitor for 24 hours
6. Document in incident log

---

# 🔧 **Admin Dashboard**

## **Overview**

The Admin Dashboard provides executive leadership with institution-wide analytics for strategic decision-making, resource allocation, and performance monitoring. It offers a comprehensive view of platform health, student outcomes, and institutional effectiveness.

### **Who Uses It:**
- University administrators
- Academic deans
- Vice presidents
- Board members
- Strategic planning teams
- Institutional research

### **Primary Goals:**
1. Monitor institution-wide performance
2. Track strategic KPIs
3. Identify systemic trends
4. Guide resource allocation
5. Support data-driven policy decisions
6. Demonstrate program effectiveness

---

## **📊 Key Performance Indicators (12 KPIs)**

### **1. Total Students**

**What it tracks:** Total number of students in filtered population

**Calculation:** `COUNT(students) matching filter criteria`

**Why it's useful:**
- **Scale indicator**
- Enrollment tracking
- Market size measure
- Resource planning baseline

**Strategic Insights:**
- Growing enrollment? Capacity planning needed
- Declining enrollment? Retention/marketing issue
- Compare with targets and previous years

---

### **2. Active Students**

**What it tracks:** Students with activity in time period

**Calculation:** `COUNT(DISTINCT students with attempts) in range`

**Why it's useful:**
- **Engagement indicator**
- Platform adoption measure
- Retention early warning
- ROI justification

**Strategic Insights:**
- Low activation rate? Onboarding issue
- Declining active users? Engagement problem
- Calculate: Active/Total = Adoption rate

---

### **3. Total Attempts**

**What it tracks:** Cumulative case study attempts across platform

**Calculation:** `COUNT(all attempts) in time period`

**Why it's useful:**
- Platform usage volume
- Server capacity planning
- Engagement depth measure
- Activity trends

**Strategic Insights:**
- Growing attempts? Platform is valuable
- Attempts per student = engagement metric
- Compare with benchmark institutions

---

### **4. Platform Average Score**

**What it tracks:** Mean score across entire institution

**Calculation:** `AVG(scores) FROM all students in range`

**Why it's useful:**
- **Primary learning outcomes measure**
- Program quality indicator
- Accreditation evidence
- Benchmark for improvement goals

**Strategic Insights:**
- Below 75%? Program-wide intervention needed
- Trending down? Curriculum or student quality issue
- Compare with program learning objectives

**Benchmarks:**
- Target: 75-80%
- Warning: 70-74%
- Critical: <70%

---

### **5. Completion Rate**

**What it tracks:** Percentage of completed vs started attempts

**Calculation:** `(Completed / Total) × 100 across institution`

**Why it's useful:**
- **Success indicator**
- Retention predictor
- UX/technical issue detector
- Student support effectiveness

**Strategic Insights:**
- Below 80%? Systemic barriers to completion
- High dropout rate? Difficulty or technical issues
- Measure of institutional support quality

---

### **6. Average Improvement**

**What it tracks:** Mean score gain from attempt 1 to 2 institution-wide

**Calculation:** `AVG(attempt2 - attempt1) across all students`

**Why it's useful:**
- **Learning effectiveness measure**
- Pedagogy validation
- Assessment quality indicator
- Growth mindset culture indicator

**Strategic Insights:**
- <5% improvement? Assessment feedback not effective
- >10% improvement? Strong learning culture
- Validates formative assessment approach

---

### **7. Total Learning Hours**

**What it tracks:** Cumulative time invested in learning

**Calculation:** `SUM(duration_seconds) / 3600 across all attempts`

**Why it's useful:**
- Engagement depth measure
- Workload assessment
- ROI calculation (hours × value)
- Resource utilization

**Strategic Insights:**
- Hours per student = engagement metric
- Compare with credit hours expectations
- Trend over time shows sustained engagement

---

### **8. Average CES Score**

**What it tracks:** Mean customer effort score (satisfaction)

**Calculation:** `AVG(ces_value) across all attempts`

**Why it's useful:**
- **User satisfaction indicator**
- Platform adoption predictor
- Investment justification
- Vendor performance measure

**Strategic Insights:**
- Below 70? Platform needs improvement
- Compare with industry benchmarks
- Correlate with retention rates

---

### **9. Case Studies Used**

**What it tracks:** Number of different case studies with activity

**Calculation:** `COUNT(DISTINCT case_id) with attempts`

**Why it's useful:**
- Content utilization measure
- Curriculum diversity indicator
- Investment ROI (cases used vs purchased)
- Content gap identifier

**Strategic Insights:**
- Low utilization? Some content not being assigned
- Certain cases unused? Quality or relevance issue
- Utilization rate = Value for money

---

### **10. Total Sessions**

**What it tracks:** Total number of learning sessions across platform

**Calculation:** `COUNT(DISTINCT session_id) in time period`

**Why it's useful:**
- Platform activity volume
- Server capacity planning
- Engagement frequency measure
- Growth tracking

**Strategic Insights:**
- Sessions per student = engagement frequency
- Growing sessions? Platform is sticky
- Compare with unique users for session length

---

### **11. Average Attempts per Student**

**What it tracks:** Mean number of attempts each student completes

**Calculation:** `Total attempts / Total students`

**Why it's useful:**
- **Engagement depth indicator**
- Curriculum coverage measure
- Platform value demonstration
- Benchmark for expectations

**Strategic Insights:**
- Low (<5)? Students not fully engaged
- High (>15)? Strong practice culture
- Set targets: "Students should complete X attempts"

---

### **12. Average Hours per Student**

**What it tracks:** Mean time each student invests in learning

**Calculation:** `Total hours / Total students`

**Why it's useful:**
- Time investment measure
- Workload assessment
- Value demonstration (hours of education provided)
- Efficiency metric (hours per outcome)

**Strategic Insights:**
- Below expectations? Not enough practice
- Very high? May be too difficult
- Cost per hour = budget / total hours

---

## **📊 Institutional Trends (4 Charts)**

### **1. Performance Trends Over Time**

**Chart Type:** Line chart

**What it shows:** Daily average scores across institution

**Why it's useful:**
- **Tracks institutional learning trajectory**
- Shows impact of interventions
- Seasonal pattern detection
- Quality assurance monitoring

**How to interpret:**
- **Upward trend:** Continuous improvement
- **Downward trend:** Program quality issue
- **Flat line:** Plateau, need new approaches
- **Seasonal dips:** Exam periods, holidays

**Strategic Insights:**
- Declining trend? Investigate curriculum, support, or admissions
- Improvement after intervention? Validates strategy
- Compare with student satisfaction surveys
- Use for accreditation evidence

**Decision Support:**
- Justifies program improvements
- Guides when to implement changes
- Shows return on investment
- Board reporting metric

---

### **2. Student Engagement Trends**

**Chart Type:** Line chart

**What it shows:** Daily active student count over time

**Why it's useful:**
- Platform adoption tracking
- Retention early warning
- Marketing campaign effectiveness
- Seasonal patterns

**How to interpret:**
- **Growing trend:** Successful adoption
- **Declining trend:** Retention problem
- **Stable trend:** Mature platform
- **Spikes:** Response to campaigns or deadlines

**Strategic Insights:**
- Declining engagement? Need re-engagement campaign
- Seasonal patterns? Plan support accordingly
- Compare with enrollment trends
- Predict churn risk

**Decision Support:**
- Marketing budget allocation
- Student support staffing
- Platform investment justification
- Retention program effectiveness

---

### **3. Learning Hours Trend**

**Chart Type:** Line chart

**What it shows:** Daily total learning hours across institution

**Why it's useful:**
- Activity volume tracking
- Capacity planning
- Value demonstration
- Engagement quality measure

**How to interpret:**
- **Growing hours:** Increased engagement
- **Stable hours:** Consistent usage
- **Declining hours:** Disengagement risk
- **Peak patterns:** Workload distribution

**Strategic Insights:**
- Hours growing faster than users? Deeper engagement
- Hours declining with stable users? Losing value
- Peak hours? Server capacity planning
- Total hours = impressive institutional metric

**Decision Support:**
- "Platform provided X hours of education"
- Justify subscription costs
- Plan infrastructure capacity
- Demonstrate program value

---

### **4. Completion Rate Trend**

**Chart Type:** Line chart

**What it shows:** Daily completion rate across platform

**Why it's useful:**
- **Quality indicator**
- Success rate tracking
- UX problem detector
- Student support effectiveness

**How to interpret:**
- **Stable high rate (>85%):** Healthy system
- **Declining rate:** Growing barriers to success
- **Improving rate:** Support interventions working
- **Volatile rate:** Inconsistent quality

**Strategic Insights:**
- Rate declining? Systematic barriers emerging
- Rate improving? Interventions validated
- Compare with industry benchmarks
- Predict student success rates

**Decision Support:**
- Justify student support investments
- Identify when additional resources needed
- Measure program quality
- Set institutional goals

---

## **🎯 Cross-Sectional Analysis (4 Charts)**

### **1. Performance by Department**

**Chart Type:** Bar chart (color-coded)

**What it shows:** Average scores for each academic department

**Why it's useful:**
- **Resource allocation guide**
- Identifies high/low performers
- Equity assessment
- Best practice identification

**How to interpret:**
- **Similar bars:** Equitable quality
- **Large variations:** Resource or quality disparities
- **Consistently low department:** Needs targeted support
- **Consistently high department:** Share best practices

**Strategic Insights:**
- Low performer? Investigate resources, faculty, prerequisites
- High performer? Document and replicate success factors
- Growing gap? Equity issue requiring intervention
- Use for budget allocation decisions

**Decision Support:**
- Justify department-specific funding
- Identify professional development needs
- Guide faculty hiring priorities
- Measure programmatic quality

---

### **2. Performance by Campus**

**Chart Type:** Bar chart (color-coded)

**What it shows:** Average scores for each campus/location

**Why it's useful:**
- **Geographic equity assessment**
- Infrastructure investment guide
- Identifies location-specific needs
- Resource distribution validator

**How to interpret:**
- **Similar bars:** Equitable educational opportunity
- **Rural campus lower:** Infrastructure or access issue
- **One campus significantly lower:** Investigate causes
- **Urban-rural gap:** May need targeted interventions

**Strategic Insights:**
- Low-performing campus? Check internet, facilities, faculty
- Consistent underperformance? May need campus closure or investment
- Growing gaps? Inequitable resource distribution
- High performer? Model for other campuses

**Decision Support:**
- Capital investment priorities
- Campus expansion decisions
- Resource reallocation
- Equity initiatives

---

### **3. Student Distribution by Cohort**

**Chart Type:** Pie chart

**What it shows:** Enrollment distribution across cohorts (top 10)

**Why it's useful:**
- Enrollment pattern visualization
- Program popularity indicator
- Capacity planning
- Marketing effectiveness

**How to interpret:**
- **Balanced slices:** Healthy enrollment distribution
- **One dominant slice:** Popular program or cohort structure
- **Many small slices:** Fragmented enrollment
- **Shrinking slice:** Program losing popularity

**Strategic Insights:**
- Growing cohorts? Successful programs
- Declining cohorts? Need marketing or revision
- Uneven distribution? Capacity allocation issue
- Historical comparison shows trends

**Decision Support:**
- Program continuation/elimination
- Marketing budget allocation
- Faculty hiring by program
- Facility planning

---

### **4. Case Study Usage**

**Chart Type:** Bar chart

**What it shows:** Attempt count for each case study

**Why it's useful:**
- **Content utilization measure**
- ROI on case study development
- Popularity indicator
- Curriculum gaps identifier

**How to interpret:**
- **Even distribution:** Good curriculum balance
- **Rarely used cases:** Poor quality or not assigned
- **Overused cases:** May need more similar content
- **Unused cases:** Wasted investment

**Strategic Insights:**
- Low usage? Investigate why (difficulty, irrelevance, not assigned)
- High usage? Students find valuable, develop more similar
- Zero usage? Consider retirement or promotion
- Use to guide future case development

**Decision Support:**
- Content development priorities
- Case study purchase decisions
- Faculty training needs (how to use cases)
- Budget justification for new content

---

## **🖥️ System & Environment Overview (2 Summaries)**

### **1. System Performance Summary**

**Displays:**
- Average Latency
- Max Latency
- Average Error Rate
- Average Reliability
- Critical Incidents

**Why it's useful:**
- **IT investment justification**
- SLA compliance verification
- Vendor performance tracking
- Infrastructure planning

**Strategic Insights:**
- Poor performance? Need infrastructure investment
- Improving metrics? Validate IT investments working
- Compare with industry SLAs
- Calculate cost of downtime

**Decision Support:**
- Justify IT budget requests
- Vendor contract negotiations
- Infrastructure upgrade priorities
- Risk assessment

---

### **2. Environment Quality Summary**

**Displays:**
- Average Noise Level
- Average Internet Stability
- Average Internet Latency
- Average Connection Drops
- Total Attempts Monitored

**Why it's useful:**
- Student experience understanding
- Infrastructure needs assessment
- Equity analysis (internet access)
- Minimum requirements validation

**Strategic Insights:**
- High noise levels? Need quiet study space guidance
- Poor internet? Campus infrastructure investment needed
- Many connection drops? WiFi upgrades required
- Rural vs urban quality gaps? Digital divide issue

**Decision Support:**
- Campus facility investments
- Student technology support programs
- Minimum technology requirements
- Student support budget

---

## **📋 Administrative Reports (4 Tables)**

### **1. Department Performance Summary**

**Columns:**
- department, total_students, active_students, active_rate
- total_attempts, avg_score, min_score, max_score
- avg_ces, total_hours, at_risk_attempts

**Why it's useful:**
- **Comprehensive departmental overview**
- Resource allocation decisions
- Performance benchmarking
- Intervention planning

**How to use:**
- Sort by avg_score to identify struggling departments
- Check active_rate for engagement issues
- Export for budget discussions
- Track improvement over time

**Strategic Insights:**
- Low active_rate? Department-specific engagement issue
- High at_risk_attempts? Need academic support program
- Low avg_score + high hours? Study efficiency problem
- Compare departments for best practices

**Decision Support:**
- Department funding allocations
- Faculty development priorities
- Student support program design
- Program continuation decisions

---

### **2. Campus Performance Summary**

**Columns:**
- campus, total_students, active_students, active_rate
- total_attempts, avg_score, avg_ces
- total_hours, cases_used

**Why it's useful:**
- Campus comparison
- Geographic equity assessment
- Facilities investment guide
- Performance benchmarking

**How to use:**
- Identify underperforming campuses
- Compare resource utilization
- Export for facilities planning
- Track multi-year trends

**Strategic Insights:**
- Campus with low score + low CES? Facilities issue
- Rural campuses underperforming? Infrastructure gap
- One campus excelling? Replicate model
- Growing performance gap? Equity problem

**Decision Support:**
- Campus expansion/closure decisions
- Capital improvement priorities
- Staff allocation by campus
- Service equity initiatives

---

### **3. Case Study Analytics**

**Columns:**
- case_study, unique_students, total_attempts
- avg_score, min_score, max_score
- avg_duration_min, retry_rate, avg_ces

**Why it's useful:**
- Content effectiveness measure
- Development ROI analysis
- Curriculum planning
- Quality assurance

**How to use:**
- Sort by avg_score to find difficult cases
- Check retry_rate for cases needing revision
- Export for curriculum committee
- Guide case study purchases

**Strategic Insights:**
- High retry rate? Case is challenging or unclear
- Low unique_students? Not being assigned or too difficult
- Very high/low duration? Workload calibration needed
- Low avg_ces? User experience issues

**Decision Support:**
- Case study purchase decisions
- Content development priorities
- Faculty training needs
- Curriculum revision planning

---

### **4. Performance Benchmarks**

**Rows:**
- Platform Average (overall score)
- Completion Rate
- Average CES
- Average Learning Hours per Student
- Student Engagement Rate

**Why it's useful:**
- **Key metrics summary for executives**
- Board reporting
- Accreditation evidence
- Strategic planning baseline

**How to use:**
- Export for board meetings
- Compare with previous periods
- Set institutional goals
- Track against strategic plan

**Strategic Insights:**
- All metrics improving? Strategy is working
- Mixed results? Targeted interventions needed
- Compare with peer institutions
- Set evidence-based goals

**Decision Support:**
- Justify strategic investments
- Set institutional priorities
- Measure strategic plan progress
- Board performance reporting

---

## **🎯 How Administrators Use This Dashboard**

### **Monthly Executive Review:**

**Week 1: Performance Assessment**
1. Review all 12 KPIs - are we meeting goals?
2. Check Performance Trends - quality maintaining?
3. Review Engagement Trends - students active?
4. Export Department Summary for deans meeting

**Week 2: Resource Planning**
1. Review Department Performance - who needs support?
2. Check Campus Performance - geographic equity?
3. Analyze Case Study Usage - content ROI?
4. Plan budget allocations based on data

**Week 3: Strategic Initiatives**
1. Check System Performance - need IT investment?
2. Review Environment Quality - infrastructure needs?
3. Analyze Completion Rate Trends - support working?
4. Plan improvement initiatives

**Week 4: Reporting**
1. Export Performance Benchmarks for board
2. Prepare trend reports for stakeholders
3. Document success stories and concerns
4. Set next month's priorities

### **Quarterly Board Meetings:**

**Preparation:**
1. Export all 4 administrative tables
2. Create trend charts for key metrics
3. Document major initiatives and outcomes
4. Prepare explanations for variances

**Presentation:**
1. Show Platform Average Score trend
2. Demonstrate Total Learning Hours (impressive)
3. Highlight Improvement metrics (learning works)
4. Present Completion Rate (success rate)
5. Show Engagement Trends (adoption)

**Decision Support:**
1. Justify budget requests with data
2. Demonstrate program effectiveness
3. Identify risks with evidence
4. Set data-driven goals for next quarter

### **Annual Strategic Planning:**

**Data Analysis:**
1. Review full-year trends across all metrics
2. Compare performance with institutional goals
3. Identify systemic issues needing attention
4. Document successes to replicate

**Resource Allocation:**
1. Use Department Performance for budget distribution
2. Use Campus Performance for facilities planning
3. Use Case Study Analytics for content budget
4. Use System Performance for IT budget

**Goal Setting:**
1. Platform Average Score target: +5% year-over-year
2. Engagement target: 80% active students
3. Completion Rate target: >85%
4. Average Improvement target: >10 points

---

## **🔄 Cross-Dashboard Insights**

### **How Dashboards Work Together:**

**Scenario 1: Declining Performance Alert**

**Admin sees:** Platform Average Score declining
↓
**Drills down to Faculty Dashboard:** Identifies Department X struggling
↓
**Faculty checks:** Specific case studies showing low scores
↓
**Developer checks:** No technical issues, good environment
↓
**Action:** Academic intervention needed, not technical

---

**Scenario 2: Low Engagement**

**Admin sees:** Active Students declining
↓
**Faculty checks:** Certain cohorts not participating
↓
**Developer checks:** High error rates during peak times
↓
**Action:** Technical issue causing frustration, not academic

---

**Scenario 3: At-Risk Student**

**Student sees:** Own low scores and poor improvement
↓
**Faculty sees:** Student in At-Risk table
↓
**Developer sees:** Student has poor environment (noise, connection)
↓
**Action:** Provide technical support + academic help

---

### **Stakeholder Communication Flow:**

**Students → Faculty:**
- Performance concerns
- Technical difficulties
- Content feedback

**Faculty → Admin:**
- Resource needs
- Program quality issues
- Success stories

**Developer → Faculty:**
- Platform issues affecting users
- Environment recommendations
- Feature updates

**Admin → All:**
- Strategic priorities
- Policy changes
- Resource allocations

---

## **📈 Success Metrics Summary**

### **Student Success:**
- Average Score: >75%
- Improvement: >10 points
- Completion Rate: >85%
- Time Investment: Appropriate for credit hours

### **Institutional Success:**
- Active Students: >75% of enrolled
- Department Equity: Scores within 10% across departments
- Case Utilization: >80% of content used
- Platform Satisfaction (CES): >75

### **Technical Success:**
- API Latency: <150ms average
- Error Rate: <0.5%
- System Reliability: >99%
- Critical Incidents: <1 per day

### **Engagement Success:**
- Attempts per Student: >8
- Hours per Student: Meets expectations
- Session Frequency: Regular (>2x/week)
- Completion Rate: >85%

---

## **🎓 Conclusion**

The MIND Dashboard provides comprehensive, actionable insights across four specialized views:

- **Students** understand their learning journey
- **Faculty** optimize teaching and support
- **Developers** ensure platform excellence
- **Administrators** make strategic decisions

**Together, these dashboards enable:**
- Data-driven decision making at all levels
- Early identification of risks and opportunities
- Evidence-based continuous improvement
- Accountability and transparency
- Student success through personalized insights

**The result:** A more effective, efficient, and equitable educational experience powered by comprehensive analytics.

---

**For additional help or questions, refer to the specific dashboard README files or contact the MIND platform team.**
