import streamlit as st
import os
import statistics

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Campus - DSCE",
    layout="centered"
)

# ── Shared state (persists within session) ────────────────────
if "courses" not in st.session_state:
    st.session_state.courses = []
if "students" not in st.session_state:
    st.session_state.students = []
if "file_records" not in st.session_state:
    st.session_state.file_records = []
    st.session_state.file_id = 101

# ── Sidebar navigation ────────────────────────────────────────
st.sidebar.title("Smart Campus")
st.sidebar.markdown("---")

page = st.sidebar.radio("Go to", [
    "Dashboard",
    "Lab 1 · Registration & Grades",
    "Lab 2 · Course Enrollment",
    "Lab 3 · Student Records",
    "Lab 4 · Search & Sort",
    "Lab 5 · Fee Calculation",
    "Lab 6 · File Records",
    "Lab 7 · Directory Scanner",
    "Lab 8 · Performance Analytics",
])

st.sidebar.markdown("---")
st.sidebar.caption("Lab 9 & 10 — Integration Project")

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "Dashboard":
    st.title("Smart Campus Information System")
    st.caption("Dayananda Sagar College of Engineering · Python Programming Lab")
    #st.markdown("---")

    #col1, col2, col3, col4 = st.columns(4)
    #col1.metric("Total Modules", "8")
    #col2.metric("Course Code", "1BPLC105B")
    #col3.metric("Credits", "4")
    #col4.metric("Type", "PLC")

    #st.markdown("---")
    st.subheader("All Modules")

    c1, c2 = st.columns(2)
    with c1:
        st.info("**Lab 1** · Registration & Grade Evaluation")
        st.info("**Lab 2** · Course Enrollment Management")
        st.info("**Lab 3** · Student Record Data Management")
        st.info("**Lab 4** · Sorting & Searching Student IDs")
    with c2:
        st.info("**Lab 5** · Student Fee Calculation")
        st.info("**Lab 6** · File Handling — Academic Records")
        st.info("**Lab 7** · Directory Scanner")
        st.info("**Lab 8** · Performance Analytics")

    st.markdown("---")
    st.caption("Use the sidebar to navigate between modules.")


# ══════════════════════════════════════════════════════════════
# LAB 1 — Registration & Grade Evaluation
# ══════════════════════════════════════════════════════════════
elif page == "Lab 1 · Registration & Grades":
    st.title("Student Registration & Grade Evaluation")
    st.caption("Lab 1 · Conditional Statements (if-elif-else)")
    st.markdown("---")

    name  = st.text_input("Student Name", placeholder="e.g. Priya Sharma")
    score = st.number_input("Exam Score (0 – 100)", min_value=0.0, max_value=100.0, step=0.5)

    if st.button("Evaluate Grade"):
        if not name.strip():
            st.error("Please enter a student name.")
        else:
            if score >= 90:
                grade, remark = "A", "Excellent"
            elif score >= 75:
                grade, remark = "B", "Very Good"
            elif score >= 60:
                grade, remark = "C", "Good"
            elif score >= 40:
                grade, remark = "D", "Average"
            else:
                grade, remark = "F", "Needs Improvement"

            st.markdown("---")
            st.subheader("Student Report")
            c1, c2 = st.columns(2)
            c1.metric("Name", name)
            c1.metric("Score", score)
            c2.metric("Grade", grade)
            c2.metric("Remark", remark)

            if grade == "A":
                st.success(f"{name} scored {score} — Grade {grade}: {remark}")
            elif grade in ("B", "C"):
                st.info(f"{name} scored {score} — Grade {grade}: {remark}")
            elif grade == "D":
                st.warning(f"{name} scored {score} — Grade {grade}: {remark}")
            else:
                st.error(f"{name} scored {score} — Grade {grade}: {remark}")


# ══════════════════════════════════════════════════════════════
# LAB 2 — Course Enrollment
# ══════════════════════════════════════════════════════════════
elif page == "Lab 2 · Course Enrollment":
    st.title("Course Enrollment Management")
    st.caption("Lab 2 · Loops (while, break, continue)")
    st.markdown("---")

    col1, col2 = st.columns(2)
    course_name = col1.text_input("Course Name", placeholder="e.g. Mathematics")
    credits     = col2.number_input("Credits", min_value=1, max_value=10, step=1)

    c1, c2 = st.columns([1, 1])
    add   = c1.button("Add Course")
    clear = c2.button("Clear All")

    if add:
        if not course_name.strip():
            st.error("Course name cannot be empty. (continue — skip invalid input)")
        elif len(st.session_state.courses) >= 5:
            st.error("Maximum 5 courses reached. (break — stop adding)")
        else:
            st.session_state.courses.append({"name": course_name, "credits": int(credits)})
            st.success(f"'{course_name}' with {credits} credits added.")

    if clear:
        st.session_state.courses = []
        st.info("All courses cleared.")

    if st.session_state.courses:
        st.markdown("---")
        st.subheader("Enrolled Courses")
        total_credits = 0
        for i, c in enumerate(st.session_state.courses):
            st.write(f"{i+1}. **{c['name']}** — {c['credits']} credits")
            total_credits += c["credits"]
        st.markdown("---")
        col1, col2 = st.columns(2)
        col1.metric("Total Courses", f"{len(st.session_state.courses)} / 5")
        col2.metric("Total Credits", total_credits)
    else:
        st.info("No courses enrolled yet.")


