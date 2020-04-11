<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  export async function preload(page, session) {
    return await getInitialData(this, session, new Map([
      ['activities', '/activities/all'],
    ]));
  }
</script>

<script>
  import * as api from '@/utils/api.js';
  import { onMount } from 'svelte';
  export let activities;
	let chosenUser = 'm.ivanova';
  let chosenActivity;
	let assignments = null;

  onMount(async () => {
    let resp = await api.get(`/activities?assigned_to=${chosenUser}`);
    assignments = await resp.json();
  });

		function assignStudent() {
			assignments.push({id: chosenActivity.id, name: chosenActivity.name});
			assignments = assignments;
	}
</script>

<div>
        <p id = "textp">Choose sport activity to assign yourself:<p>
				<p><select name="Activity" bind:value={chosenActivity}>
            <option disabled selected> – Choose  Sport Activity – </option>
            {#each activities as activity(activity.id)}
            <option value={activity}>{activity.name}</option>
            {/each}
        </select></p>
        <div>
            <input type="submit" value="Assign" on:click={assignStudent}>
        </div>
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
</div>

<a href="/" rel="prefetch">Go back</a>

<style>
    div{
    font-family: Electrica, sans-serif;
    }

    #textp{
        font-weight: bold;
        font-size: 25px;
    }
    select{
        background-color: rgb(222, 222, 222);
        padding: 8px 8px 8px 8px;
        font-family: Electrica, sans-serif;
        border-width: 1.5px;
        border-color: violet;
        border-radius: 10px;
    }

    input{
        padding: 8px 8px 8px 8px;
        font-family: Electrica, sans-serif;
        border-width: 1.5px;
        border-color: violet;
        border-radius: 10px;
    }
	table{
		padding-top: 40px;
    font-size: 18px;
	}
	th{
		color: darkviolet;
	}
</style>
