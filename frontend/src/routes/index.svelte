<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  export async function preload(page, session) {
    return await getInitialData(this, session, new Map([
      ['currentUser', '/user'],
    ]));
  }
</script>

<script>
	export let currentUser;
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
</strong>
<div style="display: flex; flex-direction: column;">
	{#if currentUser != null}
		<a href="/activities">Browse activities</a>
		<a href="/check-hours" rel="prefetch">View attendance statistics</a>
		<a href="/student-activity-assignment" rel="prefetch">Choose sport activity</a>
		{#if currentUser.is_admin}
			<a href="/admin-activity-assignment" rel="prefetch">Assign unassigned students</a>
		{/if}
	{/if}

	<a href="/log-in" rel="prefetch">Choose user</a>
</div>

<style>
	strong {
		display: block;
		margin-bottom: 1em;
	}
</style>
