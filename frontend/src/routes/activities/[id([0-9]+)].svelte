<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';
  import { goto } from '@sapper/app';

  export async function preload(page, session) {
    const data = await getInitialData(this, session, new Map([
      ['currentUser', '/user'],
      ['activity', `/activities/${page.params.id}`],
      ['userActivities', '/activities/assigned'],
    ]));

    if (data.currentUser == null) {
      this.redirect(302, '/log-in');
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
    CheckIcon,
    LogInIcon
  } from 'svelte-feather-icons';
  import Button from '@/components/button.svelte';
  import DatePicker from '@/components/date-picker.svelte';
  import Dropdown from '@/components/dropdown.svelte';
  import TextField from '@/components/text-field.svelte';
  import { formatDate } from '@/utils/date-time-format.js';
  import * as api from '@/utils/api.js';
  import {onMount} from 'svelte';

  export let currentUser;
  export let activity;
  export let userActivities;
  let sportHours = null;
  let hoursPerDay = null;
  let hours_total = 0;
  let hours_week = 0;
  let hours_today = 0;
  let hours_date = 0;

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

  let is_participant = false;
  $:  for (let userActivity of userActivities) {
        if (userActivity.id == activity.id) {
          is_participant = true;
        }
      }

  /* Replaces the "Z" timezone modifier for an explicit +00:00 */
  function isoForURL(date) {
    date.setHours(date.getHours() + 3);
    return date.toISOString().slice(0, 10);
  }

  onMount(async () => {
    if (currentUser.email !== activity.leader) {
      const resp = await api.get(`/activities/${activity.id}/attendance?student_email=${currentUser.email}`);
      sportHours = await resp.json();
      let currentDate = new Date();
      sportHours.forEach(element => {
        hours_total += element.hours_number;

        let dateParts = element.date.split(/-/);
        let elementDate = new Date(dateParts[0], dateParts[1]-1, dateParts[2]); //month count from 0
        let ifSunday = ((currentDate.getDay()==0) ? -6 : 1);
        let firstWeekDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()-currentDate.getDay()+ifSunday);
        if ((Math.round(elementDate - firstWeekDay)<=(currentDate.getDay()-ifSunday)*86400000) && (Math.round(elementDate - firstWeekDay)>=0)){ // date difference in ms
          hours_week += element.hours_number;
        }

        if (formatDate(currentDate)==formatDate(element.date)) {
          hours_today = element.hours_number;
        }

        if (formatDate(selectedDate)==formatDate(element.date)) {
          hours_date = element.hours_number;
        }
      });
    }
  })

  $: getHoursForDay(selectedDate);

  async function getHoursForDay(date) {
    const resp = await api.get(
      `/activities/${activity.id}/attendance-per-day?date=${isoForURL(date)}`
    );
    const jsonResp = await resp.json();
    hoursPerDay = new Map();
    for (let obj of jsonResp) {
      hoursPerDay.set(obj.student_email, obj.hours_number);
    }
  }

  function showHours(){
    hours_date = 0;
    sportHours.forEach(element => {
      if (formatDate(selectedDate)==formatDate(element.date)) {
        hours_date += element.hours_number;
      }
    });
  }

  async function submitHours(email, hours) {
    if (hours > 3) {
      return;
    }

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

  async function enroll(){
    let resp = await api.post(`/activities/${activity.id}/assigned`, {
      data: {student_email: currentUser.email,},
    });
    if (resp.ok) {
      resp = await api.get('/activities/assigned');
      userActivities = await resp.json();
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
    {#if activity.chat_link != null}
      <Button href="{activity.chat_link}">
        join Telegram chat
      </Button>
    {/if}
    {#if is_participant}
      <div class="status"> <span class="marker"> &#11044</span> enrolled </div>
    {:else}
      <Button isFilled on:click={enroll}>
        <LogInIcon size=24 class="icon mr" />
        enroll
      </Button>
    {/if}
  </header>
  <main class:student={currentUser.email !== activity.leader}>
    {#if is_participant && (currentUser.email !== activity.leader)}
      <div class="heading" >
        attendance
      </div>
      <div class="hours_stat">
        <div class="hours_segment">
          <p class="hours">{hours_total} hours</p>
          <p class="when">this semester</p>
        </div>
        <div class="hours_segment">
          <p class="hours">{hours_week} hours</p>
          <p class="when">this week</p>
        </div>
        <div class="hours_segment">
          <p class="hours">{hours_today} hours</p>
          <p class="when">today</p>
        </div>
        <div class="hours_segment">
          <p class="hours">{hours_date} hours</p>
          <p class="when">{formatDate(selectedDate)}</p>
        </div>
        <div class="datapicker">
          <Dropdown bind:value={datePickerOpen} noclose>
            <button slot="handle" class="btn handle" on:click={() => datePickerOpen = !datePickerOpen} style="font-size: 20px">
              <CalendarIcon size=26 class="icon mr" />
              {formatDate(selectedDate)}
              <ChevronDownIcon size=26 class="icon ml chevron" />
            </button>
            <DatePicker bind:value={selectedDate} on:change={() => { datePickerOpen = false; showHours();}} />
          </Dropdown>
        </div>
      </div>
    {/if}
    <div class="gorizontal-box">
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
      {#if currentUser.email === activity.leader}
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
                max=3
                value={hoursPerDay != null && hoursPerDay.get(student.email) || null}
                on:change={({ detail: hours}) => submitHours(student.email, hours)}
              />
            </div>
          {/each}
        </div>
      </div>
      {/if}
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

  main.student {
    flex-direction: column;
  }

  .schedule {
    flex: 1;
  }

  .attendance {
    flex: 1;
    margin-left: 1.5em;
  }

  .schedule:not(:last-child) {
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

  .hours_stat {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin: 1.5em 0em;
  }

  .hours_segment {
    padding: 0px 15px;
    width: 170px;
    text-align: center;
    border-right: 1px solid lightgrey;
  }
  .hours {
    font-weight: bold;
    font-size: 28px;
    white-space: nowrap;
  }
  .when {
    font-size: 18px;
    white-space: nowrap;
    margin-top: 0.5em;
  }
  .gorizontal-box {
    display: flex;
    flex-direction: row;
    width: 100%;
  }

  .datapicker {
    margin-left: 1em;
    white-space: nowrap;
  }

  .status {
    font-weight: 500;
    font-size: 1.2em;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  .marker {
    color: #220CA4;
    margin: 1em;
    font-size: .5em;
  }
</style>
