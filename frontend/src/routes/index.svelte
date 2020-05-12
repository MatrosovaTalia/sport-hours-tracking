<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  export async function preload(page, session) {
    const data = await getInitialData(this, session, new Map([
      ['currentUser', '/user'],
    ]));
    if (data.currentUser == null) {
      this.redirect(302, '/log-in');
    }
    return data;

  }
</script>

<script>
  import * as api from '@/utils/api.js';
  import { goto } from '@sapper/app';
  import { LogOutIcon, } from 'svelte-feather-icons';
  import Button from '@/components/button.svelte';
  export let currentUser;

  async function logout() {
    let resp = await api.get(`/logout`);
    if (resp.ok) {
      goto('/log-in');
    }
  }
</script>

<svelte:head>
	<title>Sport Hours Tracker</title>
</svelte:head>

<div class="page">
  <header>
    <div class="title">
      Sport Hours Tracker
    </div>
		Logged in as {currentUser.full_name}{currentUser.is_admin ? ' (admin)': ''}
    <Button isRound on:click={logout} classname="ml-2">
      <LogOutIcon size=24 />
    </Button>
  </header>

  <div style="display: flex; flex-direction: column; margin-top: 4em;">
    <Button isRectangle isOutline href="/activities">
      Browse activities
    </Button>
    {#if currentUser.is_admin}
      <Button isRectangle isOutline classname="mt-2" href="/admin-activity-assignment">
        Assign unassigned students
      </Button>
    {/if}
  </div>
</div>

<style>
  :global(body) {
    max-width: unset;
  }

  .page {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: Ubuntu, sans-serif;
  }

  header {
    width: 80%;
    padding: 1em 2em;
    border-bottom: 1px solid #ddd;
    display: flex;
    align-items: center;
  }

  .title {
    margin-left: 1em;
    font-size: 1.5em;
    font-weight: 500;
    flex: 1;
  }

	strong {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 1em;
	}

  :global(.ml-2) {
    margin-left: .8em;
  }

  :global(.mt-2) {
    margin-top: .8em;
  }

  .page :global(.btn.rectangle) {
    justify-content: center;
  }
</style>
