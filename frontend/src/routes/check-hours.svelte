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
  let error = null;

  async function getActivities(evt) {
    chosenUser = evt.target.value;
    try {
      let resp = await api.get(`/activities/assigned?to=${chosenUser}`);
      activities = await resp.json();
      error = null;
    } catch (e) {
      error = 'Access denied :c';
      console.error(e);
    }
  }

  async function showRecords(evt) {
    chosenActivity = evt.target.value;
    try {
      let resp = await api.get(`/activities/${chosenActivity}/attendance?student_email=${chosenUser}`);
      records = await resp.json();
      error = null;
    } catch (e) {
      error = 'Access denied :c';
      console.error(e);
    }
  }
</script>


<a href="/" rel="prefetch">Go back</a>

<form>
  <label for="student">Choose a student:</label>
  <select name="student" on:change={getActivities} value="choose">
    <option disabled selected value> – Select – </option>
    {#each users as user (user.email)}
      <option value={user.email}>{user.full_name}</option>
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
{#if error}
  <p>{error}</p>
{/if}
