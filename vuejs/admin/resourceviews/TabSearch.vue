<template>
    <collection-browse :resourceURL="resourceURL" title="Search" />
</template>
<script>

export default {

    props: {
        resourceURL: {type: String, default: null},
    },

}

</script>
