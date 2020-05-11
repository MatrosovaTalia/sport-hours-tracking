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
  import { LogInIcon, ArrowRightIcon, } from 'svelte-feather-icons';
  import Button from '@/components/button.svelte';
  import Card from '@/components/card.svelte';
  import UserPicker from '@/components/user-picker.svelte';
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

<div class="main">
  <Card width="400px">
  <div class="heading">
    <LogInIcon size=48 />
    <p id="textp">Login<p>
  </div>
  <div class="select-user">
  <UserPicker {users} bind:value={chosenUser} />
  <Button isFilled isRound on:click={login} disabled={chosenUser == null}>
    <ArrowRightIcon size=24/>
  </Button>
  </div>
  </Card>
</div>

<style>
  .main{
    font-family: Ubuntu, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #220ca4;
  }
  .heading{
    font-family: Ubuntu, sans-serif;
    margin: 15px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }
  #textp{
    font-weight: bold;
    font-size: 30px;
    margin: 0px 0px 0px 15px;
  }
  .select-user{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin: 20px;
    position: relative;
    z-index: 10;
  }
</style>
