<script>
  import { ChevronDownIcon } from 'svelte-feather-icons';
  import rippleEffect from '../utils/ripple.js';

  export let classname = '';
  export let isFilled = false;
  export let isOutline = false;
  export let isDanger = false;
  export let isRound = false;
  export let isNormal = false;
  export let isRectangle = false;
  export let isSmall = false;
  export let isSelected = false;

  if (isFilled + isOutline > 1) {
    throw new Error('A button may not be filled and outlined at the same time.');
  }

  if (isDanger + isNormal > 1) {
    throw new Error('A button may not be danger and normal at the same time.');
  }

  if (isFilled + isSelected > 1) {
    throw new Error('A button may not be filled and selected at the same time.');
  }

  export let disabled = false;
  export let label = '';
  export let href = null;
  export let chevron = false;
  export let badge = false;
  export let tooltip = '';

  $: classes = [
    isFilled && 'filled',
    isOutline && 'outline',
    isDanger && 'danger',
    isRound && 'round',
    isNormal && 'normal',
    isRectangle && 'rectangle',
    isSmall && 'small',
    isSelected && 'selected',
  ].filter(v => v !== false);
</script>

<style>
  :global(.ml) {
    margin-left: .4em;
  }
</style>

{#if href}
  <a
    {href}
    class="btn {classes.join(' ')} {classname}"
    on:click
    use:rippleEffect
    title="{tooltip}"
    rel="prefetch"
  >
    <slot />
  </a>
{:else}
  <button
    type="button"
    {disabled}
    class="btn {classes.join(' ')} {classname}"
    on:click on:mousedown on:mouseup
    title="{tooltip}"
    use:rippleEffect
  >
    {#if badge}
      <div class="badge">
        <slot>{label}</slot>
      </div>
    {:else}
      <slot>{label}</slot>
    {/if}

    {#if chevron}
      <ChevronDownIcon size="24" class="icon ml chevron" />
    {/if}
  </button>
{/if}
