// src/pages/Dashboard.jsx
import { useQuery } from "@tanstack/react-query";
import api from "../api.js";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const { data: courses = [] } = useQuery({
    queryKey: ["courses"],
    queryFn: () => api.get("/courses").then(res => res.data),
  });

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>

      <Link
        to="/courses"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mb-4 inline-block"
      >
        View All Courses
      </Link>

      <h2 className="text-xl font-semibold mt-6 mb-2">Course Details Links</h2>
      <ul className="flex flex-col gap-2">
        {courses.map(course => (
          <li key={course.id}>
            <Link
              to={`/course/${course.id}`}
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              {course.title} Details
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}