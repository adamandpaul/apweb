<template>
    <div :class="{zoom: zoom}">
        <router-link
            :to="routeTo"
            class="node-link"
            :class="{'page-title': pageTitle, 'root': root, h1: pageTitle}">
            <span class="separator">⯈</span>
            <span class="content">
                <span class="home-icon" v-if="root">🏠&#xFE0E;</span>
                <span v-if="zoom || pageTitle || !root"> {{ title }}</span>
            </span>
        </router-link>
        <ResourceMenu
            v-if="zoom"
            :items="resourceMenuItems"
            />
    </div>
</template>
<script>

import utils from '../utils'
import ResourceMenu from './ResourceMenu.vue'

export default {
    components: {
        ResourceMenu,
    },

    props: {
        node: Object,
        zoom: Boolean,
        pageTitle: Boolean,
        root: Boolean,
    },
    computed: {
        title() { return this.node.title },
        routeTo() {
            return this.pathToString(this.node.path)
        },
        resourceMenuItems() {
            return this.node.named_resources
        },
    },
    methods: {
        pathToString: utils.pathToString,
    }
}

</script>
<style lang="sass" scoped>
.node-link.page-title
    font-size: 30px
    background: #444
    color: white
    border: thin solid #444
    .content
        text-align: left


.node-link
    background: #3d8af7
    color: white
    border: thin solid #3d8af7
    border-radius: 2px
    padding: 2px 15px 2px 0
    box-sizing: border-box
    text-decoration: none
    outline: none

    display: flex
    flex-direction: column
    flex-wrap: wrap
    justify-content: center
    align-items: flex-start
    height: 64px

    &:hover
        border-color: white

    &>*
        display: block

    .separator
        margin-left: -1px
        flex-grow: 0
        height: 40px
        line-height: 40px
        font-size: 20px
        width: 15px

    .content
        width: 100%
        text-align: center
        padding: 0 8px


.root
    font-size: 30px

.zoom
    .content
        text-align: left


</style>
