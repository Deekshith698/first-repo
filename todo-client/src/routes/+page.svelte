<script lang="ts">
  import Todo from "./Todo.svelte";
  import { LightSwitch } from "@skeletonlabs/skeleton";
  import { AppRail, AppRailTile, Avatar } from "@skeletonlabs/skeleton";

  import { setTodos, todos } from "../stores/todo";
  import { onMount } from "svelte";
  import { logOut, user } from "../stores/auth";
  import { popup } from "@skeletonlabs/skeleton";
  import type { PopupSettings } from "@skeletonlabs/skeleton";
  import { goto } from "$app/navigation";
  import { Modal, getModalStore } from "@skeletonlabs/skeleton";
  import type {
    ModalSettings,
    ModalComponent,
    ModalStore,
  } from "@skeletonlabs/skeleton";
  import { invite_users } from "../todo.actions";

  const modalStore = getModalStore();

  let currentTile: number = 0;

  onMount(() => {
    if (user && $todos.length == 0) setTodos($user.id);
  });

  const popupFeatured: PopupSettings = {
    // Represents the type of event that opens/closed the popup
    event: "click",
    // Matches the data-popup value on your popup element
    target: "popupFeatured",
    // Defines which side of your trigger the popup will appear
    placement: "top",
  };

  const modal: ModalSettings = {
    type: "prompt",
    // Data
    title: "Invite your buddy",
    body: "Provide the email of your buddy in the field below.",
    // Populates the input value and attributes
    valueAttr: { type: "email", required: true },
    // Returns the updated response value
    response: (email: string) => invite_users(email, $user.id),
  };
</script>

<div class="flex h-screen overflow-auto">
  <AppRail class="w-40">
    <!-- --- -->
    <div class="p-8 flex items-center justify-center sticky top-0 bg-white">
      <LightSwitch />
    </div>

    {#each $todos as todo, index}
      <AppRailTile
        bind:group={currentTile}
        name="todo"
        value={index}
        title="todo"
        on:click={() => (currentTile = currentTile)}
      >
        <svelte:fragment slot="lead"
          >{#if index == 0}<span class="font-bold text-lg">Your Todo</span>
          {:else}<span class="font-bold text-lg">Invited Todo</span
            >{/if}</svelte:fragment
        >
        <span>Todo Id: {index + 1}</span>
      </AppRailTile>
    {/each}

    <!-- --- -->
    <button
      class="absolute bottom-0 w-[140px] p-8 flex justify-center items-center bg-white z-20 btn"
      use:popup={popupFeatured}
    >
      <Avatar src="" width="w-20" rounded="rounded-full" />
      <div class="card p-4 w-72 shadow-xl" data-popup="popupFeatured">
        <Avatar src="" class="w-20 m-auto my-3" rounded="rounded-full" />
        <div>{$user.name}</div>
        <div>{$user.email}</div>
        <div>
          <button
            class="btn bg-secondary-500 text-white rounded-md w-full my-3"
            on:click={() => {
              modalStore.trigger(modal);
            }}
            >Invite
          </button>
        </div>
        <div>
          <button
            class="btn bg-error-500 text-white rounded-md w-full"
            on:click={() => {
              logOut();
              goto("/login");
            }}
            >LogOut
          </button>
        </div>
        <div class="arrow bg-surface-100-800-token" />
      </div>
    </button>
  </AppRail>

  <div class="flex justify-center min-h-[80vh] w-full my-14">
    <div class="flex items-start badge variant-soft w-4/5 rounded-md">
      {#if todos}
        {#key currentTile}
          <Todo todos={$todos[currentTile]} />
        {/key}
      {/if}
    </div>
  </div>
</div>
