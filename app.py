from flask import Flask, render_template, request
import os

app = Flask(__name__)

# ── Lab 1 logic ──────────────────────────────────────────────
def get_grade(score):
    if score >= 90:
        return "A", "Excellent"
    elif score >= 75:
        return "B", "Very Good"
    elif score >= 60:
        return "C", "Good"
    elif score >= 40:
        return "D", "Average"
    else:
        return "F", "Needs Improvement"

# ── Lab 4 logic ──────────────────────────────────────────────
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

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# ── In-memory storage (resets on restart) ────────────────────
courses = []       # Lab 2
students = []      # Lab 3
file_records = []  # Lab 6

# ── Routes ───────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

# Lab 1
@app.route("/lab1", methods=["GET", "POST"])
def lab1():
    result = None
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        score_raw = request.form.get("score", "")
        if not name:
            error = "Please enter a student name."
        else:
            try:
                score = float(score_raw)
                if not (0 <= score <= 100):
                    error = "Score must be between 0 and 100."
                else:
                    grade, remark = get_grade(score)
                    result = {"name": name, "score": score, "grade": grade, "remark": remark}
            except ValueError:
                error = "Please enter a valid numeric score."
    return render_template("lab1.html", result=result, error=error)

# Lab 2
@app.route("/lab2", methods=["GET", "POST"])
def lab2():
    error = None
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            name = request.form.get("course_name", "").strip()
            credits_raw = request.form.get("credits", "")
            if not name:
                error = "Course name cannot be empty."
            elif len(courses) >= 5:
                error = "Maximum 5 courses allowed (break condition reached)."
            elif not credits_raw.isdigit() or int(credits_raw) <= 0:
                error = "Credits must be a positive integer (continue skips this)."
            else:
                courses.append({"name": name, "credits": int(credits_raw)})
        elif action == "clear":
            courses.clear()
    total_credits = sum(c["credits"] for c in courses)
    return render_template("lab2.html", courses=courses, total_credits=total_credits, error=error)

# Lab 3
@app.route("/lab3", methods=["GET", "POST"])
def lab3():
    error = None
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            name = request.form.get("name", "").strip()
            age_raw = request.form.get("age", "")
            grades_raw = request.form.get("grades", "")
            if not name:
                error = "Name cannot be empty."
            else:
                try:
                    age = int(age_raw)
                    grades = [float(g.strip()) for g in grades_raw.split(",") if g.strip()]
                    if not grades:
                        error = "Enter at least one grade."
                    else:
                        avg = round(sum(grades) / len(grades), 2)
                        students.append({"name": name, "age": age, "grades": grades, "avg": avg})
                except ValueError:
                    error = "Invalid age or grades."
        elif action == "clear":
            students.clear()

    # Set operations
    event_A = {"Priya", "Rahul", "Anita", "Kiran"}
    event_B = {"Rahul", "Anita", "Sneha"}
    sets = {
        "A": sorted(event_A),
        "B": sorted(event_B),
        "common": sorted(event_A & event_B),
        "only_A": sorted(event_A - event_B),
        "all": sorted(event_A | event_B),
    }
    return render_template("lab3.html", students=students, sets=sets, error=error)

# Lab 4
@app.route("/lab4", methods=["GET", "POST"])
def lab4():
    result = None
    error = None
    if request.method == "POST":
        ids_raw = request.form.get("ids", "")
        target_raw = request.form.get("target", "")
        try:
            ids = [int(x.strip()) for x in ids_raw.split(",") if x.strip()]
            target = int(target_raw)
            if len(ids) < 2:
                error = "Enter at least 2 IDs."
            else:
                bs = bubble_sort(ids)
                ss = selection_sort(ids)
                li = linear_search(ids, target)
                bi = binary_search(bs, target)
                result = {
                    "original": ids, "bubble": bs, "selection": ss,
                    "target": target,
                    "linear": li, "binary": bi
                }
        except ValueError:
            error = "Enter valid comma-separated integers."
    return render_template("lab4.html", result=result, error=error)

