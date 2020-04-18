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
  export let currentUser;
  export let activities;
</script>

<a href="/">Go back</a>
<ul>
  {#each activities as activity (activity.id)}
    <li>
      <a href="/activities/{activity.id}">
        {activity.name}
        {#if activity.leader === currentUser.email}
          [leader]
        {/if}
      </a>
    </li>
  {/each}
</ul>
