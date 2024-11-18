// @ts-nocheck
import { writable } from "svelte/store";
import { setTodos } from "./todo";
import { goto } from "$app/navigation";

export const user = writable({
  id: null,
  name: null,
  email: null,
  invitedTodos: [],
});
export const isAuthenticated = writable(false);

export function setUser(data) {
  user.set({
    id: data.id,
    name: data.name,
    email: data.email,
    invitedTodos: data.invited_todos,
  });
  isAuthenticated.set(true);
  setTodos(data.id);
}

export function logOut() {
  document.cookie = "userData=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"; // Delete the cookie

  user.set({
    id: null,
    name: null,
    email: null,
    invitedTodos: [],
  });
  isAuthenticated.set(false);
}
