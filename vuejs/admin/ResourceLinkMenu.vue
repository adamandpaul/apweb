<template>
    <div class="resource-link-menu">
        <ResourceLinkItem
            class="item"
            v-for="(item, idx) in items"
            :dark="dark"
            :key="idx"
            :item="item" />
    </div>
</template>
<script>

import ResourceLinkItem from './ResourceLinkItem.vue'

export default {

    components: {
        ResourceLinkItem,
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
