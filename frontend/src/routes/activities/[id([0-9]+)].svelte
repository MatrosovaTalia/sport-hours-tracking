<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';

  export async function preload(page, session) {
    const data = await getInitialData(this, session, new Map([
      ['currentUser', '/user'],
      ['activity', `/activities/${page.params.id}`],
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
    Edit3Icon,
    ChevronDownIcon,
    CalendarIcon,
    CheckIcon
  } from 'svelte-feather-icons';
  import Button from '@/components/button.svelte';
  import DatePicker from '@/components/date-picker.svelte';
  import Dropdown from '@/components/dropdown.svelte';
  import TextField from '@/components/text-field.svelte';
  import { formatDate } from '@/utils/date-time-format.js';
  import * as api from '@/utils/api.js';

  export let currentUser;
  export let activity;

  let autosaved = false;
  let selectedDate = new Date();
  let datePickerOpen = false;

  const weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  const scheduleByWeekday = [null, null, null, null, null, null, null];
  for (let record of activity.schedule_records) {
    if (scheduleByWeekday[record.day] == null) {
      scheduleByWeekday[record.day] = [record];
    } else {
      scheduleByWeekday[record.day].push(record);
    }
  }

  async function submitHours(email, hours) {
    console.log(selectedDate.toISOString().slice(0, 10));
    const resp = await api.post(`/activities/${activity.id}/attendance`, {
      data: {
        student_email: email,
        hours_number: hours,
        date: selectedDate.toISOString().slice(0, 10),
      },
    });
    if (resp.ok) {
      autosaved = true;
      setTimeout(() => autosaved = false, 1500);
    }
  }
</script>

<div class="page">
  <header>
    <Button isRound href="/activities">
      <ArrowLeftIcon size=24 class="icon" />
    </Button>
    <div class="activity-name">
      {activity.name}
    </div>
    {#if activity.leader === currentUser.email}
      <Button>
        <Edit3Icon size=24 class="icon mr" />
        edit activity
      </Button>
    {/if}
  </header>
  <main>
    <div class="schedule">
      <div class="heading">
        schedule
      </div>
      <div class="table-wrapper">
        <table>
          {#if activity.schedule_records.length !== 0}
            <thead>
              {#each scheduleByWeekday as weekday, i}
                {#if weekday != null}
                  <th>{weekdays[i]}</th>
                {/if}
              {/each}
            </thead>
            <tbody>
              {#each scheduleByWeekday as weekday, i}
                {#if weekday != null}
                  <td>
                    {#each weekday as record}
                      <div class="record">
                        <time>
                          {record.start_time.slice(0, 5)} – {record.finish_time.slice(0, 5)}
                        </time>
                        <div class="location">
                          {record.location}
                        </div>
                      </div>
                    {/each}
                  </td>
                {/if}
              {/each}
            </tbody>
          {:else}
            No information.
          {/if}
        </table>
      </div>
    </div>
    <div class="attendance">
      <div class="heading">
        attendance
        {#if autosaved}
          <span class="autosaved">
            <CheckIcon size=16 class="icon" />
            autosaved!
          </span>
        {/if}
      </div>
      <div class="actions">
        <Dropdown bind:value={datePickerOpen} noclose>
          <button slot="handle" class="btn handle" on:click={() => datePickerOpen = !datePickerOpen}>
            <CalendarIcon size=24 class="icon mr" />
            {formatDate(selectedDate)}
            <ChevronDownIcon size=24 class="icon ml chevron" />
          </button>
          <DatePicker bind:value={selectedDate} on:change={() => { datePickerOpen = false; }} />
        </Dropdown>
      </div>
      <div class="mark-area">
        {#each activity.assigned_students as student (student.email)}
          <div class="participant">
            <div class="name">{student.full_name}</div>
            <a href="mailto:{student.email}">{student.email}</a>
            <TextField
              type="number"
              placeholder=0
              min=0
              on:change={({ detail: hours}) => submitHours(student.email, hours)}
            />
          </div>
        {/each}
      </div>
    </div>
  </main>
</div>

<style>
  :global(body) {
    max-width: unset;
  }

  :global(svg) {
    stroke: #220CA4;
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

  .activity-name {
    margin-left: 1em;
    font-size: 1.5em;
    font-weight: 500;
    flex: 1;
  }

  :global(.mr) {
    margin-right: .5em;
  }

  :global(.ml) {
    margin-left: .5em;
  }

  .heading {
    text-transform: uppercase;
    font-weight: 500;
    color: #220CA4;
  }

  main {
    display: flex;
    padding: 2em 1em;
    width: 80%;
  }

  .schedule,
  .attendance {
    flex: 1;
    margin-left: 1.5em;
  }

  .schedule {
    border-right: 1px solid #ddd;
  }

  .table-wrapper {
    border: 1px solid #ddd;
    border-radius: 1em;
    margin-top: 1em;
    margin-right: 2em;
  }

  table {
    margin-bottom: 0;
  }

  th {
    text-align: center;
  }

  th:not(:last-child),
  td:not(:last-child) {
    border-right: 1px solid #ddd;
  }

  .record {
    margin: .5em;
  }

  .record time {
    text-align: center;
    display: block;
  }

  .record .location {
    text-align: center;
    font-size: .9em;
  }

  :global(.date-picker) {
    clear: both;
  }

  :global(.relative-wrapper) {
    margin: 1em 0 .5em;
  }

  .attendance .actions {
    margin-top: 1em;
  }

  .mark-area {
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  .participant {
    padding: .5em 1.5em .5em .5em;
    margin-left: 1em;
    display: grid;
    grid-template-columns: 1fr auto;
    grid-template-rows: auto auto;
  }

  .participant:not(:last-child) {
    border-bottom: 1px solid #ddd;
  }

  .participant a {
    grid-row: 2 / 3;
    grid-column: 1 / 2;
  }

  :global(.participant .text-field) {
    width: 4em;
    grid-row: 1 / 3;
  }

  .autosaved {
    color: #aaa;
    font-weight: 300;
    stroke: #aaa;
    text-transform: none;
    margin-left: 1em;
  }

  :global(.autosaved .icon) {
    stroke: #aaa;
  }
</style>
