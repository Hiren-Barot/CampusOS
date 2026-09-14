import { http, getErrorMessage } from "./api";

export const DEFAULT_NEW_USER_PASSWORD = "changeme123";

export async function getUsers() {
  try {
    const response = await http.get("/users/?skip=0&limit=200");
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getUsersByRole(role) {
  try {
    const response = await http.get(`/users/?role=${role}&limit=200`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getUserById(id) {
  try {
    const response = await http.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function createUser(data) {
  try {
    const response = await http.post("/users/", {
      email: data.email,
      full_name: data.name,
      role: data.role,
      department_id: data.department_id || null,
    });
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function updateUser(id, data) {
  try {
    const payload = {};
    if (data.name) payload.full_name = data.name;
    if (data.email) payload.email = data.email;
    if (data.role) payload.role = data.role;
    if (data.department_id !== undefined) payload.department_id = data.department_id;

    const response = await http.put(`/users/${id}`, payload);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function deleteUser(id) {
  try {
    const response = await http.delete(`/users/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function searchUsers(query) {
  try {
    const response = await http.get(`/users/search?q=${encodeURIComponent(query)}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getUsersByDepartment(departmentId) {
  try {
    const response = await http.get(`/users/department/${departmentId}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}