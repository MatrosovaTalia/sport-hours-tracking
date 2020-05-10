<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  export async function preload(page, session) {
    return await getInitialData(this, session, new Map([
      ['currentUser', '/user'],
    ]));
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

<strong>
	{#if currentUser == null}
		Not logged in
	{:else}
		Logged in as {currentUser.full_name}{currentUser.is_admin ? ' (admin)': ''}
	{/if}
    <Button isRound on:click={logout}>
      <LogOutIcon size=24/>
    </Button>
</strong>
<div style="display: flex; flex-direction: column;">
	{#if currentUser != null}
		<a href="/activities">Browse activities</a>
		<a href="/check-hours" rel="prefetch">View attendance statistics</a>
		<a href="/student-activity-assignment" rel="prefetch">Choose sport activity</a>
		{#if currentUser.is_admin}
			<a href="/admin-activity-assignment" rel="prefetch">Assign unassigned students</a>
			<a href="/create-activity" rel="prefetch">Create a new sport activity</a>
		{/if}
	{/if}
</div>

<style>
	strong {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 1em;
	}
</style>
