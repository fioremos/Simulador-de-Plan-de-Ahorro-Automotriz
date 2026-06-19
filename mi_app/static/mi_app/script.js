document.addEventListener("DOMContentLoaded", function () {

    inicializarPestañasFormulario();
    inicializarSeleccionVehiculos();
    inicializarEnvioSimulador();
    inicializarConversorDolar();
    activarBotonPorValidacion();

});

function inicializarPestañasFormulario() {
    const tabs = document.querySelectorAll(".tab-btn");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", function () {
            tabs.forEach(t => t.classList.remove("active"));

            contents.forEach(c => c.classList.remove("active"));

            this.classList.add("active");

            const targetId = this.getAttribute("data-tab");
            document.getElementById(targetId).classList.add("active");
        });
    });
}

function inicializarSeleccionVehiculos() {
    const tarjetas = document.querySelectorAll(".tarjeta");
    const inputVehiculo = document.getElementById("input-vehiculo");
    const selectModelo = document.getElementById("modelo");
    const asideInforme = document.getElementById("informe-resultado");

    tarjetas.forEach(tarjeta => {
        tarjeta.addEventListener("click", function () {

            tarjetas.forEach(t => {
                t.classList.remove("seleccionada");
                const boton = t.querySelector(".btn");
                if (boton) boton.textContent = "Seleccionar";
            });

            this.classList.add("seleccionada");

            const botonActual = this.querySelector(".btn");
            if (botonActual) botonActual.textContent = "Seleccionado";

            const nombreAuto = this.querySelector(".car-names").textContent;
            const precioAuto = this.querySelector("p strong").textContent;
            const srcImagen = this.querySelector("img").getAttribute("src");

            if (inputVehiculo) inputVehiculo.value = nombreAuto;

            if (selectModelo) {
                selectModelo.innerHTML = "";

                const nuevaOpcion = document.createElement("option");
                nuevaOpcion.value = nombreAuto.toLowerCase().replace(" ", "_");
                nuevaOpcion.textContent = nombreAuto;
                nuevaOpcion.selected = true;

                selectModelo.appendChild(nuevaOpcion);
            }

            if (asideInforme) {
                const carNamePlace = asideInforme.querySelector(".car-name");
                const carPricePlace = asideInforme.querySelector(".car-price");
                const carImgPlace = asideInforme.querySelector(".img-mini");

                if (carNamePlace) carNamePlace.textContent = nombreAuto;
                if (carPricePlace) carPricePlace.textContent = precioAuto;
                if (carImgPlace) carImgPlace.setAttribute("src", srcImagen);
            }
        });
    });
}

