<script lang="ts">
  let className: string | undefined | null = undefined;
  export { className as class };
</script>

<tbody class={className} {...$$restProps}>
  <slot />
</tbody>

<style lang="postcss">
  tbody {
    @apply [&_tr:last-child]:border-0;
  }
</style>
