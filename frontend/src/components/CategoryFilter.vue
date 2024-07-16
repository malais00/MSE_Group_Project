<template>
    <div class="filterContainer">
        <v-chip
            v-for="(category, i) in categories"
            :key="category.name"
            variant="elevated"
            :color="selectedCategories.includes(category.name) ? 'primary' : ''"
            style="display: flex; justify-content: space-between; align-items: center; margin: 0 4px"
            @click="handleChipClick(category.name)"
        >
            <v-icon class="categoryIcon">{{ category.icon }}</v-icon>
            <span class="categoryName">{{ category.name }}</span>
        </v-chip>
    </div>
</template>

<script>
export default {
    name: "CategoryFilter",
    data() {
        return {
            selectedCategories: ['All'],
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
        updateFilter(selection) {
            // Emit the selected categories whenever the selection changes
            this.$emit("filter-changed", this.selectedCategories);
        },

        handleChipClick(category) {
            if (category === 'All') {
                // If "All" is clicked, deselect all other categories and select only "All"
                this.selectedCategories = ['All'];
            } else {
                // If any other category is clicked and "All" was selected, deselect "All"
                if (this.selectedCategories.includes('All')) {
                    this.selectedCategories = this.selectedCategories.filter(cat => cat !== 'All');
                }

                // Toggle the selection of the clicked category
                const index = this.selectedCategories.indexOf(category);
                if (index === -1) {
                    this.selectedCategories.push(category);
                } else {
                    this.selectedCategories.splice(index, 1);
                }

                // If no categories are selected, select "All" by default
                if (this.selectedCategories.length === 0) {
                    this.selectedCategories = ['All'];
                }
            }

            this.updateFilter();
        }
    }
}
</script>

<style lang="scss">
.filterContainer {
    display: flex;
}

.categoryIcon {
    margin-right: 4px
}

@media only screen and (max-width: 780px) {
    .categoryName {
        display: none;
    }

    .categoryIcon {
        margin-right: 0px
    }
}
</style>
