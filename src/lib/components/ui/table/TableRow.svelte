<script lang="ts">
  let className: string | undefined | null = undefined;
  export { className as class };
</script>

<tr class={className} {...$$restProps}>
  <slot />
</tr>

<style lang="postcss">
  tr {
    @apply border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted;
  }
</style>
