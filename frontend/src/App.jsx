// src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard.jsx";
import CoursesPage from "./pages/CoursesPage.jsx";
import CourseDetail from "./pages/CourseDetail.jsx";
import ExerciseTestCases from "./pages/ExerciseTestCases.jsx";

export default function App() {
  return (
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/courses" element={<CoursesPage />} />
    <Route path="/course/:id" element={<CourseDetail />} />
    <Route
      path="/exercises/:exerciseId/test-cases"
      element={<ExerciseTestCases />}
    />
  </Routes>
</BrowserRouter>
  );
}