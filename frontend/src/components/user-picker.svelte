<script>
  import { createEventDispatcher } from 'svelte';
  import Dropdown from './dropdown.svelte';
  import Button from './button.svelte';

  export let users;
  export let label = 'select e-mail';
  export let value = null;
  let open = false;

  $: actualLabel = value || label;

  function setValue(email) {
    value = email;
    dispatch('change', email);
    open = false;
  }

  const dispatch = createEventDispatcher();
</script>

<Dropdown label={actualLabel} noclose bind:value={open}>
  {#each users as user}
    <Button on:click={() => setValue(user.email)}>{user.email}</Button>
  {/each}
</Dropdown>
