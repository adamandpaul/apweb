<template>
    <router-link
        class="router-link"
        :to="routeTo">
        <span class="arrow">› </span>
        <span>{{ title }}</span>
    </router-link>
</template>
<script>

import utils from '../utils'

export default {

    props: {
        item: Object,
    },

    computed: {
        title() { return this.item.title },
        routeTo() { return this.pathToString(this.item.path) },
    },

    methods: {
        pathToString: utils.pathToString,
    },
}
</script>
<style lang="sass" scoped>

.router-link
    box-sizing: border-box
    background: #021f54
    border: thin solid #0c59cf
    border-radius: 2px
    color: white
    outline: none

    margin: 8px
    padding: 8px
    line-height: 28px

    text-decoration: none

    &:hover
        border-color: white

.arrow
    font-weight: 900

</style>
