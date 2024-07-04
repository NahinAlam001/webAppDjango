<script lang="ts">
  let className: string | undefined | null = undefined;
  export { className as class };
</script>

<caption class={className} {...$$restProps}>
  <slot />
</caption>

<style lang="postcss">
  caption {
    @apply mt-4 text-sm text-muted-foreground;
  }
</style>
