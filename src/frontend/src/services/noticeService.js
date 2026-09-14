import { http, getErrorMessage } from "./api";

export async function getNotices() {
  try {
    const response = await http.get("/notices/");
    return response.data.map(mapNotice);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getMyNotices() {
  try {
    const response = await http.get("/notices/my");
    return response.data.map(mapNotice);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getNoticeById(id) {
  try {
    const response = await http.get(`/notices/${id}`);
    return mapNotice(response.data);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function createNotice(data) {
  try {
    const response = await http.post("/notices/", {
      title: data.title,
      content: data.content,
      department_id: data.department_id,
      is_published: true,
    });
    return mapNotice(response.data);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function updateNotice(id, data) {
  try {
    const response = await http.put(`/notices/${id}`, {
      title: data.title,
      content: data.content,
    });
    return mapNotice(response.data);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function deleteNotice(id) {
  try {
    const response = await http.delete(`/notices/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function searchNotices(query) {
  try {
    const response = await http.get(`/notices/search?q=${encodeURIComponent(query)}`);
    return response.data.map(mapNotice);
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

function mapNotice(n) {
  return {
    id: n.id,
    title: n.title,
    content: n.content,
    meta: n.faculty_name || "Unknown",
    tag: "EVENT",
    department_id: n.department_id,
    faculty_id: n.faculty_id,
    is_published: n.is_published,
    createdAt: n.created_at,
    updatedAt: n.updated_at,
  };
}