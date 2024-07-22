<template>
  <v-footer height="40" app class="footer">
    <a
      href="https://github.com/malais00/MSE_Group_Project"
      title="GitHub"
      class="d-inline-block mx-2 social-link"
      rel="noopener noreferrer"
      target="_blank"
    >
      <v-icon
        icon="mdi-github"
        :size="24"
      />
    </a>
      <div class="d-inline-block mx-2 social-link" style="cursor: pointer">
          <v-icon
              icon="mdi-theme-light-dark"
              :size="24"
              @click="toggleTheme()"
          />
      </div>


    <div
      class="text-caption text-disabled"
      style="position: absolute; right: 16px; display: flex; align-items: center"
    >
      <span class="d-none d-sm-inline-block">SS2024 Modern Search Engines</span>
      —
        <a
            class="text-decoration-none on-surface"
            href="https://uni-tuebingen.de/"
            rel="noopener noreferrer"
            target="_blank"
        >
            <img class="uniImg" :src="uniTuebingenIcon">
      </a>
    </div>
  </v-footer>
</template>

<script>
import uniTuebingenIcon from "@/assets/Logo_Universitaet_Tuebingen.svg"
import { useTheme } from 'vuetify'

export default {
    name: "Header",
    data() {
        return {
            items: [
                {
                    title: 'GitHub',
                    icon: `mdi-github`,
                    href: 'https://github.com/malais00/MSE_Group_Project',
                },
                {
                    title: 'Change Theme',
                    icon: `mdi-theme-light-dark`,
                    href: '',
                },
            ],
            theme: useTheme(),
            uniTuebingenIcon,
        };
    },
    methods: {
        changeTheme() {
            const currentTheme = this.$vuetify.theme.global.name.value;
            let newTheme = 'customTheme';
            if(currentTheme === 'customTheme') {
                newTheme = 'customDarkTheme'
            }
            this.theme.global.name.value = newTheme;
        }
    }
}
</script>

<script setup>
import { useTheme } from 'vuetify'

const theme = useTheme()

function toggleTheme () {
    const currentTheme = theme.global.name.value;
    let newTheme = 'customTheme';
    if(currentTheme === 'customTheme') {
        newTheme = 'customDarkTheme'
    }
    theme.global.name.value = newTheme
}
</script>

<style scoped lang="sass">
  .social-link :deep(.v-icon)
    color: rgba(var(--v-theme-on-background), var(--v-disabled-opacity))
    text-decoration: none
    transition: .2s ease-in-out

    &:hover
      color: rgb(var(--v-theme-primary))
</style>

<style scoped lang="scss">
    .footer {
        background-color: rgb(var(--v-theme-neutral));
        border-radius: 8px 8px 0 0;
    }
    .uniImg {
        height: 3vh;
        margin-left: 4px;
    }
</style>
