import { http, getErrorMessage, setToken, clearToken, getStoredUser, setStoredUser } from "./api";

export async function login(email, password) {
  if (!email || !password) {
    throw new Error("Email and password are required");
  }

  try {
    const response = await http.post("/auth/login", { email, password });
    const { access_token, must_change_password } = response.data;

    setToken(access_token);

    const userResponse = await http.get("/auth/me");
    const user = {
      ...userResponse.data,
      must_change_password,
    };

    setStoredUser(user);
    return user;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function register({ name, email, password }) {
  if (!name || !email || !password) {
    throw new Error("Name, email and password are required");
  }

  try {
    const response = await http.post("/auth/register", {
      email,
      password,
      full_name: name,
    });

    const { access_token } = response.data;
    setToken(access_token);

    const userResponse = await http.get("/auth/me");
    const user = userResponse.data;

    setStoredUser(user);
    return user;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export function logout() {
  clearToken();
}

export function getCurrentUser() {
  return getStoredUser();
}

export async function fetchCurrentUser() {
  try {
    const response = await http.get("/auth/me");
    const user = response.data;
    setStoredUser(user);
    return user;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function changePassword(currentPassword, newPassword) {
  try {
    const response = await http.post("/auth/change-password", {
      current_password: currentPassword,
      new_password: newPassword,
    });
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}