# Lab 5
@app.route("/lab5", methods=["GET", "POST"])
def lab5():
    result = None
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip() or "Student"
        try:
            tuition   = float(request.form.get("tuition", 0) or 0)
            hostel    = float(request.form.get("hostel", 0) or 0)
            transport = float(request.form.get("transport", 0) or 0)
            if tuition <= 0:
                error = "Please enter a valid tuition fee."
            else:
                total = tuition + hostel + transport
                result = {"name": name, "tuition": tuition, "hostel": hostel,
                          "transport": transport, "total": total}
        except ValueError:
            error = "Enter valid numeric fee values."
    return render_template("lab5.html", result=result, error=error)

# Lab 6
@app.route("/lab6", methods=["GET", "POST"])
def lab6():
    error = None
    report = None
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            name = request.form.get("name", "").strip()
            marks_raw = request.form.get("marks", "")
            if not name:
                error = "Name cannot be empty."
            else:
                try:
                    marks = int(marks_raw)
                    if not (0 <= marks <= 100):
                        error = "Marks must be between 0 and 100."
                    else:
                        sid = 101 + len(file_records)
                        _, remark = get_grade(marks)
                        file_records.append({"id": sid, "name": name, "marks": marks, "remark": remark})
                except ValueError:
                    error = "Enter a valid integer for marks."
        elif action == "clear":
            file_records.clear()
        elif action == "report" and file_records:
            total = len(file_records)
            avg = round(sum(r["marks"] for r in file_records) / total, 2)
            top = max(file_records, key=lambda r: r["marks"])
            low = min(file_records, key=lambda r: r["marks"])
            report = {"total": total, "avg": avg, "top": top, "low": low}
    return render_template("lab6.html", records=file_records, report=report, error=error)

# Lab 7
@app.route("/lab7", methods=["GET", "POST"])
def lab7():
    tree = None
    error = None
    path = ""
    if request.method == "POST":
        path = request.form.get("path", "").strip()
        if not path:
            error = "Please enter a directory path."
        elif not os.path.exists(path):
            error = f"FileNotFoundError: Invalid directory path: '{path}'"
        elif not os.path.isdir(path):
            error = f"NotADirectoryError: '{path}' is not a directory."
        else:
            tree = []
            warnings = []
            for root, dirs, files in os.walk(path):
                level = root.replace(path, "").count(os.sep)
                tree.append({"indent": level, "name": os.path.basename(root), "type": "folder"})
                for f in files:
                    tree.append({"indent": level + 1, "name": f, "type": "file"})
                if not files and not dirs:
                    warnings.append(f"MissingFileOrFolderError: Empty folder: '{root}'")
            tree_data = {"items": tree, "warnings": warnings}
            tree = tree_data
    return render_template("lab7.html", tree=tree, error=error, path=path)

# Lab 8
@app.route("/lab8", methods=["GET", "POST"])
def lab8():
    result = None
    error = None
    csv_data = []

    CSV_FILE = "student_performance.csv"

    if request.method == "POST":
        action = request.form.get("action")
        if action == "load":
            # Load from CSV
            if not os.path.exists(CSV_FILE):
                error = f"'{CSV_FILE}' not found. Make sure it's in the same folder as app.py."
            else:
                try:
                    with open(CSV_FILE, "r") as f:
                        lines = f.readlines()
                    headers = lines[0].strip().split(",")
                    for line in lines[1:]:
                        parts = line.strip().split(",")
                        if len(parts) == 4:
                            csv_data.append({
                                "name": parts[0],
                                "math": float(parts[1]),
                                "science": float(parts[2]),
                                "english": float(parts[3])
                            })
                    if not csv_data:
                        error = "No data found in CSV."
                    else:
                        result = compute_analytics(csv_data)
                except Exception as e:
                    error = f"Error reading CSV: {e}"

    return render_template("lab8.html", result=result, error=error)

def compute_analytics(data):
    import statistics
    subjects = ["math", "science", "english"]
    stats = {}
    for s in subjects:
        vals = [d[s] for d in data]
        stats[s] = {
            "mean":   round(sum(vals) / len(vals), 2),
            "median": round(statistics.median(vals), 2),
            "stdev":  round(statistics.stdev(vals), 2) if len(vals) > 1 else 0
        }
    tops = {s: max(data, key=lambda d: d[s]) for s in subjects}
    return {"data": data, "stats": stats, "tops": tops}


if __name__ == "__main__":
    app.run(debug=True)
