<template>
    <div class="headerContainer">
        <div style="display: flex; flex-direction: row; width: 100%; height: 100%; justify-content: flex-start; align-items: center">
            <h1 class="headline">TübiSearch</h1>
            <div class="queryContainer">
                <v-text-field
                    v-model="query"
                    variant="solo"
                    density="compact"
                    hide-details="hide-details"
                    append-inner-icon="mdi-magnify"
                    clearable
                    bg-color="white"
                    class="searchQuery"
                    @click:appendInner="sendSearchQuery"
                    @keydown.enter="sendSearchQuery"
                >
                </v-text-field>
            </div>

        </div>

    </div>
</template>

<script>
export default {
    name: "Header",
    data() {
        return {
            query: '',
            documents: [],
        };
    },
    methods: {
        sendSearchQuery() {
            this.$emit('search-query', this.query);
            this.get
        }
    }
}
</script>

<style scoped lang="scss">
.headerContainer {
    position: fixed;
    z-index: 2;
    width: 100vw;
    height: 10vh;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    background-color: rgb(var(--v-theme-primary));
    color: rgb(var(--v-theme-white));
}

.searchQuery {
    color: rgb(var(--v-theme-primary));
}

.queryContainer {
    width: 30%;
}

.headline {
    padding: 0 2%;
}

@media only screen and (max-width: 900px) {
    .queryContainer {
        width: 90%;
        margin-right: 2%;
    }

    .headline {
        font-size: 6vw
    }
}

@media only screen and (max-width: 600px) {
    .queryContainer {
        width: 96%;
        margin-left: 2%;

    }

    .headline {
        display: none
    }
}
</style>
