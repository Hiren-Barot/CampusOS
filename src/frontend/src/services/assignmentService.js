import { http, getErrorMessage } from "./api";

export async function getAssignments() {
  try {
    const response = await http.get("/assignments/");
    return response.data.map(mapAssignment);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getAssignmentById(id) {
  try {
    const response = await http.get(`/assignments/${id}`);
    return mapAssignment(response.data);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function createAssignment(data) {
  try {
    const response = await http.post("/assignments/", {
      title: data.title,
      description: data.description || "",
      department_id: data.department_id,
      deadline: data.dueDate,
    });
    return mapAssignment(response.data);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function updateAssignment(id, data) {
  try {
    const response = await http.put(`/assignments/${id}`, {
      title: data.title,
      description: data.description,
      deadline: data.dueDate,
    });
    return mapAssignment(response.data);
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

export async function getUpcomingAssignments() {
  try {
    const response = await http.get("/assignments/upcoming");
    return response.data.map(mapAssignment);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function searchAssignments(query) {
  try {
    const response = await http.get(`/assignments/search?q=${encodeURIComponent(query)}`);
    return response.data.map(mapAssignment);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

function mapAssignment(a) {
  return {
    id: a.id,
    title: a.title,
    description: a.description,
    by: a.faculty_name || "Unknown",  
    dueDate: a.deadline,                
    department_id: a.department_id,
    faculty_id: a.faculty_id,
    createdAt: a.created_at,
  };
}