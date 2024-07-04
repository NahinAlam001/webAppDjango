<script lang="ts">
  let className: string | undefined | null = undefined;
  export { className as class };
</script>

<td class={className} {...$$restProps}>
  <slot />
</td>

<style lang="postcss">
  td {
    @apply p-4 align-middle [&:has([role=checkbox])]:pr-0;
  }
</style>
