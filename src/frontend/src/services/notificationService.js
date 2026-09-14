import { http, getErrorMessage } from "./api";

export async function getNotifications() {
  try {
    const response = await http.get("/notifications/");
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getUnreadNotifications() {
  try {
    const response = await http.get("/notifications/unread");
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getUnreadCount() {
  try {
    const response = await http.get("/notifications/unread/count");
    return response.data.count;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function markAsRead(id) {
  try {
    const response = await http.patch(`/notifications/${id}/read`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function markAllAsRead() {
  try {
    const response = await http.patch("/notifications/read-all");
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function deleteNotification(id) {
  try {
    const response = await http.delete(`/notifications/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}