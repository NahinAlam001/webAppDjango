<script lang="ts">
  let className: string | undefined | null = undefined;
  export { className as class };
</script>

<th class={className} {...$$restProps}>
  <slot />
</th>

<style lang="postcss">
  th {
    @apply h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0;
  }
</style>
