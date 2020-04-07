<script>
    let activities = [
        {id: '10', name: 'Breakdance, Friday, 17:00-18:30'},
	{id: '11', name: 'Breakdance, Saturday, 13:00-14:30'},
        {id: '20', name: 'Swimming, Friday, 9:00-10:00'},
	{id: '21', name: 'Swimming, Wednessday, 9:00-10:00'},
        {id: '3', name: 'Stretching, Monday, 15:00-16:30'},
        {id: '4', name: 'Fitness trainings, Thursday, 8:30-10:00'},
        {id: '5', name: 'Backetball, Wednessday, 18:00-20:00'},
    ];
	let chosenUser = 1;
	let chosenActivity;
	let assignments = [{ActivityID: 10, StudentID: chosenUser}];

	function assignStudent() {
		assignments.push({ActivityID: chosenActivity, StudentID: chosenUser});
		assignments = assignments;
	}
</script>

<div>
        <p id = "textp">Choose sport activity to assign yourself:<p>
	<p><select name="Activity" bind:value={chosenActivity}>
            	<option disabled selected>--Choose  Sport Activity--</option>
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
        {#each assignments as assignment (assignment.ActivityID)}
          	<tr>
            		<td>{assignment.ActivityID}</td>
          	</tr>
        {/each}
      	</tbody>
    	</table>
  	{/if}
</div>

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
