<script lang="ts">
  let className: string | undefined | null = undefined;
  export { className as class };
</script>

<div>
  <table class={className} {...$$restProps}>
    <slot />
  </table>
</div>

<style lang="postcss">
  div {
    @apply w-full overflow-auto;
  }

  table {
    @apply w-full caption-bottom text-sm;
  }
</style>
