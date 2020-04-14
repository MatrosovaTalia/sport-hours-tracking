<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  export async function preload(page, session) {
    const data = await getInitialData(this, session, new Map([
      ['users', '/users'],
      ['activities', '/activities/all']
      ['currentUser', '/user'],
    ]));
    if (data.currentUser == null) {
      this.error(403, 'Log in, please');      
    }
    return data;
  }
</script>

<script>
  import * as api from '@/utils/api.js';
  export let users;
  export let activities;
  let chosenUser = null;
  let chosenActivity = null;
  let assignedStudents = null;

  async function showAssignedStudents() {
    let resp = await api.get(`/activities/${chosenActivity}/assigned`);
    assignedStudents = await resp.json();
  }

  async function assignStudent() {
    let resp = await api.post(`/activities/${chosenActivity}/assigned`, {data: {student_email: chosenUser,},});
    if (resp.ok) {
      showAssignedStudents();
      chosenActivity = null;
      chosenUser = null;
    }
  }
</script>

<a href="/" rel="prefetch">Go back</a>
<div>
  <p id = "textp">Fill the form to assign student to sport activity:</p>
  <select name="Activity" bind:value={chosenActivity} on:change={showAssignedStudents}>
    <option disabled selected> – Choose  Sport Activity – </option>
    {#each activities as activity(activity.id)}
      <option value={activity.id}>{activity.name}</option>
    {/each}
  </select>
  <select name="Student" bind:value={chosenUser}>
    <option disabled selected> – Choose Student – </option>
    {#each users as user(user.email)}
      <option value={user.email}>{user.full_name}</option>
    {/each}
  </select>
</div>
<button type="button" on:click={assignStudent} disabled={(chosenUser == null)|(chosenActivity == null)}>Assign</button>
{#if assignedStudents != null}
  <table>
    <thead>
      <th>Participant's Email</th>
      <th>Participant's Full Name</th>
    </thead>
    <tbody>
    {#each assignedStudents as student (student.email)}
      <tr>
        <td>{student.email}</td>
  	    <td>{student.full_name}</td>
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