# ══════════════════════════════════════════════════════════════
# LAB 3 — Student Records
# ══════════════════════════════════════════════════════════════
elif page == "Lab 3 · Student Records":
    st.title("Student Record Data Management")
    st.caption("Lab 3 · Data Structures — Lists, Dictionaries, Sets")
    st.markdown("---")

    st.subheader("Add Student Record")
    col1, col2 = st.columns(2)
    name   = col1.text_input("Student Name", placeholder="e.g. Rahul")
    age    = col2.number_input("Age", min_value=1, max_value=100, step=1)
    grades = st.text_input("Grades (comma separated)", placeholder="e.g. 85, 90, 78")

    c1, c2 = st.columns([1, 1])
    add   = c1.button("Add Student")
    clear = c2.button("Clear Records")

    if add:
        if not name.strip():
            st.error("Name cannot be empty.")
        else:
            try:
                grade_list = [float(g.strip()) for g in grades.split(",") if g.strip()]
                if not grade_list:
                    st.error("Enter at least one grade.")
                else:
                    avg = round(sum(grade_list) / len(grade_list), 2)
                    st.session_state.students.append({
                        "name": name, "age": int(age),
                        "grades": grade_list, "avg": avg
                    })
                    st.success(f"Record for '{name}' added.")
            except ValueError:
                st.error("Invalid grades. Enter numbers separated by commas.")

    if clear:
        st.session_state.students = []
        st.info("Records cleared.")

    if st.session_state.students:
        st.markdown("---")
        st.subheader("Student Records (List of Dictionaries)")
        for i, s in enumerate(st.session_state.students):
            st.write(f"**{i+1}. {s['name']}** | Age: {s['age']} | Grades: {s['grades']} | Avg: {s['avg']}")

    # Set analysis
    st.markdown("---")
    st.subheader("Event Participation Analysis (Sets)")

    event_A = {"Priya", "Rahul", "Anita", "Kiran"}
    event_B = {"Rahul", "Anita", "Sneha"}

    col1, col2 = st.columns(2)
    col1.write("**Event A:**")
    col1.write(sorted(event_A))
    col2.write("**Event B:**")
    col2.write(sorted(event_B))

    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.write("**Common (A ∩ B):**")
    col1.write(sorted(event_A & event_B))
    col1.write("**Only in A (A − B):**")
    col1.write(sorted(event_A - event_B))
    col2.write("**All Participants (A ∪ B):**")
    col2.write(sorted(event_A | event_B))
    col2.write("**Only in B (B − A):**")
    col2.write(sorted(event_B - event_A))


# ══════════════════════════════════════════════════════════════
# LAB 4 — Search & Sort
# ══════════════════════════════════════════════════════════════
elif page == "Lab 4 · Search & Sort":
    st.title("Sorting & Searching Student IDs")
    st.caption("Lab 4 · Bubble Sort, Selection Sort, Linear Search, Binary Search")
    st.markdown("---")

    ids_input    = st.text_input("Student IDs (comma separated)", value="105, 102, 110, 108, 101, 115")
    target_input = st.number_input("Search Target ID", value=108, step=1)

    def bubble_sort(arr):
        lst = arr[:]
        n = len(lst)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
        return lst

    def selection_sort(arr):
        lst = arr[:]
        n = len(lst)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if lst[j] < lst[min_idx]:
                    min_idx = j
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
        return lst

    def linear_search(arr, t):
        for i in range(len(arr)):
            if arr[i] == t:
                return i
        return -1

    def binary_search(arr, t):
        lo, hi = 0, len(arr) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == t:
                return mid
            elif arr[mid] < t:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    if st.button("Sort & Search"):
        try:
            ids = [int(x.strip()) for x in ids_input.split(",") if x.strip()]
            target = int(target_input)
            if len(ids) < 2:
                st.error("Enter at least 2 IDs.")
            else:
                bs = bubble_sort(ids)
                ss = selection_sort(ids)
                li = linear_search(ids, target)
                bi = binary_search(bs, target)

                st.markdown("---")
                st.subheader("Sorting Results")
                st.write(f"**Original:**   {ids}")
                st.write(f"**Bubble Sort:**    {bs}")
                st.write(f"**Selection Sort:** {ss}")

                st.markdown("---")
                st.subheader(f"Search Results for ID {target}")
                if li != -1:
                    st.success(f"Linear Search: Found at index {li} (original list)")
                else:
                    st.error("Linear Search: Not found")

                if bi != -1:
                    st.success(f"Binary Search: Found at index {bi} (sorted list)")
                else:
                    st.error("Binary Search: Not found")
        except ValueError:
            st.error("Enter valid comma-separated integers for IDs.")


