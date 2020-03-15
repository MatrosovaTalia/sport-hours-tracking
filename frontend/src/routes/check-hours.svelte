<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';

  export async function preload(page, session) {
    return await getInitialData(this, session, new Map([
      ['users', '/users'],
    ]));
  }
</script>

<script>
  import * as api from '@/utils/api.js';

  export let users;
  let activities = null;
  let chosenUser = null;
  let chosenActivity = null;
  let records = null;

  async function getActivities(evt) {
    chosenUser = evt.target.value;
    let resp = await api.get(`/activities?assigned_to=${chosenUser}`);
    activities = await resp.json();
  }

  async function showRecords(evt) {
    chosenActivity = evt.target.value;
    let resp = await api.get(`/activities/${chosenActivity}/attendance?student_id=${chosenUser}`);
    records = await resp.json();
  }
</script>


<a href="/" rel="prefetch">Go back</a>

<form>
  <label for="student">Choose a student:</label>
  <select name="student" on:change={getActivities} value="choose">
    <option disabled selected value> – Select – </option>
    {#each users as user (user.id)}
      <option value={user.id}>{user.full_name}</option>
    {/each}
  </select>

  <label for="student">Choose an activity:</label>
  <select name="student" disabled={activities == null} on:change={showRecords}>
    <option disabled selected value> – Select – </option>
    {#if activities != null}
      {#each activities as activity (activity.id)}
        <option value={activity.id}>{activity.name}</option>
      {/each}
    {/if}
  </select>

  {#if records != null}
    <table>
      <thead>
        <th>Date</th>
        <th>Hours</th>
      </thead>
      <tbody>
        {#each records as record (record.id)}
          <tr>
            <td>{record.date}</td>
            <td>{record.hours_number}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</form>
