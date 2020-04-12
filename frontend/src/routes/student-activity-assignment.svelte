<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  export async function preload(page, session) {
    return await getInitialData(this, session, new Map([
      ['activities', `/activities/all`],
      ['assignments', `/activities?assigned_to=${chosenUser}`],
    ]));
  }
</script>

<script>
  import * as api from '@/utils/api.js';
  export let activities;
  export let assignments;
  let currentUser=current_user;
	let chosenUser = 'm.ivanova';
  let chosenActivity;

  async function assignStudent() {
    let resp = await api.post(`/activities/${chosenActivity}/assigned`, {data: {student_email: chosenUser,},});
    if (resp.ok) {
      chosenActivity = null;
      let resp = await api.get(`/activities?assigned_to=${chosenUser}`);
      assignments = await resp.json();
    }
  }
</script>

<div>
        <p>{currentUser}</p>
        <p id = "textp">Choose sport activity to assign yourself:<p>
				<p><select name="Activity" bind:value={chosenActivity}>
            <option disabled selected> – Choose  Sport Activity – </option>
            {#each activities as activity(activity.id)}
            <option value={activity.id}>{activity.name}</option>
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
