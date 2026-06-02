from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    return jsonify(db.get_all_students()), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    student_data = request.get_json()

    if student_data is None:
        return jsonify({"error": "Request body must be JSON"}), 404
    
    required_fields = ["name", "course"]

    for field in required_fields:
        if field not in student_data:
            return jsonify({"error": f"Missing field: {field}"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if not isinstance(name, str) or name == "":
        return jsonify({"error": f"Invalid name"}), 404
    
    if not isinstance(course, str) or course == "":
        return jsonify({"error": f"Invalid course"}), 404
    
    if mark is not None:
        if not isinstance(mark, int):
            return jsonify({"error": f"Invalid mark"}), 404
        if not 0 <= mark <= 100:
            return jsonify({"error": f"Invalid mark"}), 404
    else:
        mark = -1

    result = db.insert_student(name, course, mark)
    return jsonify(result), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    if not isinstance(student_id, int):
        return jsonify({"error": "Invalid Student ID"}), 404
    # check student data existence
    student = db.get_student_by_id(student_id)
    
    if student == None:
        return jsonify({"error": "Invalid Student ID"}), 404
    
    # read request
    student_data = request.get_json()
    if student_data is None:
        return jsonify({"error": "Request body must be JSON"}), 404
    required_fields = ["name", "course"]

    for field in required_fields:
        if field not in student_data:
            return jsonify({"error": f"Missing field: {field}"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if not isinstance(name, str) or name == "":
        return jsonify({"error": f"Invalid name"}), 404
    
    if not isinstance(course, str) or course == "":
        return jsonify({"error": f"Invalid course"}), 404
    
    if mark is not None:
        if not isinstance(mark, int):
            return jsonify({"error": f"Invalid mark"}), 404
        if not 0 <= mark <= 100:
            return jsonify({"error": f"Invalid mark"}), 404
    else:
        mark = -1
    
    result = db.update_student(student["id"], name, course, mark)

    return result, 200

    


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    if not isinstance(student_id, int):
        return jsonify({"error": "Invalid Student ID"}), 404
    
    student_data = db.get_student_by_id(student_id)

    if student_data == None:
        return jsonify({"error": "Invalid Student ID"}), 404
    
    db.delete_student(student_id)
    return student_data, 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    student_db = db.get_all_students()
    valid_marks = list(map(lambda x: x["mark"], student_db))
    total_count = len(student_db)
    if len(student_db) == 0:
        result = {
            "count": 0,
            "average": 0,
            "min": 0,
            "max": 0
        }
        return jsonify(result), 200
    average = sum(valid_marks) / total_count
    min_mark = min(valid_marks)
    max_mark = max(valid_marks)
    result = {
        "count": total_count,
        "average": average,
        "min": min_mark,
        "max": max_mark
    }
    return jsonify(result), 200



@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
