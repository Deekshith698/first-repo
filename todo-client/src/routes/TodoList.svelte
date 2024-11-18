<script>
  // @ts-nocheck
  import { user } from "../stores/auth";
  import { setTodos } from "../stores/todo";

  import { delete_todo, update_done } from "../todo.actions";
  import { send, receive } from "./transition";
  export let todos;
  export let done;

  async function updataDoneValue(todo_id) {
    await update_done(todo_id);
    await setTodos($user.id);
  }
</script>

<ul class="w-full">
  {#if todos}
    {#each todos.filter((/** @type {{ done: any; }} */ todo) => todo.done === done) as todo (todo.id)}
      <label class="m-4" class:done>
        <li
          class="card p-4 variant-ghost-warning flex gap-2 relative"
          in:receive={{ key: todo.id }}
          out:send={{ key: todo.id }}
        >
          <div>
            <div class="flex items-center gap-3 font-normal">
              <input
                type="checkbox"
                class="outline-none border-none rounded-sm"
                checked={todo.done}
                on:change={async () => {
                  await updataDoneValue(todo.id);
                }}
              />
              <span>{todo.description}</span>
            </div>
            <div class="flex gap-1 flex-wrap mt-3">
              {#each todo.tags as tag}
                <span class="badge variant-filled-secondary">{tag}</span>
              {/each}
            </div>
          </div>

          <button
            type="button"
            class="btn-icon absolute right-2 self-center"
            on:click={async () => {
              await delete_todo(todo.id);
              await setTodos($user.id);
            }}><img class="w-5" src="./delete.webp" alt="delete logo" /></button
          >
        </li>
      </label>
    {/each}
  {/if}
</ul>

<style>
  .done {
    opacity: 0.6;
    text-decoration: line-through;
  }
</style>