function inicializarEnvioSimulador() {
    const formulario = document.getElementById("form-simulador");
    const contenedorErrores = document.getElementById("contenedor-errores");
    const listaErrores = document.getElementById("lista-errores");
    const informeResultado = document.getElementById("informe-resultado");

    if (!formulario) return;

    formulario.addEventListener("submit", function (evento) {
        evento.preventDefault();

        if (contenedorErrores) contenedorErrores.style.display = "none";
        if (informeResultado) informeResultado.style.display = "none";
        if (listaErrores) listaErrores.innerHTML = "";

        const tarjetaSeleccionada = document.querySelector(".tarjeta.seleccionada");
        if (tarjetaSeleccionada) {
            const nombreAuto = tarjetaSeleccionada.querySelector(".car-names").textContent;
            document.getElementById("input-vehiculo").value = nombreAuto;
        }

        const datosFormulario = new FormData(formulario);

        fetch(formulario.action, {
            method: "POST",
            body: datosFormulario,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success === false) {
                if (contenedorErrores) {
                    contenedorErrores.style.display = "block";
                    if (data.motivos) {
                        data.motivos.forEach(m => {
                            const li = document.createElement("li");
                            li.textContent = m;
                            listaErrores.appendChild(li);
                        });
                    } else if (data.errores) {
                        for (let campo in data.errores) {
                            const li = document.createElement("li");
                            li.textContent = `${data.errores[campo].join(", ")}`;
                            listaErrores.appendChild(li);
                        }
                    }
                    contenedorErrores.scrollIntoView({ behavior: 'smooth' });
                }
            }
            else if (data.success === true && data.informe) {
                alert("¡Solicitud enviada con éxito!\nSu informe de financiamiento ha sido generado correctamente.");
                const inf = data.informe;

                if (tarjetaSeleccionada) {
                    const nombreAuto = tarjetaSeleccionada.querySelector(".car-names").textContent;
                    const srcImagen = tarjetaSeleccionada.querySelector("img").getAttribute("src");

                    informeResultado.querySelector(".car-name").textContent = nombreAuto;
                    informeResultado.querySelector(".img-mini").setAttribute("src", srcImagen);
                }

                informeResultado.querySelector(".car-price").textContent = inf.vehiculo_valor;

                document.getElementById("inf-tipo-plan").textContent = inf.tipo_plan;
                document.getElementById("inf-monto-adjudicar").textContent = inf.importe_adjudicacion;
                document.getElementById("inf-monto-retiro").textContent = inf.importe_retiro_patentamiento;
                document.getElementById("inf-tasa").textContent = inf.tasa_interes;
                document.getElementById("inf-cuota").textContent = inf.valor_cuota_mensual;

                informeResultado.style.display = "block";
                informeResultado.scrollIntoView({ behavior: 'smooth' });
            }
        })
        .catch(error => {
            console.error("Error crítico:", error);
        });
    });
}

function inicializarConversorDolar() {
    const urlApiDolar = "https://dolarapi.com/v1/dolares/oficial";
    let cotizacionOficial = null;

    const inputIngresoT = document.getElementById("ingreso_t");
    const cartelT = document.getElementById("conversor-ingreso-t");

    const inputIngresoG = document.getElementById("ingreso_g");
    const cartelG = document.getElementById("conversor-ingreso-g");

    if (!inputIngresoT || !inputIngresoG) return;

    fetch(urlApiDolar)
        .then(response => {
            if (!response.ok) throw new Error("Error al obtener la cotización");
            return response.json();
        })
        .then(data => {
            cotizacionOficial = parseFloat(data.venta);
            console.log(`Cotización del dólar oficial obtenida: $${cotizacionOficial}`);
        })
        .catch(error => {
            console.error("No se pudo conectar con DolarApi:", error);
        });

    function actualizarCartelConversor(input, cartel) {
        if (!cotizacionOficial) return;

        const valorPesos = parseFloat(input.value);

        if (isNaN(valorPesos) || valorPesos <= 0) {
            cartel.style.display = "none";
            cartel.textContent = "";
            return;
        }

        const valorDolares = valorPesos / cotizacionOficial;

        const dolaresFormateados = valorDolares.toLocaleString("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        const cotizacionFormateada = cotizacionOficial.toLocaleString("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

        cartel.textContent = `Este importe equivale a u$s ${dolaresFormateados} bajo la cotización del dólar oficial del día ($${cotizacionFormateada}).`;
        cartel.style.display = "block";
    }

    inputIngresoT.addEventListener("input", function () {
        actualizarCartelConversor(inputIngresoT, cartelT);
    });

    inputIngresoG.addEventListener("input", function () {
        actualizarCartelConversor(inputIngresoG, cartelG);
    });
}

function activarBotonPorValidacion() {
    const formulario = document.getElementById("form-simulador");
    const botonSimular = document.getElementById("btn-simular") || document.querySelector(".btn-simular");

    if (!formulario || !botonSimular) return;

    const camposRequeridos = formulario.querySelectorAll("[required]");

    function comprobarCampos() {
        let todoValido = true;

        camposRequeridos.forEach(campo => {
            if (!campo.checkValidity()) {
                todoValido = false;
            }
        });

        if (todoValido) {
            botonSimular.removeAttribute("disabled");
        } else {
            botonSimular.setAttribute("disabled", "true");
        }
    }

    formulario.addEventListener("input", comprobarCampos);
    formulario.addEventListener("change", comprobarCampos);
}