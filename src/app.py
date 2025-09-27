"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory course database
courses = {
    "Python Programming": {
        "description": "Aprenda Python do zero e desenvolva projetos.",
        "students": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Matemática Avançada": {
        "description": "Resolução de problemas avançados e preparação para olimpíadas.",
        "students": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "História Mundial": {
        "description": "Explore eventos históricos e suas consequências.",
        "students": []
    }
}



@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


# Endpoints para cursos
@app.get("/courses")
def get_courses():
    """Retorna todos os cursos e seus alunos inscritos"""
    return courses


@app.post("/courses/{course_name}/enroll")
def enroll_student(course_name: str, email: str):
    """Inscreve um aluno em um curso"""
    if course_name not in courses:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    if email in courses[course_name]["students"]:
        raise HTTPException(status_code=400, detail="Aluno já inscrito")
    courses[course_name]["students"].append(email)
    return {"message": f"Aluno {email} inscrito no curso {course_name}"}


@app.delete("/courses/{course_name}/unenroll")
def unenroll_student(course_name: str, email: str):
    """Remove um aluno de um curso"""
    if course_name not in courses:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    if email not in courses[course_name]["students"]:
        raise HTTPException(status_code=400, detail="Aluno não está inscrito neste curso")
    courses[course_name]["students"].remove(email)
    return {"message": f"Aluno {email} removido do curso {course_name}"}


@app.get("/students/{email}/courses")
def get_student_courses(email: str):
    """Retorna todos os cursos em que o aluno está inscrito"""
    enrolled = [name for name, c in courses.items() if email in c["students"]]
    return {"email": email, "courses": enrolled}


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
