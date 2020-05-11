<script context="module">
  import getInitialData from '@/utils/get-initial-data.js';

  export async function preload(page, session) {
    const { users, currentUser } = await getInitialData(this, session, new Map([
      ['users', '/users'],
      ['currentUser', '/user'],
    ]));
    if (currentUser == null) {
      this.redirect(302, '/log-in');
    }
    else if (!currentUser.is_admin) {
      this.error(403, 'Access denied');
    }
    return { users };
  }
</script>

<script>
  import {
    ArrowLeftIcon,
    CheckSquareIcon,
  } from 'svelte-feather-icons';
  import Button from '@/components/button.svelte';
  import Card from '@/components/card.svelte';
  import TimePicker from '@/components/time-picker.svelte';
  import Dropdown from '@/components/dropdown.svelte';
  import TextField from '@/components/text-field.svelte';
  import FormField from '@/components/form-field.svelte';
  import UserPicker from '@/components/user-picker.svelte';
  import Accordion from '@/components/accordion.svelte';
  import AccordionSection from '@/components/accordion-section.svelte';
  import * as api from '@/utils/api.js';

  export let users;

  let name;
  let leaderEmail;
  let maxStudents;
  let chatLink;

  const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  let schedule = weekdays.map(day => ({ day, start: null, end: null, location: null }));

  async function create() {
    const payload = {
      name: name,
      leader: leaderEmail,
      max_students: maxStudents || null,
      chat_link: chatLink,
      schedule_records: [],
    };

    for (let i = 0; i < schedule.length; ++i) {
      let day = schedule[i];
      if (day.location
       && day.start.hours != null
       && day.start.minutes != null
       && day.end.hours != null
       && day.end.minutes != null) {
        payload.schedule_records.push({
          day: i,
          start_time: (
            day.start.hours.toString().padStart(2, '0')
            + ':' + day.start.minutes.toString().padStart(2, '0')
          ),
          finish_time: (
            day.end.hours.toString().padStart(2, '0')
            + ':' + day.end.minutes.toString().padStart(2, '0')
          ),
          location: day.location,
        });
      }
    }

    try {
      const resp = await api.post('/activities', { data: payload });
      if (resp.ok) {
        name = null;
        leaderEmail = null;
        schedule = weekdays.map(day => ({ day, start: null, end: null, location: null }));
        goto('/activities');
      }
    } catch (e) {
      console.error(e);
    }
  }
</script>

<div class="page">
  <header>
    <Button isRound href="/activities">
      <ArrowLeftIcon size=24 class="icon" />
    </Button>
    <div class="title">
      Create a new sport activity
    </div>
  </header>
  <form>
    <FormField
      title="Name"
      required
    >
      <TextField minlength={1} bind:value={name} />
    </FormField>
    <FormField
      title="Leader"
      required
    >
      <UserPicker {users} bind:value={leaderEmail} />
    </FormField>
    <FormField
      title="Maximum amount of students"
      subtitle="Leave blank for no restrictions"
    >
      <TextField type="number" bind:value={maxStudents} />
    </FormField>
    <FormField
      title="Link to the Telegram chat"
    >
      <TextField bind:value={chatLink} />
    </FormField>
    <FormField
      title="Schedule"
      classname="schedule"
    >
      <Accordion let:panelController={panelController}>
        {#each schedule as day}
          <AccordionSection label={day.day} on:panel-open={panelController}>
            <div class="day">
              <div class="times">
                <Dropdown label="select start time" noclose>
                  <TimePicker bind:value={day.start} />
                </Dropdown>
                <Dropdown label="select end time" noclose>
                  <TimePicker bind:value={day.end} />
                </Dropdown>
              </div>
              <div class="label">
                Location
              </div>
              <TextField bind:value={day.location} />
            </div>
          </AccordionSection>
        {/each}
      </Accordion>
    </FormField>
    <div class="actions">
      <Button isFilled disabled={!name || !leaderEmail} on:click={create}>create</Button>
    </div>
  </form>
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

  form {
    width: 80%;
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-top: 2em;
  }

  form :global(.form-field) {
    width: 60%;
    justify-content: flex-start;
    align-items: center;
  }

  form :global(.form-field .name) {
    font-weight: 500;
    width: 15em;
    margin-right: 1em;
  }

  form :global(.text-field-wrapper) {
    flex: 1;
  }

  form :global(.schedule) {
    flex-direction: column;
    align-items: flex-start;
  }

  form :global(.schedule .times) {
    margin: .5em 0;
    display: flex;
    justify-content: space-between;
  }

  form :global(.time-picker) {
    padding: 1em;
  }
</style>