# ══════════════════════════════════════════════════════════════
# LAB 5 — Fee Calculation
# ══════════════════════════════════════════════════════════════
elif page == "Lab 5 · Fee Calculation":
    st.title("Student Fee Calculation")
    st.caption("Lab 5 · Functions with Default Parameters")
    st.markdown("---")

    def calculate_fee(tuition_fee, hostel_fee=0, transportation_fee=0):
        return tuition_fee + hostel_fee + transportation_fee

    name      = st.text_input("Student Name", placeholder="e.g. Anita")
    tuition   = st.number_input("Tuition Fee (₹)", min_value=0.0, step=1000.0)
    hostel    = st.number_input("Hostel Fee (₹) — optional (default = 0)", min_value=0.0, step=1000.0)
    transport = st.number_input("Transport Fee (₹) — optional (default = 0)", min_value=0.0, step=500.0)

    if st.button("Calculate Fee"):
        if tuition <= 0:
            st.error("Please enter a valid tuition fee.")
        else:
            total = calculate_fee(tuition, hostel, transport)
            st.markdown("---")
            st.subheader(f"Fee Breakdown — {name or 'Student'}")
            st.write(f"Tuition Fee: ₹ {tuition:,.2f}")
            if hostel:
                st.write(f"Hostel Fee: ₹ {hostel:,.2f}")
            if transport:
                st.write(f"Transport Fee: ₹ {transport:,.2f}")
            st.markdown("---")
            st.metric("Total Fee", f"₹ {total:,.2f}")


# ══════════════════════════════════════════════════════════════
# LAB 6 — File Records
# ══════════════════════════════════════════════════════════════
elif page == "Lab 6 · File Records":
    st.title("File Handling — Academic Records")
    st.caption("Lab 6 · File Operations (write, read, process)")
    st.markdown("---")

    def get_grade(m):
        if m >= 90: return "A", "Excellent"
        elif m >= 75: return "B", "Very Good"
        elif m >= 60: return "C", "Good"
        elif m >= 40: return "D", "Average"
        else: return "F", "Needs Improvement"

    col1, col2 = st.columns(2)
    name  = col1.text_input("Student Name", placeholder="e.g. Arjun")
    marks = col2.number_input("Marks (0–100)", min_value=0, max_value=100, step=1)

    c1, c2, c3 = st.columns(3)
    add    = c1.button("Write Record")
    report = c2.button("Generate Report")
    clear  = c3.button("Clear File")

    if add:
        if not name.strip():
            st.error("Name cannot be empty.")
        else:
            grade, remark = get_grade(marks)
            st.session_state.file_records.append({
                "id": st.session_state.file_id,
                "name": name, "marks": marks,
                "grade": grade, "remark": remark
            })
            st.session_state.file_id += 1
            st.success(f"Record for '{name}' written.")

    if clear:
        st.session_state.file_records = []
        st.session_state.file_id = 101
        st.info("File cleared.")

    if st.session_state.file_records:
        st.markdown("---")
        st.subheader("Stored Records (student_records.txt)")

        # Show raw file format
        raw = "ID,Name,Marks\n"
        for r in st.session_state.file_records:
            raw += f"{r['id']},{r['name']},{r['marks']}\n"
        st.code(raw, language="text")

        # Table
        st.subheader("Parsed Records")
        for r in st.session_state.file_records:
            st.write(f"**{r['id']}** | {r['name']} | {r['marks']} marks | Grade: {r['grade']} — {r['remark']}")

    if report:
        if not st.session_state.file_records:
            st.error("No records to report.")
        else:
            recs = st.session_state.file_records
            total = len(recs)
            avg   = round(sum(r["marks"] for r in recs) / total, 2)
            top   = max(recs, key=lambda r: r["marks"])
            low   = min(recs, key=lambda r: r["marks"])

            st.markdown("---")
            st.subheader("Generated Report")
            col1, col2 = st.columns(2)
            col1.metric("Total Students", total)
            col1.metric("Average Marks", avg)
            col2.metric("Top Student", f"{top['name']} ({top['marks']})")
            col2.metric("Lowest Scorer", f"{low['name']} ({low['marks']})")


