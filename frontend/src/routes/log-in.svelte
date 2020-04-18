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
  import { goto } from '@sapper/app';
  export let users;
  let chosenUser = null;

  async function login() {
    let resp = await api.get(`/login?email=${chosenUser}`);
    if (resp.ok) {
      chosenUser = null;
    } 
    goto('/');
  }

  async function logout() {
    let resp = await api.get(`/logout`);
    if (resp.ok) {
      goto('/');
    }
  }
</script>


<a href="/" rel="prefetch">Go back</a>
<div>
  <p id="textp">Choose user to enter the service:<p>
  <select name="User" bind:value={chosenUser}>
    <option disabled selected> – Choose User – </option>
    {#each users as user(user.email)}
      <option value={user.email}>{user.full_name}</option>
    {/each}
  </select>
  <button type="button" on:click={login} disabled={chosenUser == null}>Continue</button>
  <button type="button" on:click={logout}>Log out</button>
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
  button{
    padding: 8px 8px 8px 8px;
    font-family: Electrica, sans-serif;
    border-radius: 10px;
  }
</style>
