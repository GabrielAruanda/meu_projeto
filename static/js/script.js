// scripts.js

// Espera até que o documento esteja completamente carregado
$(document).ready(function() {
    // Adiciona um evento de hover para o elemento com id 'sidebar'
    $('#sidebar').hover(
        // Função executada quando o mouse entra no 'sidebar'
        function() {
            $(this).removeClass('collapsed'); // Remove a classe 'collapsed'
        },
        // Função executada quando o mouse sai do 'sidebar'
        function() {
            $(this).addClass('collapsed'); // Adiciona a classe 'collapsed'
        }
    );

    // Adiciona um evento de clique para elementos com a classe 'toggle-btn'
    $('.toggle-btn').click(function() {
        $('#sidebar').toggleClass('collapsed'); // Alterna a classe 'collapsed' no 'sidebar'
    });
});
