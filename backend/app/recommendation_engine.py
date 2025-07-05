# recommendation_engine.py

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.sparse.linalg import svds

def load_data(student_path, courses_path):
    students = pd.read_csv(student_path)
    courses = pd.read_csv(courses_path)
    return students, courses

def preprocess_students(students):
    students = students.dropna(subset=['CGPA', 'Preferences', 'Courses_taken_ids'])
    students['Courses_taken'] = students['Courses_taken_ids'].str.split(';')
    students = students.reset_index(drop=True)
    return students

def build_interaction_matrix(students, courses):
    student_ids = students['Student ID'].tolist()
    course_ids = courses['Course ID'].tolist()
    student_idx_map = {sid: i for i, sid in enumerate(student_ids)}
    course_idx_map = {cid: i for i, cid in enumerate(course_ids)}

    interaction = np.zeros((len(student_ids), len(course_ids)))
    for i, row in students.iterrows():
        for cid in row['Courses_taken']:
            if cid in course_idx_map:
                interaction[student_idx_map[row['Student ID']], course_idx_map[cid]] = 1
    return interaction, student_idx_map, course_idx_map

def train_svd_centered(interaction, train_idx, k=20):
    train_interaction = interaction[train_idx, :]
    user_means = train_interaction.mean(axis=1, keepdims=True)
    train_interaction_centered = train_interaction - user_means
    U, sigma, Vt = svds(train_interaction_centered, k=k)
    sigma = np.diag(sigma)
    pred_centered = np.dot(np.dot(U, sigma), Vt)
    pred = pred_centered + user_means

    full_pred = np.zeros_like(interaction)
    full_pred[train_idx] = pred

    course_means = train_interaction.mean(axis=0)
    test_idx = [i for i in range(interaction.shape[0]) if i not in train_idx]
    for idx in test_idx:
        full_pred[idx] = course_means

    return full_pred

def recommend_courses(student_id, students, courses, predicted_interaction, student_idx_map, course_idx_map, top_n=3):
    idx = student_idx_map[student_id]
    student_row = predicted_interaction[idx]
    taken_courses = set(students.loc[idx, 'Courses_taken'])
    pref_domain = students.loc[idx, 'Preferences']

    course_scores = [
        (courses.iloc[j]['Course ID'], score)
        for j, score in enumerate(student_row)
        if (courses.iloc[j]['Course ID'] not in taken_courses) and 
           (courses.iloc[j]['Domain'] == pref_domain)
    ]
    course_scores.sort(key=lambda x: -x[1])
    recommended_ids = [cid for cid, _ in course_scores[:top_n]]
    return courses[courses['Course ID'].isin(recommended_ids)]
