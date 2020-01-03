<template>
    <div class="resource-menu">
        <ResourceMenuItem
            class="item"
            v-for="(item, idx) in items"
            :dark="dark"
            :key="idx"
            :item="item" />
    </div>
</template>
<script>

import ResourceMenuItem from './ResourceMenuItem.vue'

export default {

    components: {
        ResourceMenuItem,
    },

    props: {
        items: Array,
        dark: {
            type: Boolean,
            default: false,
        },
    },

}
</script>
