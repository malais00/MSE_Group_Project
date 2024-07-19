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
            <div class="okapiContainer">
                <span class="okapiText">Okapi25</span>
                <div class="sliderGroupContainer">
                    <v-tooltip
                        :text="b_description"
                        location="bottom"
                    >
                        <template v-slot:activator="{ props }">
                            <div
                                class="sliderContainer"
                                v-bind="props"
                            >
                                <span style="width: 12px">b</span>
                                <v-slider
                                    :model-value="b_okapi25_parameter"
                                    :thumb-label="true"
                                    show-ticks="always"
                                    density="compact"
                                    hide-details
                                    thumb-size="10"
                                    step="0.1"
                                    max="1.0"
                                ></v-slider>
                            </div>
                        </template>
                    </v-tooltip>

                    <v-tooltip
                        :text="k1_description"
                        location="bottom"
                    >
                        <template v-slot:activator="{ props }">
                            <div
                                class="sliderContainer"
                                v-bind="props"
                            >
                                <span style="width: 12px">k1</span>
                                <v-slider
                                    :model-value="k1_okapi25_parameter"
                                    :thumb-label="true"
                                    show-ticks="always"
                                    density="compact"
                                    hide-details
                                    thumb-size="10"
                                    step="0.1"
                                    min="0.8"
                                    max="2.0"
                                ></v-slider>
                            </div>
                        </template>
                    </v-tooltip>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Header",
    props: {
    },
    data() {
        return {
            query: '',
            documents: [],
            b_okapi25_parameter: 0.75,
            k1_okapi25_parameter: 1.5,
            b_description: "The b parameter makes sure that search results aren't biased towards very long or very short documents.",
            k1_description: "The k1 parameter ensures that documents with more instances of the search term are ranked higher."
        };
    },
    methods: {
        sendSearchQuery() {
            this.$emit('search-query', this.query, this.b_okapi25_parameter, this.k1_okapi25_parameter);
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

.okapiContainer {
    display: flex;
    flex-direction: row;
    margin: 0 2%;
    width: 60%;
}

.okapiText {
    transform: rotate(-90deg);
    transform-origin: right top;
    margin-right: 28px;
    text-decoration: underline;
}

.sliderGroupContainer {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    width: 100%
}

.sliderContainer {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
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
