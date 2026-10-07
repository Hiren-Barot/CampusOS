import { http, getErrorMessage } from "./api";

export async function getQueries() {
  try {
    const response = await http.get("/queries/");
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getQueryById(id) {
  try {
    const response = await http.get(`/queries/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function createQuery(data) {
  try {
    const response = await http.post("/queries/", {
      title: data.title,
      description: data.description,
    });
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function replyToQuery(id, replyText) {
  try {
    const response = await http.post(`/queries/${id}/reply`, {
      reply: replyText,
    });
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function deleteQuery(id) {
  try {
    const response = await http.delete(`/queries/${id}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}