// src/pages/CoursesPage.jsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../api.js";
import { useState } from "react";
import { Link } from "react-router-dom";

export default function CoursesPage() {
  const queryClient = useQueryClient();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const { data: courses = [] } = useQuery({
    queryKey: ["courses"],
    queryFn: () => api.get("/courses").then(res => res.data),
  });

  const createCourseMutation = useMutation({
    mutationFn: (newCourse) => api.post("/courses", newCourse).then(res => res.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["courses"] }),
  });

  const handleCreateCourse = () => {
    createCourseMutation.mutate({ title, description });
    setTitle("");
    setDescription("");
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Courses</h2>

      <div className="mb-4 flex gap-2">
        <input
          placeholder="Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          className="border p-1"
        />
        <input
          placeholder="Description"
          value={description}
          onChange={e => setDescription(e.target.value)}
          className="border p-1"
        />
        <button
          className="bg-blue-500 text-white px-2 rounded"
          onClick={handleCreateCourse}
        >
          Create Course
        </button>
      </div>

      <ul className="flex flex-col gap-2">
        {courses.map(course => (
          <li key={course.id}>
            <Link to={`/course/${course.id}`} className="text-blue-600">
              {course.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}