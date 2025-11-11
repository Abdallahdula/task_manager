from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/student')
def student_info():
    student_id = request.args.get('id')
    # Mock student data
    data = {
        "id": student_id,
        "name": "Abdallah Sadri Abdalla",
        "course": "Data Science",
        "year": 2,
        "Sgpa": 8.5
    }
    return jsonify(data)

@app.route('/api/students/count')
def student_count():
    # Mock total number of students
    total_students = 150
    return jsonify({"total_students": total_students})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
