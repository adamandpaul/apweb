<template>
    <a class="link" :href="url">
        <span class="arrow">›› </span>
        <span>{{ title }}</span>
    </a>
</template>
<script>

export default {

    props: {
        item: Object,
    },

    computed: {
        title() { return this.item.title },
        url() { return this.item.url },
    },

}
</script>
<style lang="sass" scoped>

.link
    box-sizing: border-box
    background: #0e5402
    border: thin solid #0ccf0e
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
