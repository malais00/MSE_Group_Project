<template>
    <v-app>
        <Header
            @search-query="(query) => searchQuery(query, 0)"
        />

        <v-main>
            <ResultDocuments
                :searchResults="searchResults"
                :loading-results="loadingResults"
                class="resultDocuments"
                @fetchMoreResults="(index) => searchQuery(currentQueryReadOnly, index)"
            />
        </v-main>

        <AppFooter class="footer"/>
    </v-app>
</template>

<script>
import ResultDocuments from "@/components/ResultDocuments";
import Header from "@/components/Header";
import AppFooter from "@/components/AppFooter";
import * as request from "@/api/request";
import {checkResponseStatus} from "@/util/check";
import {preprocessQuery} from "@/util/queryPreprocessing";

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
        }
    },
    methods: {
        async searchQuery(query, index) {
            this.currentQueryReadOnly = query;
            if(query !== "") {
                this.loadingResults = true;
                const response = await request.getRequest("/query/"+query+"/"+index);
                await checkResponseStatus(200, response);
                const res = await response.json();
                if(this.searchResults.length === 0) {
                    this.searchResults = res;
                } else {
                    this.searchResults = this.searchResults.concat(res);
                    console.log("new search results: ", res);
                    console.log(this.searchResults);
                }
                this.loadingResults = false;
            }
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
