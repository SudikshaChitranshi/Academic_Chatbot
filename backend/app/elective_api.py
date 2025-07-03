from app.recommendation_engine import (
    load_data, preprocess_students, build_interaction_matrix,
    train_svd_centered, recommend_courses
) 

def get_recommendations_from_csv(student_data):
    # Load & preprocess
    students, courses = load_data("app/Student_data.csv","app/Course_data.csv")
    students = preprocess_students(students)

    # Append the new student
    students = students.copy()
    students['Courses_taken'] = students['Courses_taken_ids'].str.split(';')
    students = students.reset_index(drop=True)
    students = students.append(student_data, ignore_index=True)

    # Build model & recommend
    interaction, student_idx_map, course_idx_map = build_interaction_matrix(students, courses)
    train_idx = list(range(len(students) - 1))
    predicted = train_svd_centered(interaction, train_idx)
    rec_df = recommend_courses(student_data['Student ID'], students, courses, predicted, student_idx_map, course_idx_map, top_n=3)

    return rec_df[['Course ID', 'Name', 'Domain', 'Difficulty']].to_dict(orient="records")
