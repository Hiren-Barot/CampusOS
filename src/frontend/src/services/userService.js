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
    const payload = {
      email: data.email,
      full_name: data.name,
      role: data.role,
      department_id: data.department_id || null,
    };

    if (data.profile) {
      const profile = {};
      Object.keys(data.profile).forEach((key) => {
        const val = data.profile[key];
        if (val !== "" && val !== null && val !== undefined) {
          if (key === "semester" || key === "admission_year" || key === "experience_years") {
            profile[key] = Number(val);
          } else {
            profile[key] = val;
          }
        }
      });
      if (Object.keys(profile).length > 0) {
        payload.profile = profile;
      }
    }

    const response = await http.post("/users/", payload);
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
    if (data.is_active !== undefined) payload.is_active = data.is_active;

    if (data.profile) {
      const profile = {};
      Object.keys(data.profile).forEach((key) => {
        const val = data.profile[key];
        if (val !== "" && val !== null && val !== undefined) {
          if (key === "semester" || key === "admission_year" || key === "experience_years") {
            profile[key] = Number(val);
          } else {
            profile[key] = val;
          }
        } else {
          profile[key] = null;
        }
      });
      payload.profile = profile;
    }

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