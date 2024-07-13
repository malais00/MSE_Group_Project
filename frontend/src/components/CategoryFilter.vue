<template>
    <div class="filterContainer">
        <v-chip-group
            v-model="selectedCategories"
            active-class="primary"
            mandatory
            multiple
            @update:model-value="updateFilter()"
        >
            <v-chip
                v-for="category in categories"
                :key="category.name"
                variant="elevated"
                :color="selectedCategories.includes(category.name) ? 'primary' : 'grey'"
                style="display: flex; justify-content: space-between; align-items: center"
            >
                <v-icon style="margin-right: 4px">{{ category.icon }}</v-icon>
                {{ category.name }}
            </v-chip>
        </v-chip-group>
    </div>
</template>

<script>
export default {
    name: "CategoryFilter",
    data() {
        return {
            selectedCategories: [0],
            categories: [
                {
                    "name": "All",
                    "icon": "mdi-filter"
                },
                {
                    "name": "Pictures",
                    "icon": "mdi-image"
                },
                {
                    "name": "News",
                    "icon": "mdi-newspaper"
                },
                {
                    "name": "Videos",
                    "icon": "mdi-video"
                },
                {
                    "name": "Maps",
                    "icon": "mdi-map"
                },
                {
                    "name": "Shopping",
                    "icon": "mdi-cart"
                },
                {
                    "name": "Books",
                    "icon": "mdi-book"
                },
                {
                    "name": "Flights",
                    "icon": "mdi-airplane"
                }
            ]
        };
    },
    methods: {
        updateFilter() {
            console.log(this.selectedCategories);
            this.$emit("filter-changed", this.selectedCategories);
        }
    }
}
</script>

<style lang="scss">
.filterContainer {
    display: flex;
    justify-content: space-between;
}
</style>
