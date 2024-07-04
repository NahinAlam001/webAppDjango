<script lang="ts">
  let className: string | undefined | null = undefined;
  export { className as class };
</script>

<thead class={className} {...$$restProps}>
  <slot />
</thead>

<style lang="postcss">
  thead {
    @apply [&_tr]:border-b;
  }
</style>