# ══════════════════════════════════════════════════════════════
# LAB 7 — Directory Scanner
# ══════════════════════════════════════════════════════════════
elif page == "Lab 7 · Directory Scanner":
    st.title("Directory Scanner")
    st.caption("Lab 7 · os.walk, Exception Handling, User-Defined Exceptions")
    st.markdown("---")

    class MissingFileOrFolderError(Exception):
        pass

    path = st.text_input("Directory Path", placeholder=r"e.g. C:\Users\YourName\Desktop\SmartCampus")

    if st.button("Scan Directory"):
        if not path.strip():
            st.error("Please enter a directory path.")
        elif not os.path.exists(path):
            st.error(f"FileNotFoundError: Invalid directory path: '{path}'")
        elif not os.path.isdir(path):
            st.error(f"NotADirectoryError: '{path}' is not a directory.")
        else:
            st.markdown("---")
            st.subheader("Directory Structure")
            tree_text = ""
            total_files = 0
            total_folders = 0
            warnings = []

            try:
                for root, dirs, files in os.walk(path):
                    level = root.replace(path, "").count(os.sep)
                    indent = "    " * level
                    tree_text += f"{indent}📁 {os.path.basename(root)}/\n"
                    total_folders += 1
                    for f in files:
                        tree_text += f"{'    ' * (level + 1)}📄 {f}\n"
                        total_files += 1
                    if not files and not dirs:
                        try:
                            raise MissingFileOrFolderError(f"Empty folder: '{root}'")
                        except MissingFileOrFolderError as e:
                            warnings.append(str(e))

                st.code(tree_text, language="text")
                col1, col2 = st.columns(2)
                col1.metric("Total Folders", total_folders)
                col2.metric("Total Files", total_files)

                if warnings:
                    st.markdown("---")
                    for w in warnings:
                        st.warning(f"⚠ MissingFileOrFolderError: {w}")

            except PermissionError:
                st.error(f"PermissionError: Cannot access '{path}'")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")


# ══════════════════════════════════════════════════════════════
# LAB 8 — Performance Analytics
# ══════════════════════════════════════════════════════════════
elif page == "Lab 8 · Performance Analytics":
    st.title("Student Performance Analytics")
    st.caption("Lab 8 · statistics module (mean, median, stdev) — same logic as NumPy/Pandas")
    st.markdown("---")

    CSV_FILE = "student_performance.csv"

    if st.button("Load CSV & Run Analytics"):
        if not os.path.exists(CSV_FILE):
            st.error(f"FileNotFoundError: '{CSV_FILE}' not found. Place it in the same folder as app.py.")
        else:
            try:
                with open(CSV_FILE, "r") as f:
                    lines = f.readlines()

                data = []
                for line in lines[1:]:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        data.append({
                            "name":    parts[0],
                            "math":    float(parts[1]),
                            "science": float(parts[2]),
                            "english": float(parts[3])
                        })

                if not data:
                    st.error("No data found in CSV.")
                else:
                    # Raw data
                    st.subheader("Raw Data (from CSV)")
                    for s in data:
                        avg = round((s["math"] + s["science"] + s["english"]) / 3, 1)
                        st.write(f"**{s['name']}** | Math: {s['math']} | Science: {s['science']} | English: {s['english']} | Avg: {avg}")

                    st.markdown("---")

                    # Stats
                    subjects = ["math", "science", "english"]
                    st.subheader("Statistical Summary (NumPy-equivalent)")
                    col1, col2, col3 = st.columns(3)
                    cols = [col1, col2, col3]
                    for i, subj in enumerate(subjects):
                        vals = [d[subj] for d in data]
                        mean   = round(statistics.mean(vals), 2)
                        median = round(statistics.median(vals), 2)
                        stdev  = round(statistics.stdev(vals), 2) if len(vals) > 1 else 0
                        cols[i].metric(subj.capitalize() + " Mean", mean)
                        cols[i].write(f"Median: {median}")
                        cols[i].write(f"Std Dev: {stdev}")

                    st.markdown("---")

                    # Top performers
                    st.subheader("Top Performers")
                    col1, col2, col3 = st.columns(3)
                    for col, subj in zip([col1, col2, col3], subjects):
                        top = max(data, key=lambda d: d[subj])
                        col.success(f"**{subj.capitalize()}**\n\n{top['name']} ({top[subj]})")

                    st.markdown("---")

                    # Bar chart using st.bar_chart
                    st.subheader("Average Scores per Subject (Bar Chart)")
                    chart_data = {
                        "Subject": ["Math", "Science", "English"],
                        "Average": [
                            round(statistics.mean([d["math"]    for d in data]), 2),
                            round(statistics.mean([d["science"] for d in data]), 2),
                            round(statistics.mean([d["english"] for d in data]), 2),
                        ]
                    }
                    import pandas as pd
                    df = pd.DataFrame(chart_data).set_index("Subject")
                    st.bar_chart(df)

            except Exception as e:
                st.error(f"Unexpected Error: {e}")
