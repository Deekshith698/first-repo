<script>
  // @ts-nocheck

  import { focusTrap } from "@skeletonlabs/skeleton";
  import { setUser } from "../../stores/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  let name = "";
  let password = "";
  let email = "";

  async function handleRegister() {
    const response = await fetch("http://localhost:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    });
    if (response.ok) {
      const data = await response.json();
      setUser(data);
      document.cookie = `userData=${encodeURIComponent(JSON.stringify(data))}; path=/; max-age=86400`;
      goto("/");
    } else {
      alert("Login failed");
    }
  }

  onMount(() => {
    const userData = document.cookie
      .split("; ")
      .find((row) => row.startsWith("userData="))
      ?.split("=")[1];

    if (userData) {
      setUser(JSON.parse(decodeURIComponent(userData)));
      goto("/");
    }
  });
</script>

<div class="flex justify-center items-center h-full pb-44">
  <form on:submit={handleRegister} class="w-1/2" use:focusTrap={true}>
    <div class="mb-5">
      <label
        for="name"
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
        >Your Name</label
      >
      <input
        type="name"
        bind:value={name}
        id="name"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="your name"
        required
      />
    </div>
    <div class="mb-5">
      <label
        for="email"
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
        >Your email</label
      >
      <input
        type="email"
        bind:value={email}
        id="email"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="name@flowbite.com"
        required
      />
    </div>
    <div class="mb-5">
      <label
        for="password"
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
        >Your password</label
      >
      <input
        type="password"
        bind:value={password}
        id="password"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        required
      />
    </div>
    <div class="mb-3">
      Have an account? <a href="/login" class="underline font-bold">login</a>
    </div>

    <button
      type="submit"
      class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >Submit</button
    >
  </form>
</div>
