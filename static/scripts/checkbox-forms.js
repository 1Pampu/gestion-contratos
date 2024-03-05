function alternarFormulario(formulario_id, selector_id, campos_lista){
    var formulario = document.getElementById(formulario_id);
    var selector = document.getElementById(selector_id);

    if(formulario.style.display == 'none'){
        // Mostrar formulario
        formulario.style.display = 'flex';
        // Deshabilitar el selector y quitarle el atributo required
        selector.setAttribute('disabled', 'disabled')
        selector.removeAttribute('required')
        selector.value = ''
        // Agregar el atributo required a todos los campos nuevos
        campos_lista.forEach(function(campo){
            document.getElementById(campo).setAttribute('required', 'required')
        });
    } else {
        // Ocultar formulario
        formulario.style.display = 'none';
        // Habilitar el selector y agregarle el atributo required
        selector.removeAttribute('disabled')
        selector.setAttribute('required', 'required')
        // Quitar el atributo required a todos los campos nuevos
        campos_lista.forEach(function(campo){
            document.getElementById(campo).removeAttribute('required')
        });
    }
}