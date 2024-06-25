
    $(document).ready(function() {
        // Select elementindeki her bir option elemanını dön
        $('#categories-select option').each(function() {
            // Option elemanının içeriğini al
            var optionText = $(this).text();
            var optionValue = $(this).val();

            // Yeni bir checkbox oluştur
            var checkbox = $('<input type="checkbox" />').attr('value', optionValue);
            var label = $('<label class="custom-checkbox"></label>').append(checkbox).append(optionText);

            // Checkbox'ı ve label'ı select elementinin öncesine ekle
            $('#categories-select').before(label);
        });

        // Select elementini gizle
        $('#categories-select').hide();

        // Checkbox'lardan birinin durumu değiştiğinde, ilgili option'ı seçili/seleçili değil olarak ayarla
        $('input[type="checkbox"]').change(function() {
            var value = $(this).val();
            $('#categories-select option[value="' + value + '"]').prop('selected', $(this).is(':checked'));
        });
    });

