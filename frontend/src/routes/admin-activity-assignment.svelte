<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  import { goto } from '@sapper/app';

  export async function preload(page, session) {
    const { unassignedStudents, currentUser } = await getInitialData(this, session, new Map([
      ['unassignedStudents', '/users/unassigned'],
      ['currentUser', '/user'],
    ]));
    if (currentUser == null) {
      this.redirect(302, '/log-in');
    }
    else if (!currentUser.is_admin) {
      this.error(403, 'Access denied');
    }
    return { unassignedStudents };
  }
</script>

<script>
  import {
    ArrowLeftIcon,
    CheckSquareIcon,
  } from 'svelte-feather-icons';
  import Button from '@/components/button.svelte';
  import Card from '@/components/card.svelte';
  // import DatePicker from '@/components/date-picker.svelte';
  // import Dropdown from '@/components/dropdown.svelte';
  // import TextField from '@/components/text-field.svelte';
  import * as api from '@/utils/api.js';

  export let unassignedStudents;

  async function assignRandomly(email) {
    const resp = await api.post(`/assign-randomly`, {
      data: { student_email: email },
    });

    if (resp.ok) {
      unassignedStudents = unassignedStudents.filter(student => student.email !== email);
    }
  }

  async function assignEveryone() {
    length = unassignedStudents.length;
    for (let i = 0; i < length; ++i) {
      await assignRandomly(unassignedStudents[0].email);
    }
  }
</script>

<div class="page">
  <header>
    <Button isRound href="/">
      <ArrowLeftIcon size=24 class="icon" />
    </Button>
    <div class="title">
      Unassigned students
    </div>
    {#if unassignedStudents.length !== 0}
      <Button isFilled on:click={assignEveryone}>
        assign everyone randomly
      </Button>
    {/if}
  </header>
  {#if unassignedStudents.length !== 0}
    <div class="student-grid">
      {#each unassignedStudents as student (student.email)}
        <Card>
          {student.full_name}
          <Button on:click={() => assignRandomly(student.email)}>
            assign randomly
          </Button>
        </Card>
      {/each}
    </div>
  {:else}
    <div class="empty">
      <div class="icon">
        <CheckSquareIcon size=48 />
      </div>
      <strong>Everyone is assigned!</strong>
      <p>Hooray!</p>
    </div>
  {/if}
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

  .student-grid {
    width: 80%;
    margin-top: 2em;
    display: grid;
    justify-items: start;
    grid-template-columns: repeat(auto-fill, 16em);
    gap: 2em;
  }

  .student-grid :global(.btn) {
    margin: .5em 0 0 0;
  }

  .empty {
    margin-top: 6em;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .empty strong {
    font-size: 1.2em;
    margin-top: .3em;
    margin-bottom: .2em;
  }

  .empty :global(.icon) {
    display: flex;
    width: 8em;
    height: 8em;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #e9e7f6;
  }
</style>
