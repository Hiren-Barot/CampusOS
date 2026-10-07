import { http, getErrorMessage } from "./api";

export async function getAssignments() {
  try {
    const response = await http.get("/assignments/?skip=0&limit=200");
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getMyAssignments() {
  try {
    const response = await http.get("/assignments/my");
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getUpcomingAssignments() {
  try {
    const response = await http.get("/assignments/upcoming");
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getAssignmentById(id) {
  try {
    const response = await http.get(`/assignments/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function createAssignment(data) {
  try {
    const formData = new FormData();
    formData.append("title", data.title);
    if (data.description) formData.append("description", data.description);
    formData.append("deadline", data.deadline);
    if (data.department_id) formData.append("department_id", String(data.department_id));
    if (data.file) formData.append("file", data.file);

    const response = await http.post("/assignments/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function updateAssignment(id, data) {
  try {
    const response = await http.put(`/assignments/${id}`, data);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function deleteAssignment(id) {
  try {
    const response = await http.delete(`/assignments/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function searchAssignments(query) {
  try {
    const response = await http.get(`/assignments/search?q=${encodeURIComponent(query)}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function downloadAssignmentFile(id, fileName) {
  try {
    const response = await http.get(`/assignments/${id}/download`, {
      responseType: "blob",
    });

    const blob = new Blob([response.data]);
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName || `assignment-${id}`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}