<template>
    <div>
        <component :is="ui" :tile="tile" /> 
    </div>
</template>
<script>
export default {
    props: {
        tile: {},
    },
    computed: {
        ui() {
            return this.tile.ui || "resource-tile-default"
        },
    },
}
</script>