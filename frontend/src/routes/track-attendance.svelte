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
  let chosenDate = null;
  let chosenHours = null;

  async function getActivities(evt) {
    chosenUser = evt.target.value;
    let resp = await api.get(`/activities?assigned_to=${chosenUser}`);
    activities = await resp.json();
  }

  async function submit() {
    let resp = await api.post(`/activities/${chosenActivity}/attendance`, {
      data: {
        student_email: chosenUser,
        hours_number: chosenHours,
        date: chosenDate,
      },
    });

    if (resp.ok) {
      chosenUser = null;
      chosenActivity = null;
      chosenDate = null;
      chosenHours = null;
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
  <select name="student" disabled={activities == null} bind:value={chosenActivity}>
    <option disabled selected value> – Select – </option>
    {#if activities != null}
      {#each activities as activity (activity.id)}
        <option value={activity.id}>{activity.name}</option>
      {/each}
    {/if}
  </select>

  <label for="date">Choose a date:</label>
  <input type="date" bind:value={chosenDate} name="date" disabled={activities == null} />

  <label for="hours">How many hours for the day?</label>
  <input type="number" bind:value={chosenHours} name="hours" min={1} disabled={activities == null} />

  <button
    type="button"
    on:click={submit}
    disabled={!([chosenUser, chosenActivity, chosenDate, chosenHours].every(x => !!x))}
  >
    Save
  </button>
</form>
