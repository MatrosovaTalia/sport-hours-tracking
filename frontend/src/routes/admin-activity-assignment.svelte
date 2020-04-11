<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  export async function preload(page, session) {
    return await getInitialData(this, session, new Map([
      ['users', '/users'],
      ['activities', '/activities/all'],
    ]));
  }
</script>

<script>
  import * as api from '@/utils/api.js';
  export let users;
  export let activities;
		let chosenUser;
		let chosenActivity;
	  let assignedStudents = null;

  async function showAssignedStudents() {
    let resp = await api.get(`/activities/${chosenActivity}/assigned`);
    assignedStudents = await resp.json();
  }

  async function assignStudent() {
    let resp = await api.post(`/activities/${chosenActivity}/assigned`, {
      data: {
        student_email: chosenUser,
      },
    });

    if (resp.ok) {
      showAssignedStudents();
      chosenActivity = null;
      chosenUser = null;
    }
  }
</script>

<div>
        <p id = "textp">Fill the form to assign student to sport activity:<p>
				<p><select name="Activity" bind:value={chosenActivity} on:change={showAssignedStudents}>
            <option disabled selected>--Choose  Sport Activity--</option>
            {#each activities as activity(activity.id)}
            <option value={activity.id}>{activity.name}</option>
            {/each}
        </select></p>
				<p><select name="Student" bind:value={chosenUser}>
            <option disabled selected> – Choose Student – </option>
            {#each users as user(user.email)}
            <option value={user.email}>{user.full_name}</option>
            {/each}
        </select></p>
        <div>
            <input type="submit" value="Assign" on:click={assignStudent}>
        </div>
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
		padding: 5px;
	}
	td{
		padding: 5px;
	}
</style>
