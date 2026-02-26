// src/pages/CourseDetail.jsx
import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../api.js";
import { useState } from "react";

export default function CourseDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: course } = useQuery({
    queryKey: ["course", id],
    queryFn: () => api.get(`/courses/${id}`).then(res => res.data),
  });

  const { data: lectures = [] } = useQuery({
    queryKey: ["lectures", id],
    queryFn: () => api.get(`/courses/${id}/lectures`).then(res => res.data),
  });

  const { data: exercises = [] } = useQuery({
    queryKey: ["exercises", id],
    queryFn: () => api.get(`/courses/${id}/exercises`).then(res => res.data),
  });

  // -----------------------------
  // STATE
  // -----------------------------

  const [lectureTitle, setLectureTitle] = useState("");
  const [lectureContent, setLectureContent] = useState("");
  const [lectureSection, setLectureSection] = useState("");
  const [lectureOrder, setLectureOrder] = useState(1);

  const [exerciseTitle, setExerciseTitle] = useState("");
  const [exerciseDesc, setExerciseDesc] = useState("");
  const [exerciseSection, setExerciseSection] = useState("");
  const [exerciseOrder, setExerciseOrder] = useState(1);

  // -----------------------------
  // CREATE MUTATIONS
  // -----------------------------

  const createLecture = useMutation({
    mutationFn: (payload) =>
      api.post("/lectures/", payload).then(res => res.data),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["lectures", id] }),
  });

  const createExercise = useMutation({
    mutationFn: (payload) =>
      api.post("/exercises/", payload).then(res => res.data),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["exercises", id] }),
  });

  // -----------------------------
  // DELETE MUTATIONS
  // -----------------------------

  const deleteLecture = useMutation({
    mutationFn: (lectureId) => api.delete(`/lectures/${lectureId}`),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["lectures", id] }),
  });

  const deleteExercise = useMutation({
    mutationFn: (exerciseId) => api.delete(`/exercises/${exerciseId}`),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["exercises", id] }),
  });

  // -----------------------------
  // HANDLERS
  // -----------------------------

  const handleCreateLecture = () => {
    createLecture.mutate({
      title: lectureTitle,
      content: lectureContent,
      course_id: id,
      section: lectureSection,
      order_index: lectureOrder,
    });

    setLectureTitle("");
    setLectureContent("");
    setLectureSection("");
    setLectureOrder(1);
  };

  const handleCreateExercise = () => {
    createExercise.mutate({
      title: exerciseTitle,
      description: exerciseDesc,
      starter_code: "",
      course_id: id,
      section: exerciseSection,
      order_index: exerciseOrder,
    });

    setExerciseTitle("");
    setExerciseDesc("");
    setExerciseSection("");
    setExerciseOrder(1);
  };

  // -----------------------------
  // UI
  // -----------------------------

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">{course?.title}</h2>

      {/* ========================= */}
      {/* LECTURES TABLE */}
      {/* ========================= */}

      <div className="mb-6">
        <h3 className="font-semibold mb-2">Lectures</h3>

        <div className="overflow-x-auto">
          <table className="border-collapse border border-gray-300 mb-4 min-w-[600px]">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2">Section</th>
                <th className="border p-2">Title</th>
                <th className="border p-2">Content</th>
                <th className="border p-2">Order</th>
                <th className="border p-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {lectures.map(l => (
                <tr key={l.id}>
                  <td className="border p-2">{l.section}</td>
                  <td className="border p-2">{l.title}</td>
                  <td className="border p-2">{l.content}</td>
                  <td className="border p-2">{l.order_index}</td>
                  <td className="border p-2 text-center">
                    <button
                      className="text-red-600 font-bold"
                      onClick={() => deleteLecture.mutate(l.id)}
                    >
                      X
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="flex gap-2 mb-4">
          <input
            placeholder="Title"
            value={lectureTitle}
            onChange={e => setLectureTitle(e.target.value)}
            className="border p-1"
          />
          <input
            placeholder="Content"
            value={lectureContent}
            onChange={e => setLectureContent(e.target.value)}
            className="border p-1"
          />
          <input
            placeholder="Section"
            value={lectureSection}
            onChange={e => setLectureSection(e.target.value)}
            className="border p-1"
          />
          <input
            type="number"
            placeholder="Order"
            value={lectureOrder}
            onChange={e => setLectureOrder(Number(e.target.value))}
            className="border p-1"
          />
          <button
            className="bg-green-500 text-white px-2 rounded"
            onClick={handleCreateLecture}
          >
            Add Lecture
          </button>
        </div>
      </div>

      {/* ========================= */}
      {/* EXERCISES TABLE */}
      {/* ========================= */}

      <div>
        <h3 className="font-semibold mb-2">Exercises</h3>

        <div className="overflow-x-auto">
          <table className="border-collapse border border-gray-300 mb-4 min-w-[700px]">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2">Section</th>
                <th className="border p-2">Title</th>
                <th className="border p-2">Description</th>
                <th className="border p-2">Order</th>
                <th className="border p-2">Delete</th>
                <th className="border p-2">Test Cases</th>
              </tr>
            </thead>
            <tbody>
              {exercises.map(e => (
                <tr key={e.id}>
                  <td className="border p-2">{e.section}</td>
                  <td className="border p-2">{e.title}</td>
                  <td className="border p-2">{e.description}</td>
                  <td className="border p-2">{e.order_index}</td>

                  {/* Delete */}
                  <td className="border p-2 text-center">
                    <button
                      className="text-red-600 font-bold"
                      onClick={() => deleteExercise.mutate(e.id)}
                    >
                      X
                    </button>
                  </td>

                  {/* Manage Test Cases */}
                  <td className="border p-2 text-center">
                    <button
                      className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                      onClick={() =>
                        navigate(`/exercises/${e.id}/test-cases`)
                      }
                    >
                      Manage
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="flex gap-2">
          <input
            placeholder="Title"
            value={exerciseTitle}
            onChange={e => setExerciseTitle(e.target.value)}
            className="border p-1"
          />
          <input
            placeholder="Description"
            value={exerciseDesc}
            onChange={e => setExerciseDesc(e.target.value)}
            className="border p-1"
          />
          <input
            placeholder="Section"
            value={exerciseSection}
            onChange={e => setExerciseSection(e.target.value)}
            className="border p-1"
          />
          <input
            type="number"
            placeholder="Order"
            value={exerciseOrder}
            onChange={e => setExerciseOrder(Number(e.target.value))}
            className="border p-1"
          />
          <button
            className="bg-purple-500 text-white px-2 rounded"
            onClick={handleCreateExercise}
          >
            Add Exercise
          </button>
        </div>
      </div>
    </div>
  );
}