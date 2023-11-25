<template>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Видео загрузчик</title>

    </head>
    <div class="home">
        <img style="max-width:350px; margin-top: 30px;" :src="require('@/assets/GeekNeiro.png')" />

        <FileUploadComponentVue />
    </div>
</template>

<script setup lang="ts">
import FileUploadComponentVue from "@/components/FileUploadComponent.vue";

</script>
