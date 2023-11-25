<template>
    <div class="download-form">
        <strong>{{ fileName }}</strong>
        <button @click="downloadFile" class="button download-button">Скачать файл</button>
    </div>
</template>
<script setup   lang="ts">
import { defineProps } from 'vue';
import axios from 'axios';

const props = defineProps({
    fileName: { type: String, required: true },
})

const downloadFile = async () => {
    try {
        var fileUrl = '/synopsis/download?file_name=' + props.fileName
        const response = await axios.get(fileUrl, {
            responseType: 'blob'
        });

        // Создание ссылки для скачивания файла
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.download = props.fileName + '.md';
        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Ошибка при загрузке файла:', error);
    }
};



</script>

<style>
.download-button {
    margin-left: auto;
    margin-right: 0.7em;
}

.download-form {
    border: 2px solid #4CAF50;
    /* Цвет границы */
    border-radius: 15px;
    /* Радиус закругления углов */
    padding: 15px;
    /* Внутренний отступ для отступа содержимого от границ */
    max-width: 600px;
    /* Максимальная ширина контейнера */
    margin: auto;
    /* Центрирование контейнера */
    text-align: center;
    /* Выравнивание текста и элементов внутри по центру */
    display: flex;
    align-items: center;
    gap: 10px;
    /* Отступ между элементами */
}
</style>