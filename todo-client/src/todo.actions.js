// @ts-nocheck
import { setTodos } from "./stores/todo";

export async function getTodos(user_id) {
  const response = await fetch(`http://localhost:8000/todos/${user_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    console.log("Failed to fetch todo data");
  }
}

export async function addTodos(user_id, todo) {
  const response = await fetch(`http://localhost:8000/todos/add/${user_id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(todo),
  });
  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    console.log("Failed to add new todo");
  }
}

export async function invite_users(email, todo_id) {
  const response = await fetch(`http://localhost:8000/todo/invite`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, todo_id }),
  });
  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    console.log("Failed to invite new user");
  }
}

export async function invited_todos(user_id) {
  const response = await fetch(
    `http://localhost:8000/users/${user_id}/invited_todos_grouped`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    console.log("Failed to fetch invited todos");
  }
}

export async function update_done(todo_id) {
  const response = await fetch(`http://localhost:8000/todos/${todo_id}/done`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
  });
  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    console.log("Failed to update Done todo Status");
  }
}

export async function delete_todo(todo_id) {
  const response = await fetch(`http://localhost:8000/todos/${todo_id}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
  });
  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    console.log("Failed to delete Todo");
  }
}
