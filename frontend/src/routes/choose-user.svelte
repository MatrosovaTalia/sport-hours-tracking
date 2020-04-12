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
  let chosenUser = null;

    async function login() {
        let resp = await api.get(`/login?email=${chosenUser}`);

        if (resp.ok) {
          chosenUser = null;
        } 
    }
</script>


<a href="/" rel="prefetch">Go back</a>

<div>
        <p id = "textp">Choose user to enter the service:<p>
        <p><select name="User" bind:value={chosenUser}>
            <option disabled selected> – Choose User – </option>
            {#each users as user(user.email)}
            <option value={user.email}>{user.full_name}</option>
            {/each}
        </select></p>
        <div>
            <a href="/" rel="prefetch">
            <input type="submit" value="Continue" on:click={login} disabled={!([chosenUser].every(x => !!x))}>
            </a>
        </div>
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
        border-radius: 10px;
    }
    input{
        padding: 8px 8px 8px 8px;
        font-family: Electrica, sans-serif;
        border-radius: 10px;
    }
</style>
