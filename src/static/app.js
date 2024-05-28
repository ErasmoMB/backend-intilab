function getAuthors() {
    $.ajax({
        url: "http://localhost:5000/authors",
        type: "GET",
        success: function(data) {
            var authors = data;
            var html = "";
            for (var i = 0; i < authors.length; i++) {
                html += "<tr>";
                html += "<td>" + authors[i]._id + "</td>";
                html += "<td><img src='" + authors[i].image + "' alt='Imagen del autor' style='width: 100px; height: 100px;'></td>";
                html += "<td>" + authors[i].academic_degrees.join("<br>") + "</td>"; // Modificado aquí
                html += "<td>";
                html += "<button class='update-button btn btn-primary' data-id='" + authors[i]._id + "'>Actualizar</button> ";
                html += "<button class='delete-button btn btn-danger' data-id='" + authors[i]._id + "'>Eliminar</button>";
                html += "</td>";
                html += "</tr>";
            }
            $("#authors-table tbody").html(html);
        },
        error: function(error) {
            alert("Hubo un error al obtener los autores");
        }
    });
}

var selectedAuthorId; // Variable global para almacenar el ID del autor seleccionado

$(document).ready(function() {
    $.getJSON('http://localhost:5000/autor')
        .done(function(data) {
            console.log(data);
            var select = $('#autores');
            $.each(data.autores, function(id, author) {
                select.append('<option value="' + id + '">' + author.name + '</option>');
            });
            select.change(function() {
                selectedAuthorId = $(this).val(); // Almacenar el ID del autor seleccionado
                console.log('Autor seleccionado: ' + selectedAuthorId);
            });
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.log("Error: " + textStatus + ", " + errorThrown);
        });

    $("#add-academic-degree").click(function() {
        $("#academic-degrees").append('<input type="text" class="academic-degree form-control" name="academic_degrees[]">');
    });
});

$("#create-author-form").submit(function(e) {
    e.preventDefault();

    var image = $("#image")[0].files[0]; // Obteniendo el archivo de imagen
    var academic_degrees = $(".academic-degree").map(function(){return $(this).val();}).get(); // Obteniendo todos los grados académicos

    var formData = new FormData();
    formData.append('id', selectedAuthorId); // Usar el ID del autor seleccionado
    formData.append('image', image);
    for(var i = 0; i < academic_degrees.length; i++){
        formData.append('academic_degrees', academic_degrees[i]);
    }

    $.ajax({
        url: "/authors",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            alert("Autor creado con éxito");
            getAuthors();
            // Vaciar los campos del formulario
            $("#id").val("");
            $("#image").val("");
            $(".academic-degree").val("");
        },
        error: function(error) {
            alert("Hubo un error al crear el autor");
        }
    });
});
$(document).on("click", ".update-button", function() {
    var id = $(this).data("id");

    // Obtener los datos actuales del autor
    $.ajax({
        url: "/authors/" + id,
        type: "GET",
        success: function(data) {
            // Crear un formulario para seleccionar la nueva imagen y los grados académicos
            var form = $("<form id='update-form' class='container' style='max-width: 500px;'>");
            form.append("<div class='form-group'><input type='file' id='update-image' class='form-control-file'></div>");
            var academicDegreesDiv = $("<div class='form-group' id='update-academic-degrees'></div>");
            for(var i = 0; i < data.academic_degrees.length; i++){
                academicDegreesDiv.append('<input type="text" class="academic-degree form-control" style="max-width: 300px;" value="' + data.academic_degrees[i] + '">');
            }
            form.append(academicDegreesDiv);
            form.append("<button type='button' id='add-update-academic-degree' class='btn btn-primary'>Añadir otro grado académico</button>");
            form.append("<input type='submit' value='Actualizar' class='btn btn-success mt-3'>");
            form.append("<button type='button' id='cancel-update' class='btn btn-danger mt-3'>Cancelar</button>");
            $(".container").append(form);

            $("#add-update-academic-degree").click(function() {
                $("#update-academic-degrees").append('<input type="text" class="academic-degree form-control" style="max-width: 300px;" placeholder="Ingrese los grados académicos separados por coma">');
            });

            $("#cancel-update").click(function() {
                form.remove();
            });

            $("#update-form").submit(function(e) {
                e.preventDefault();

                var image = $("#update-image")[0].files[0]; // Obteniendo el archivo de imagen
                var academic_degrees = $(".academic-degree").map(function(){return $(this).val();}).get(); // Obteniendo todos los grados académicos

                var formData = new FormData();
                formData.append('image', image);
                for(var i = 0; i < academic_degrees.length; i++){
                    formData.append('academic_degrees', academic_degrees[i]);
                }

                $.ajax({
                    url: "/authors/" + id,
                    type: "PUT",
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(data) {
                        alert("Autor actualizado con éxito");
                        getAuthors();
                        form.remove(); // Eliminar el formulario después de la actualización
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        alert(jqXHR.responseJSON.message);
                    }
                });
            });
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseJSON.message);
        }
    });
});

$(document).on("click", ".delete-button", function() {
    var id = $(this).data("id");

    $.ajax({
        url: "/authors/" + id,
        type: "DELETE",
        success: function(data) {
            alert("Autor eliminado con éxito");
            getAuthors();
        },
        error: function(error) {
            alert("Hubo un error al eliminar el autor");
        }
    });
});



getAuthors();