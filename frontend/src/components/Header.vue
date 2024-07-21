<template>
    <div class="headerContainer">
        <div style="display: flex; flex-direction: row; width: 100%; height: 100%; justify-content: flex-start; align-items: center">
            <h1 class="headline">TübiSearch</h1>
            <div
                class="queryContainer"
            >
                <div
                    style="overflow: hidden"
                    :style="showSpellchecker ? 'border-radius: 8px 8px 0 0' : 'border-radius: 8px'"
                >
                    <v-text-field
                        v-model="query"
                        variant="solo"
                        density="compact"
                        hide-details="hide-details"
                        append-inner-icon="mdi-magnify"
                        clearable
                        bg-color="white"
                        class="searchQuery"
                        rounded="0"
                        @click:appendInner="sendSearchQuery"
                        @keydown.enter="sendSearchQuery"
                    >
                    </v-text-field>
                </div>
                <div
                    v-if="showSpellchecker"
                    class="spellcheckContainer"
                >
                    <v-divider></v-divider>
                    <span @click="sendSpellcheckedQuery" style="cursor: pointer">
                        Did you mean: {{ correctedQuery }}
                    </span>
                    <div
                        style="width: 100%; display: flex; justify-content: center"
                        @click="$emit('hide-spellchecker')"
                    >
                        <v-icon>mdi-menu-up-outline</v-icon>
                    </div>
                </div>
            </div>
            <v-menu
                :close-on-content-click="false"
            >
                <template v-slot:activator="{ props }">
                    <v-btn
                        v-bind="props"
                        style="margin-left: 2%"
                    >
                        <v-icon color="primary">mdi-cog</v-icon>
                    </v-btn>
                </template>
                <v-card style="width: 25vw">
                    <v-card-title>Okapi25</v-card-title>
                    <v-card-subtitle>Tweak your parameters!</v-card-subtitle>
                    <v-card-text>
                        <div class="okapiContainer">
<!--                            <span class="okapiText">Okapi25</span>-->
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
                                            <span class="parameterTitle">b</span>
                                            <v-slider
                                                v-model="b_okapi25_parameter"
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
                                            <span class="parameterTitle">k1</span>
                                            <v-slider
                                                v-model="k1_okapi25_parameter"
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
                                <v-tooltip
                                    :text="diversity_description"
                                    location="bottom"
                                >
                                    <template v-slot:activator="{ props }">
                                        <div
                                            class="sliderContainer"
                                            v-bind="props"
                                        >
                                            <span class="parameterTitle">Diversity</span>
                                            <v-slider
                                                v-model="diversity_okapi25_parameter"
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
                    </v-card-text>
                </v-card>
            </v-menu>
        </div>
    </div>
</template>

<script>
export default {
    name: "Header",
    props: {
        showSpellchecker: {
            type: Boolean,
            required: false,
            default: false
        },
        correctedQuery: {
            type: String,
            required: false,
            default: ''
        }
    },
    data() {
        return {
            query: '',
            documents: [],
            b_okapi25_parameter: 0.75,
            k1_okapi25_parameter: 1.5,
            diversity_okapi25_parameter: 1.5,
            b_description: "The b parameter makes sure that search results aren't biased towards very long or very short documents.",
            k1_description: "The k1 parameter ensures that documents with more instances of the search term are ranked higher.",
            diversity_description: "The diversity parameter in search engine queries helps ensure that the search results include a wide variety of information on the topic, rather than repeating similar content."
        };
    },
    methods: {
        sendSearchQuery() {
            this.$emit('search-query', this.query, this.b_okapi25_parameter, this.k1_okapi25_parameter, this.diversity_okapi25_parameter)
        },
        sendSpellcheckedQuery() {
            this.query = this.correctedQuery;
            this.$emit('hide-spellchecker');
            this.$emit('search-query', this.query, this.b_okapi25_parameter, this.k1_okapi25_parameter, this.diversity_okapi25_parameter);

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
    position: relative;
    color: rgb(var(--v-theme-primary));
    z-index: 2;
}

.queryContainer {
    position: relative;
    width: 30%;
}

.headline {
    padding: 0 2%;
}

.okapiContainer {
    display: flex;
    flex-direction: row;
    margin: 0 2%;
    width: 100%;
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

.spellcheckContainer {
    position: absolute;
    width: fit-content;
    min-width: 100%;
    max-width: 200%;
    padding: 4px;
    height: fit-content;
    background-color: white;
    color: black;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), /* bottom shadow */
    4px 0 8px rgba(0, 0, 0, 0.2), /* right shadow */
    -4px 0 8px rgba(0, 0, 0, 0.2); /* left shadow */
    border-radius: 0 0 8px 8px;
    z-index: 1;
    cursor: pointer;
}

.parameterTitle {
    width: 64px;
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
