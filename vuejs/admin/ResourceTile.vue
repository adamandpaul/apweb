<template>
    <div>
        <component :is="ui" :tile="tile" :newTab="newTab">
            <template v-slot:start="{resource}"><slot name="start" :resource="resource"></slot></template>
            <template v-slot:left="{resource}"><slot name="left" :resource="resource"></slot></template>
            <template v-slot:end="{resource}"><slot name="end" :resource="resource"></slot></template>
        </component> 
    </div>
</template>
<script>
export default {
    props: {
        tile: {},
        newTab: {},
    },
    computed: {
        ui() {
            return this.tile.ui || "resource-tile-default"
        },
    },
}
</script>