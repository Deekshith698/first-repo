<script lang="ts">
  import { InputChip } from "@skeletonlabs/skeleton";
  import { createTodos } from "../todoStore";
  import TodoList from "./TodoList.svelte";
  import { addTodos } from "../todo.actions";
  import { setTodos } from "../stores/todo";
  import { user } from "../stores/auth";

  export let todos;

  let content: string = "";
  let tags: string[];

  const createNote = async () => {
    await addTodos(todos[0].user_id, {
      description: content,
      tags: tags,
      done: false,
    });

    await setTodos($user.id);

    content = "";
    tags = [];
  };
</script>

<svelte:head>
  <title>ToDoDo</title>
  <meta name="description" content="ToDo Application" />
</svelte:head>

<section
  class="container mx-auto my-10 flex flex-col justify-start items-center px-4"
>
  <div class="container gap-5 flex flex-col">
    <textarea
      bind:value={content}
      class="textarea bg-primary-50"
      rows="5"
      placeholder="Add your notes"
    />
    <InputChip
      name="tags"
      bind:value={tags}
      class="bg-primary-200 p-4"
      placeholder="Tag anything"
    />
    <button
      type="button"
      on:click={createNote}
      class="btn variant-ghost-primary self-end">Create Note</button
    >
  </div>

  <div class="flex justify-around max-md:flex-wrap w-full mt-10 gap-4 text-xl">
    <div class="flex flex-col items-center w-full">
      <h1>ToDo</h1>
      <TodoList {todos} done={false} />
    </div>
    <div class=" flex flex-col items-center w-full">
      <h1>Done</h1>
      <TodoList {todos} done={true} />
    </div>
  </div>
</section>
