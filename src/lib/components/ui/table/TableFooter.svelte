<script lang="ts">
  let className: string | undefined | null = undefined;
  export { className as class };
</script>

<tfoot class={className} {...$$restProps}>
  <slot />
</tfoot>

<style lang="postcss">
  tfoot {
    @apply bg-primary font-medium text-primary-foreground;
  }
</style>
