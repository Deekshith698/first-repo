// @ts-nocheck
import { writable } from "svelte/store";
import { getTodos } from "./todo.actions";
import { user } from "./stores/auth";

export const createTodos = () => {
  let uuid = 0;
  const todos = getTodos(user.id);

  const { subscribe, update } = writable(todos);

  return {
    subscribe,
    add: (description, tags) => {
      const todo = {
        id: uuid++,
        description: description,
        tags: tags,
        done: false,
      };

      update(($todos) => [...$todos, todo]);
    },
    remove: (todo) => {
      update($todos.filter((t) => t !== todo));
    },
    mark: (todo, done) => {
      update(($todos) => [
        ...$todos.filter((t) => t !== todo),
        { ...todo, done },
      ]);
    },
  };
};
