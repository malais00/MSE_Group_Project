<template>
    <div>
        <div class="resultDocumentsContainer" @scroll="handleScroll">
            <!--            <CategoryFilter/>-->
            <div
                v-if="loadingResults && searchResults.length === 0 && !maxDocumentsReached"
                class="readyInfo"
            >
                <v-progress-circular
                    indeterminate
                    size="64"
                    color="primary"
                />
            </div>
            <div
                v-else-if="searchResults.length !== 0"
                v-for="doc in searchResults"
                :key="doc.url"
            >
                <div class="docContainer">
                    <div class="percentileDiv">
                        <div class="percentileLine" :style="`bottom: ${scalePercentileLine(doc.percentile)}px`"></div>
                        <!--                        <span>{{doc.percentile }}</span>-->
                    </div>

                    <v-divider vertical :thickness="2" style="margin-right: 12px"></v-divider>

                    <div style="display: flex; flex-direction: row; align-items: center">
                        <div style="display: flex; flex-direction: column">
                            <div style="display: flex; flex-direction: row; align-items: center">
                                <v-icon v-if="doc.favicon === '' || doc.favicon === undefined">mdi-web</v-icon>
                                <img class="faviconDoc" alt="" :src="doc.favicon ? doc.favicon : ''">
                                <h2>{{ doc.title }}</h2>
                            </div>
                            <a style="width: fit-content" :href="doc.url">{{ doc.url }}</a>
                            <p v-html="highlightedDescription(doc.description)"></p>
                        </div>
                    </div>
                </div>
            </div>
            <div
                v-else
                class="readyInfo"
            >Let's explore Tübingen</div>
            <div v-if="searchResults.length !== 0 && loadingResults && !maxDocumentsReached">
                <v-progress-circular
                    indeterminate
                    size="64"
                    color="primary"
                />
            </div>
        </div>
    </div>
</template>

<script>
import CategoryFilter from "@/components/CategoryFilter.vue";
import * as request from "@/api/request";
import {checkResponseStatus} from "@/util/check";

export default {
    name: "ResultDocuments",
    components: {CategoryFilter},
    props: {
        searchResults: {
            type: Array,
            required: true
        },
        loadingResults: {
            type: Boolean,
            required: true
        },
        maxDocumentsReached: {
            type: Boolean,
            required: true
        },
        currentQuery: {
            type: String,
            required: true
        },
    },
    data() {
        return {};
    },
    watch: {
        // Watch for changes in searchResults and fetch descriptions for new documents
        searchResults() {
            this.searchResults.forEach(async (doc) => {
                if(doc.description === undefined) {
                    doc.description = await this.getDocumentDescription(doc.url);
                }
            });
        }
    },
    methods: {
        // Fetch more results when the user scrolls to the bottom of the page
        handleScroll(event) {
            if(this.maxDocumentsReached) {
                return;
            }
            const container = event.target;
            if (container.scrollTop + container.clientHeight >= container.scrollHeight - 500 && !this.loadingResults) {
                this.fetchMoreResults();
            }
        },

        fetchMoreResults() {
            if (!this.loadingResults && this.searchResults.length !== 0) {
                this.$emit('fetchMoreResults', this.searchResults.length / 10);
            }
        },

        // Fetch a description for the url by using a backend proxy to escape CORS problems
        async getDocumentDescription(url) {
            const response = await request.getRequest("/document/first-paragraph/"+this.currentQuery + "?url=" + url);
            if(await checkResponseStatus(200, response)) {
                const res = await response.json();
                if(res.first_paragraph !== undefined) {
                    return res.first_paragraph;
                } else {
                    return '';
                }
            }
            return '';
        },

        // Scale the percentile line to fit the 0-100 range (tweak it a little because most values are above 25/50)
        scalePercentileLine(percentile) {
            if (percentile < 25) {
                return 0;
            }
            let normalizedPercentile = percentile - 25;
            let scaledPercentile = normalizedPercentile * (100 / 75);
            return (scaledPercentile / 100) * 60;
        },

        // Highlight the search query in the description
        highlightedDescription(description) {
            if (!description || !this.currentQuery) return description;
            const queries = this.currentQuery.split(' ');
            queries.forEach(query => {
                const regex = new RegExp(`(${query})`, 'gi');
                description = description.replace(regex, '<strong>$1</strong>');
            });
            return description;
        }
    }
}
</script>

<style lang="scss">
.resultDocumentsContainer {
    overflow: auto;
    color: rgb(var(--v-theme-slider));
    padding: 2%;
    height: 100%;
}

.docContainer {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    padding: 2vh 0;
}

.readyInfo {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 70vh;
    font-size: 2em;
}

.faviconDoc {
    width: 24px;
    height: 24px;
    margin-right: 8px
}

.percentileDiv {
    position: relative;
    min-width: 12px;
    min-height: 64px;
    max-width: 12px;
    max-height: 64px;
    margin-right: 18px;
    background: linear-gradient(to bottom, #00be00, rgb(var(--v-theme-primary)));
    border-radius: 8px;
    border: 1px solid black;
}

.percentileLine {
    position: absolute;
    min-width: 19px;
    min-height: 2px;
    left: -4px;
    background: rgb(var(--v-theme-slider));
}

</style>
