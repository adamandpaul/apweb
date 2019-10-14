<template>
    <div class="resource-menu">
        <div class="container">
            <div class="row">
                <ResourceMenuItem
                    class="item"
                    v-for="(item, idx) in items"
                    :key="idx"
                    :item="item" />
            </div>
        </div>
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
    },

}
</script>
<style lang="sass" scoped>

.resource-menu
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
