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
            >
                <div class="docContainer">
                    <div class="percentileDiv">
                        <div class="percentileLine"></div>
                    </div>

                    <div style="display: flex; flex-direction: row; align-items: center">
                        <div style="display: flex; flex-direction: column">
                            <div style="display: flex; flex-direction: row; align-items: center">
                                <v-icon v-if="doc.favicon === '' || doc.favicon === undefined">mdi-web</v-icon>
                                <img class="faviconDoc" alt="" :src="doc.favicon ? doc.favicon : ''">
                                <h2>{{ doc.title }}</h2>
                            </div>
                            <a style="width: fit-content" :href="doc.url">{{ doc.url }}</a>
                            <p>{{ doc.description }}</p>
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
        return {

        };
    },
    watch: {
        searchResults() {
            this.searchResults.forEach(async (doc) => {
                if(doc.description === undefined) {
                    doc.description = await this.getDocumentDescription(doc.url);
                }
            });
        }
    },
    methods: {
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
                console.log("fetching more results: ", this.searchResults.length / 10);
                this.$emit('fetchMoreResults', this.searchResults.length / 10);
            }
        },
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
        }
    }
}
</script>

<style lang="scss">
.resultDocumentsContainer {
    overflow: auto;
    color: rgb(var(--v-theme-font));
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
    min-height: 48px;
    max-width: 12px;
    max-height: 48px;
    background: linear-gradient(to bottom, green, red);
    border-radius: 25px;
    border: 1px solid black;
}

.percentileLine {
    position: absolute;
    min-width: 11px;
    min-height: 2px;
    bottom: 12px;
    background: black;
}
</style>
