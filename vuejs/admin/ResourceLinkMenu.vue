<template>
    <div class="resource-link-menu">
        <div class="container">
            <div class="row">
                <ResourceLinkItem
                    class="item"
                    v-for="(item, idx) in items"
                    :key="idx"
                    :item="item" />
            </div>
        </div>
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
    },

}
</script>
<style lang="sass" scoped>

.resource-link-menu
    max-width: 800px
    margin: 0 auto

.row
    display: flex
    flex-wrap: wrap
    justify-content: center

.item
    display: block
    flex-basis: 345px
    max-width: 345px

</style>