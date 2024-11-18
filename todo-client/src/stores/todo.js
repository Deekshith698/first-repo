// @ts-nocheck
import { writable } from "svelte/store";
import { getTodos, invited_todos } from "../todo.actions";
import { user } from "./auth";

export const todos = writable([]);

export async function setTodos(user_id) {
  let data = await getTodos(user_id);
  todos.set([data]);

  let invites = await invited_todos(user_id);
  todos.update((currentTodos) => [
    ...currentTodos,
    ...Object.values(invites)
      .map((todo) => [todo])
      .flat(),
  ]);
}
