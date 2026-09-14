import { http, getErrorMessage } from "./api";

export async function getDepartments() {
  try {
    const response = await http.get("/departments/");
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getDepartmentById(id) {
  try {
    const response = await http.get(`/departments/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function createDepartment(data) {
  try {
    const response = await http.post("/departments/", {
      name: data.name,
      code: data.code || data.name.substring(0, 3).toUpperCase(),
      hod_id: data.hod_id || null,
    });
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function updateDepartment(id, data) {
  try {
    const response = await http.put(`/departments/${id}`, data);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function deleteDepartment(id) {
  try {
    const response = await http.delete(`/departments/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function searchDepartments(query) {
  try {
    const response = await http.get(`/departments/search?q=${encodeURIComponent(query)}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}