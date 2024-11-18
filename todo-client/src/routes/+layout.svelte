<script lang="ts">
  import "../app.postcss";
  import { AppShell } from "@skeletonlabs/skeleton";

  // Highlight JS
  import hljs from "highlight.js/lib/core";
  import "highlight.js/styles/github-dark.css";
  import { storeHighlightJs } from "@skeletonlabs/skeleton";
  import xml from "highlight.js/lib/languages/xml"; // for HTML
  import css from "highlight.js/lib/languages/css";
  import javascript from "highlight.js/lib/languages/javascript";
  import typescript from "highlight.js/lib/languages/typescript";
  import { page } from "$app/stores";

  hljs.registerLanguage("xml", xml); // for HTML
  hljs.registerLanguage("css", css);
  hljs.registerLanguage("javascript", javascript);
  hljs.registerLanguage("typescript", typescript);
  storeHighlightJs.set(hljs);

  // Floating UI for Popups
  import {
    computePosition,
    autoUpdate,
    flip,
    shift,
    offset,
    arrow,
  } from "@floating-ui/dom";
  import { storePopup } from "@skeletonlabs/skeleton";
  storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

  import { isAuthenticated } from "../stores/auth";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { initializeStores, Modal } from "@skeletonlabs/skeleton";

  initializeStores();

  let currentPath: string;

  $: page.subscribe((p) => {
    currentPath = p.url.pathname;
  });

  onMount(() => {
    if (!$isAuthenticated && currentPath !== "/login") {
      goto("/register");
    }
  });
</script>

<Modal />
<AppShell>
  <!-- Page Route Content -->
  {#if isAuthenticated}
    <slot />
  {/if}
</AppShell>
