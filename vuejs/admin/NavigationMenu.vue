<template>
    <div class="menu" :class="{zoom: zoom}">
        <div class="container">

            <div class="row" v-if="zoom">
                <button class="zoom-toggle" @click="zoom = false">⊟</button>
                <div class="aligned-row">
                    <NavigationMenuNode
                        class="navigation-menu-node"
                        v-for="(node, idx) in breadcrumbs"
                        :key="idx"
                        :node="node"
                        :zoom="true"
                        :root="idx == 0"
                        :page-title="idx == (breadcrumbs.length - 1)"
                        :class="{'page-title': idx == (breadcrumbs.length - 1)}"
                        />
                </div>
            </div>

            <div class="row" v-else>
                <button class="zoom-toggle" @click="zoom = true">⊞</button>
                <NavigationMenuNode
                    class="navigation-menu-node"
                    v-for="(node, idx) in breadcrumbs"
                    :key="idx"
                    :node="node"
                    :zoom="false"
                    :root="idx == 0"
                    :page-title="idx == (breadcrumbs.length - 1)"
                    :class="{'page-title': idx == (breadcrumbs.length - 1)}"
                    />
            </div>
        </div>
    </div>
</template>
<script>

import NavigationMenuNode from './NavigationMenuNode.vue'
import { mapGetters } from 'vuex'

export default {

    data() {
        return {
            zoom: false,
        }
    },

    components: {
        NavigationMenuNode,
    },

    computed: {
        ...mapGetters([
            'breadcrumbs',
        ]),
    },

    watch: {
        breadcrumbs() {
            this.zoom = false
        }
    }

}

</script>
<style lang="sass" scoped>

.menu
    background: black
    padding: 8px 16px

.container
    position: relative
    margin: 0 auto

.row
    margin: 0 -8px
    display: flex
    flex-wrap: wrap

    &>*
        flex-basis: content
        flex-grow: 1
        margin: 8px 8px

        &.page-title
            flex-grow: 10



.aligned-row
    flex-basis: 200px

.zoom-toggle
    width: 64px
    height: 64px
    flex-basis: 64px
    flex-grow: 0
    flex-shrink: 0
    cursor: pointer

    background: black
    color: white
    padding: 0
    line-height: 64px
    text-align: center
    font-weight: 400
    border: thin solid black
    border-radius: 2px
    font-size: 30px

    &:hover
        border-color: white

.zoom
    .row
        justify-content: end
    .navigation-menu-node
        max-width: 900px

button

</style>
