<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  export async function preload(page, session) {
    const data = await getInitialData(this, session, new Map([
      ['activities', '/activities/all'],
      ['currentUser', '/user'],
    ]));
    if (data.currentUser == null) {
      this.error(403, 'Create a Project');      
    }
    return data;
  }
</script>

<script>
  import * as api from '@/utils/api.js';
	import { onMount } from 'svelte';
  export let activities;
  export let assignments;
  export let currentUser;
  let chosenActivity;

  onMount( async () => {
    let resp = await api.get(`/activities?assigned_to=${currentUser.email}`);
    assignments = await resp.json();
  })

  async function assignStudent() {
    let resp = await api.post(`/activities/${chosenActivity}/assigned`, {data: {student_email: currentUser.email,},});
    if (resp.ok) {
      chosenActivity = null;
      let resp = await api.get(`/activities?assigned_to=${currentUser.email}`);
      assignments = await resp.json();
    }
  }
</script>

<a href="/" rel="prefetch">Go back</a>
<div>
  <p id = "textp">Choose sport activity to assign yourself:</p>
	<select name="Activity" bind:value={chosenActivity}>
    <option disabled selected> – Choose  Sport Activity – </option>
    {#each activities as activity(activity.id)}
      <option value={activity.id}>{activity.name}</option>
    {/each}
  </select>
</div>
<button type="button" on:click={assignStudent} disabled={chosenActivity==null}>Assign</button>
{#if assignments != null}
  <table>
    <thead>
      <th>Your Sport Activities</th>
    </thead>
    <tbody>
    {#each assignments as assignment (assignment.id)}
      <tr>
        <td>{assignment.name}</td>
      </tr>
    {/each}
    </tbody>
  </table>
{/if}

<style>
  div{
    font-family: Electrica, sans-serif;
  }

  #textp{
    font-weight: bold;
    font-size: 25px;
  }
  select{
    padding: 8px;
    background-color: rgb(222, 222, 222);
    border-radius: 10px;
  }

  button{
    padding: 8px;
    font-family: Electrica, sans-serif;
    border-radius: 10px;
  }
	table{
    font-family: Electrica, sans-serif;
    font-size: 18px;
	}
	th{
		color: darkviolet;
	}
</style>
