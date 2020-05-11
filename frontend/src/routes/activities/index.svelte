<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';

  export async function preload(page, session) {
    const data = await getInitialData(this, session, new Map([
      ['currentUser', '/user'],
      ['activities', '/activities'],
    ]));

    if (data.currentUser == null) {
      this.error(401, 'Log in, please');
    }

    return data;
  }
</script>

<script>
  import {
    ArrowLeftIcon,
    PlusIcon,
    StarIcon,
    ChevronRightIcon,
  } from 'svelte-feather-icons';
  import Button from '@/components/button.svelte';
  import Card from '@/components/card.svelte';
  export let currentUser;
  export let activities;
</script>

<div class="page">
  <header>
    <Button isRound href="/">
      <ArrowLeftIcon size=24 class="icon" />
    </Button>
    <div class="title">
      All sport activities
    </div>
    {#if currentUser.is_admin}
    <Button href="/create-activity">
      <PlusIcon size=24 />
      <p class="create-button">create a new activity</p>
    </Button>
    {/if}
  </header>
  <div class="club-grid">
    {#each activities as activity (activity.id)}
      <Card>
        <div class="club-name">
          {activity.name}
          {#if activity.leader === currentUser.email}
            <StarIcon size=24 />
          {/if}
        </div>
        <Button href="/activities/{activity.id}">
          schedule & details
          <ChevronRightIcon size=24 />
        </Button>
      </Card>
    {/each}
  </div>
</div>


<style>
  :global(body) {
    max-width: unset;
  }

  :global(svg) {
    stroke: #220ca4;
  }

  .page {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: Ubuntu, sans-serif;
  }

  header {
    width: 80%;
    padding: 1em 2em;
    border-bottom: 1px solid #ddd;
    display: flex;
    align-items: center;
  }

  .title {
    margin-left: 1em;
    font-size: 1.5em;
    font-weight: 500;
    flex: 1;
  }

  .create-button{
    margin: .5em;
    font-size: 1.1em;
    font-weight: 500;
  }
  .club-grid {
    width: 80%;
    margin-top: 2em;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
    grid-gap: 1em;
  }

  .club-grid :global(.btn) {
    margin: .5em 0 0 0;
  }

  .club-name{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    font-size: 1.25em;
    font-weight: 500;
  }
</style>
