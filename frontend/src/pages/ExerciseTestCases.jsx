import { useParams } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../api";
import { useState } from "react";

export default function ExerciseTestCases() {
  const { exerciseId } = useParams();
  const queryClient = useQueryClient();

  const [inputData, setInputData] = useState("");
  const [expectedOutput, setExpectedOutput] = useState("");

  // --- FETCH TEST CASES ---
  const { data: testCases = [] } = useQuery({
    queryKey: ["testCases", exerciseId],
    queryFn: () =>
      api
        .get(`/exercises/${exerciseId}/test-cases`)
        .then((res) => res.data),
  });

  // --- CREATE TEST CASE ---
  const createTestCase = useMutation({
    mutationFn: (payload) =>
      api.post("/exercise-test-cases/", payload).then((res) => res.data),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["testCases", exerciseId] }),
  });

  // --- DELETE TEST CASE ---
  const deleteTestCase = useMutation({
    mutationFn: (id) => api.delete(`/exercise-test-cases/${id}`),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["testCases", exerciseId] }),
  });

  const handleCreate = () => {
    createTestCase.mutate({
      exercise_id: exerciseId,
      input_data: inputData,
      expected_output: expectedOutput,
    });

    setInputData("");
    setExpectedOutput("");
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Exercise Test Cases</h2>

      {/* Test Cases Table */}
      <div className="overflow-x-auto mb-6">
        <table className="border-collapse border border-gray-300 min-w-[600px]">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2">Input</th>
              <th className="border p-2">Expected Output</th>
              <th className="border p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {testCases.map((tc) => (
              <tr key={tc.id}>
                <td className="border p-2">{tc.input_data}</td>
                <td className="border p-2">{tc.expected_output}</td>
                <td className="border p-2 text-center">
                  <button
                    className="text-red-600 font-bold"
                    onClick={() => deleteTestCase.mutate(tc.id)}
                  >
                    X
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Add Test Case */}
      <div className="flex gap-2">
        <input
          placeholder="Input data"
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          className="border p-2"
        />
        <input
          placeholder="Expected output"
          value={expectedOutput}
          onChange={(e) => setExpectedOutput(e.target.value)}
          className="border p-2"
        />
        <button
          className="bg-green-500 text-white px-4 rounded hover:bg-green-600"
          onClick={handleCreate}
        >
          Add
        </button>
      </div>
    </div>
  );
}