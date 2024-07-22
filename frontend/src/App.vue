<template>
    <v-app>
        <Header
            @search-query="(query, b_okapi25_parameter, k1_okapi25_parameter, diversity_okapi25_parameter, fairness_okapi25_parameter, pagerank_weight_parameter) =>
            searchQuery(query, 0, b_okapi25_parameter, k1_okapi25_parameter, diversity_okapi25_parameter, fairness_okapi25_parameter, pagerank_weight_parameter, true)"
            @show-spellchecker="showSpellchecker = true"
            @hide-spellchecker="showSpellchecker = false"
            :show-spellchecker="showSpellchecker"
            :corrected-query="correctedQuery"
        />

        <v-main>
            <ResultDocuments
                :searchResults="searchResults"
                :loading-results="loadingResults"
                :maxDocumentsReached="maxDocumentsReached"
                :current-query="currentQueryReadOnly"
                class="resultDocuments"
                @fetchMoreResults="(index) => searchQuery(currentQueryReadOnly, index, b_okapi25_parameterReadOnly, k1_okapi25_parameterReadOnly, diversity_okapi25_parameterReadOnly, fairness_okapi25_parameterReadOnly, pagerank_weight_parameterReadOnly, false)"
            />
        </v-main>

        <AppFooter class="footer"/>
        <v-snackbar
            v-model="snackbarActivator"
            bottom
            timeout="5000"
            :color="snackbarColor"
            style="bottom: 9vh"
        >{{ snackbarText }}</v-snackbar>
    </v-app>
</template>

<script>
import ResultDocuments from "@/components/ResultDocuments";
import Header from "@/components/Header";
import AppFooter from "@/components/AppFooter";
import * as request from "@/api/request";
import {checkResponseStatus} from "@/util/check";

export default {
    name: "CategoryFilter",
    data() {
        return {
            ResultDocuments,
            Header,
            AppFooter,
            loadingResults: false,
            searchResults: [],
            currentQueryReadOnly: '',
            b_okapi25_parameterReadOnly: 0.0,
            k1_okapi25_parameterReadOnly: 0.0,
            diversity_okapi25_parameterReadOnly: 0.0,
            fairness_okapi25_parameterReadOnly: 0.0,
            pagerank_weight_parameterReadOnly: 0.0,
            snackbarActivator: false,
            snackbarText: '',
            snackbarColor: 'error',
            showSpellchecker: false,
            correctedQuery: '',
            maxDocumentsReached: false,
        }
    },
    methods: {
        async searchQuery(query, index, b_okapi25_parameter, k1_okapi25_parameter, diversity_okapi25_parameter, fairness_okapi25_parameter, pagerank_weight_parameter, initialQuery=false) {
            if(initialQuery) {
                this.maxDocumentsReached = false;
            }
            this.currentQueryReadOnly = query;
            this.b_okapi25_parameterReadOnly = b_okapi25_parameter;
            this.k1_okapi25_parameterReadOnly = k1_okapi25_parameter;
            this.diversity_okapi25_parameterReadOnly = diversity_okapi25_parameter;
            this.fairness_okapi25_parameterReadOnly = fairness_okapi25_parameter;
            this.pagerank_weight_parameterReadOnly = pagerank_weight_parameter;
            if(query !== "") {
                this.loadingResults = true;
                try {
                    const response = await request.getRequest("/query/"+query+"/"+index+"/okapi/"+b_okapi25_parameter+"/"+k1_okapi25_parameter+"/"+diversity_okapi25_parameter+"/"+fairness_okapi25_parameter+"/pagerank/"+pagerank_weight_parameter);
                    if(await checkResponseStatus(200, response)) {
                        const res = await response.json();
                        if(res.length < 10) {
                            this.maxDocumentsReached = true;
                        }
                        if(initialQuery) {
                            this.searchResults = res;
                        } else {
                            this.searchResults = this.searchResults.concat(res);
                        }
                        this.loadingResults = false;
                    } else {
                        this.showSnackbar('Something went wrong searching for documents.', 'error');
                        this.loadingResults = false;
                    }
                } catch (e) {
                    this.showSnackbar('Something went wrong searching for documents.', 'error');
                    this.loadingResults = false;
                }
                this.checkSpelling(query); // Don't await this for performance reasons
            }
        },

        async checkSpelling(query) {
            const response = await request.getRequest("/query/spellcheck/"+query);
            if(await checkResponseStatus(200, response)) {
                const res = await response.json();
                if(res['misspelled']) {
                    this.showSpellchecker = true;
                    this.correctedQuery = res['corrected_query'];
                }
            }
        },

        showSnackbar(text, color) {
            this.snackbarActivator = true;
            this.snackbarText = text;
            this.snackbarColor = color;
        },

        async getNextDocuments(query, index) {
            const response = await request.getRequest("/query/"+query+"/"+index);
            await checkResponseStatus(200, response);
            const res = await response.json();
            this.searchResults = res;
        },

        async getDetails(documentId) {
            const response = await request.getRequest("/document/details/"+documentId);
            await checkResponseStatus(200, response);
            const res = await response.json();
            const documentDetails = res;
        }
    }
}
</script>

<style lang="scss">
#app {
}

.resultDocuments {
    width: 100vw;
    height: calc(90vh - 40px);
    margin-top: 10vh;

}

.footer {

}
</style>

<style>
html, body {
    overflow: hidden; /* Hide scrollbar on main html and body */
    height: 100%; /* Ensure the body takes full height */
    margin: 0; /* Remove default margin */
}
</style>
