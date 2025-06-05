import streamlit as st  
import pandas as pd  
import numpy as np  
import plotly.express as px  
import plotly.graph_objects as go  

# Configuración de página  
st.set_page_config(  
    page_title="Calculadora de Modelos de Costos",  
    page_icon="📊",  
    layout="wide"  
)  

# Inicializar session_state  
if "page" not in st.session_state:  
    st.session_state.page = "caratula"  

# Estilos personalizados  
st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }

    /* Título principal */
    h1 {
        color: #6a5acd;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 30px;
        font-weight: bold;
    }

    /* Sección de información */
    .info-section {
        background-color: #1e1e1e;
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 6px 10px rgba(0,0,0,0.2);
    }

    .info-text {
        color: #b0b0b0;
        font-size: 1.1rem;
        line-height: 1.8;
    }

    /* Sección de creadora */
    .creator-section {
        text-align: center;
        margin-bottom: 40px;
    }

    .creator-name {
        color: #6a5acd;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .creator-details {
        color: #b0b0b0;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Botones */
    .button-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-top: 30px;
    }

    .stButton>button {
        background-color: #6a5acd;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px 30px;
        font-size: 1.2rem;
        text-transform: uppercase;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .stButton>button:hover {
        background-color: #5448c4;
        transform: scale(1.05);
        box-shadow: 0 6px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def mostrar_caratula():
    st.markdown('<div class="info-section">', unsafe_allow_html=True)
    st.title("Calculadora de Modelos de Costos")
    st.markdown('<p class="info-text">Esta calculadora permite analizar decisiones entre dos alternativas mediante tres modelos de costos:</p>', unsafe_allow_html=True)
    
    st.markdown("""
    - **Modelo de Costo Total:** Incluye todos los costos e ingresos de cada alternativa.
    - **Modelo de Costos Relevantes:** Se enfoca solo en los costos e ingresos que varían entre alternativas.
    - **Modelo de Costo de Oportunidad:** Calcula lo que se renuncia al elegir una alternativa.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="creator-section">', unsafe_allow_html=True)
    st.markdown('<div class="creator-name">Vanessa Bogado</div>', unsafe_allow_html=True)
    st.markdown('<div class="creator-details">Módulo de Gestión de Costos<br>Carrera Informática Empresarial<br>Universidad Paraguayo Alemana</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        if st.button("Modelo de Costo Total", key="btn_costo_total", use_container_width=True):
            st.session_state.page = "costo_total"
            st.experimental_rerun()
    
    with col2:
        if st.button("Modelo de Costos Relevantes", key="btn_costos_relevantes", use_container_width=True):
            st.session_state.page = "costos_relevantes"
            st.experimental_rerun()
    
    with col3:
        if st.button("Modelo de Costo de Oportunidad", key="btn_costo_oportunidad", use_container_width=True):
            st.session_state.page = "costo_oportunidad"
            st.experimental_rerun()
    
    with col4:
        if st.button("Modelo Combinado (3 en 1)", key="btn_modelo_combinado", use_container_width=True):
            st.session_state.page = "combinado"
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  

# Función para ingresar datos básicos de las alternativas  
def ingresar_datos_basicos():  
    st.write("### Datos básicos de las alternativas")  
    
    # Nombres de las alternativas  
    col1, col2 = st.columns(2)  
    with col1:  
        nombre_alt1 = st.text_input("Nombre de la Alternativa 1", "Alternativa 1")  
    with col2:  
        nombre_alt2 = st.text_input("Nombre de la Alternativa 2", "Alternativa 2")  
    
    # Datos de unidades y precios  
    col1, col2 = st.columns(2)  
    with col1:  
        st.subheader(f"{nombre_alt1}")  
        unidades1 = st.number_input(f"Unidades ({nombre_alt1})", min_value=0, value=0, step=1, key="unidades1")  
        precio1 = st.number_input(f"Precio por unidad ({nombre_alt1})", min_value=0, value=0, step=1, key="precio1")  
        costo_var_unit1 = st.number_input(f"Costo variable unitario ({nombre_alt1})", min_value=0, value=0, step=1, key="cvu1")  
    
    with col2:  
        st.subheader(f"{nombre_alt2}")  
        unidades2 = st.number_input(f"Unidades ({nombre_alt2})", min_value=0, value=0, step=1, key="unidades2")  
        precio2 = st.number_input(f"Precio por unidad ({nombre_alt2})", min_value=0, value=0, step=1, key="precio2")  
        costo_var_unit2 = st.number_input(f"Costo variable unitario ({nombre_alt2})", min_value=0, value=0, step=1, key="cvu2")  
    
    # Cálculos automáticos  
    ingreso1 = unidades1 * precio1  
    ingreso2 = unidades2 * precio2  
    
    costo_variable1 = unidades1 * costo_var_unit1  
    costo_variable2 = unidades2 * costo_var_unit2  
    
    margen1 = ingreso1 - costo_variable1  
    margen2 = ingreso2 - costo_variable2  
    
    st.markdown("---")  
    st.write("### Resultados calculados automáticamente")  
    
    # Mostrar los cálculos paso a paso  
    col1, col2 = st.columns(2)  
    with col1:  
        st.write(f"**Ingreso Total ({nombre_alt1}):** {unidades1} × ${precio1} = ${ingreso1:,}")  
        st.write(f"**Costo Variable Total ({nombre_alt1}):** {unidades1} × ${costo_var_unit1} = ${costo_variable1:,}")  
        st.write(f"**Margen de Contribución ({nombre_alt1}):** ${ingreso1:,} - ${costo_variable1:,} = ${margen1:,}")  
    
    with col2:  
        st.write(f"**Ingreso Total ({nombre_alt2}):** {unidades2} × ${precio2} = ${ingreso2:,}")  
        st.write(f"**Costo Variable Total ({nombre_alt2}):** {unidades2} × ${costo_var_unit2} = ${costo_variable2:,}")  
        st.write(f"**Margen de Contribución ({nombre_alt2}):** ${ingreso2:,} - ${costo_variable2:,} = ${margen2:,}")  
    
    return {  
        "nombre_alt1": nombre_alt1,  
        "nombre_alt2": nombre_alt2,  
        "unidades1": unidades1,  
        "unidades2": unidades2,  
        "precio1": precio1,  
        "precio2": precio2,  
        "costo_var_unit1": costo_var_unit1,  
        "costo_var_unit2": costo_var_unit2,  
        "ingreso1": ingreso1,  
        "ingreso2": ingreso2,  
        "costo_variable1": costo_variable1,  
        "costo_variable2": costo_variable2,  
        "margen1": margen1,  
        "margen2": margen2  
    }  

# Función para ingresar costos fijos con posibilidad de reducción porcentual  
def ingresar_costos_fijos(datos_basicos):  
    st.markdown("---")  
    st.write("### Costos Fijos")  
    
    # Inicializar lista de costos fijos predeterminados si no existe  
    if 'costos_fijos' not in st.session_state:  
        st.session_state.costos_fijos = []  
        
        # Agregar costos fijos predeterminados vacíos si es primera vez  
        costos_predeterminados = ["Arriendo", "Electricidad", "Remuneraciones", "Teléfono"]  
        for costo in costos_predeterminados:  
            st.session_state.costos_fijos.append({  
                "nombre": costo,  
                "valor1": 0,  
                "valor2": 0,  
                "reduccion": 0,  
                "relevante": False  
            })  
    
    # Mostrar costos fijos actuales  
    st.write("#### Costos fijos:")  
    
    # Lista temporal para mantener los costos fijos actualizados  
    costos_actualizados = []  
    
    # Para cada costo fijo, mostrar campos editables  
    for i, costo in enumerate(st.session_state.costos_fijos):  
        with st.container():  
            st.markdown("<div class='costo-box'>", unsafe_allow_html=True)  
            
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])  
            
            # Columna 1: Nombre editable del costo fijo  
            with col1:  
                nombre_costo = st.text_input(  
                    "Nombre del costo fijo",  
                    value=costo["nombre"],  
                    key=f"nombre_costo_{i}"  
                )  
            
            # Columna 2: Valor para alternativa 1  
            with col2:  
                valor1 = st.number_input(  
                    f"Valor para {datos_basicos['nombre_alt1']}",  
                    min_value=0,   
                    value=int(costo["valor1"]),   
                    step=1000,  
                    key=f"costo_{i}_valor1"  
                )  
            
            # Columna 3: Opciones para alternativa 2  
            with col3:  
                opcion = st.radio(  
                    f"Opción para Alt. 2",  
                    ["Mismo valor", "Valor diferente", "Reducción %"],  
                    index=0 if costo["reduccion"] == 0 and costo["valor1"] == costo["valor2"] else   
                         1 if costo["reduccion"] == 0 else 2,  
                    key=f"costo_{i}_opcion"  
                )  
                
                if opcion == "Mismo valor":  
                    valor2 = valor1  
                    reduccion = 0  
                    relevante = False  
                elif opcion == "Valor diferente":  
                    valor2 = st.number_input(  
                        f"Valor para {datos_basicos['nombre_alt2']}",  
                        min_value=0,   
                        value=int(costo["valor2"] if costo["valor2"] != valor1 else 0),   
                        step=1000,  
                        key=f"costo_{i}_valor2"  
                    )  
                    reduccion = 0  
                    relevante = (valor1 != valor2)  
                else:  # Reducción porcentual  
                    reduccion = st.slider(  
                        "% de reducción",   
                        0, 100,   
                        int(costo["reduccion"]) if costo["reduccion"] > 0 else 0,   
                        5,  
                        key=f"costo_{i}_reduccion"  
                    )  
                    valor2 = int(valor1 * (1 - reduccion/100))  
                    relevante = (reduccion > 0)  
                    st.write(f"Valor: ${valor2:,}")  
            
            # Columna 4: Opciones adicionales (relevante, eliminar)  
            with col4:  
                relevante = st.checkbox(  
                    "¿Es relevante?",   
                    value=relevante if 'relevante' in locals() else costo["relevante"],  
                    key=f"costo_{i}_relevante"  
                )  
                
                if st.button("Eliminar", key=f"eliminar_costo_{i}"):  
                    # No agregar este costo a la lista actualizada  
                    continue  
            
            # Agregar el costo actualizado a la lista temporal  
            costos_actualizados.append({  
                "nombre": nombre_costo,  
                "valor1": valor1,  
                "valor2": valor2,  
                "reduccion": reduccion,  
                "relevante": relevante  
            })  
            
            st.markdown("</div>", unsafe_allow_html=True)  
    
    # Actualizar la lista de costos fijos en la sesión  
    st.session_state.costos_fijos = costos_actualizados  
    
    # Agregar opción para nuevo costo fijo  
    with st.expander("Agregar nuevo costo fijo"):  
        nuevo_nombre = st.text_input("Nombre del nuevo costo fijo", key="nuevo_costo_nombre")  
        
        col1, col2 = st.columns(2)  
        
        with col1:  
            nuevo_valor1 = st.number_input(  
                f"Valor para {datos_basicos['nombre_alt1']}",  
                min_value=0,   
                value=0,   
                step=1000,  
                key="nuevo_valor1"  
            )  
        
        with col2:  
            opcion_nuevo = st.radio(  
                f"Opción para {datos_basicos['nombre_alt2']}",  
                ["Mismo valor", "Valor diferente", "Reducción %"],  
                key="opcion_nuevo"  
            )  
            
            if opcion_nuevo == "Mismo valor":  
                nuevo_valor2 = nuevo_valor1  
                nueva_reduccion = 0  
                es_relevante = False  
            elif opcion_nuevo == "Valor diferente":  
                nuevo_valor2 = st.number_input(  
                    f"Valor para {datos_basicos['nombre_alt2']}",  
                    min_value=0,   
                    value=0,   
                    step=1000,  
                    key="nuevo_valor2"  
                )  
                nueva_reduccion = 0  
                es_relevante = (nuevo_valor1 != nuevo_valor2)  
            else:  # Reducción porcentual  
                nueva_reduccion = st.slider("% de reducción", 0, 100, 0, 5, key="nueva_reduccion")  
                nuevo_valor2 = int(nuevo_valor1 * (1 - nueva_reduccion/100))  
                es_relevante = (nueva_reduccion > 0)  
                st.write(f"Valor con {nueva_reduccion}% reducción: ${nuevo_valor2:,}")  
        
        if st.button("Agregar costo fijo", key="btn_agregar"):  
            if nuevo_nombre:  
                st.session_state.costos_fijos.append({  
                    "nombre": nuevo_nombre,  
                    "valor1": nuevo_valor1,  
                    "valor2": nuevo_valor2,  
                    "reduccion": nueva_reduccion,  
                    "relevante": es_relevante  
                })  
                st.success(f"Costo fijo '{nuevo_nombre}' agregado exitosamente")  
                st.experimental_rerun()  
            else:  
                st.warning("Por favor, ingrese un nombre para el costo fijo")  
    
    # Resumen de costos fijos  
    if st.session_state.costos_fijos:  
        st.write("### Resumen de costos fijos")  
        
        # Total de costos fijos para cada alternativa  
        total_costos_fijos1 = sum(c["valor1"] for c in st.session_state.costos_fijos)  
        total_costos_fijos2 = sum(c["valor2"] for c in st.session_state.costos_fijos)  
        
        # Total de costos fijos relevantes  
        total_costos_relevantes1 = sum(c["valor1"] for c in st.session_state.costos_fijos if c["relevante"])  
        total_costos_relevantes2 = sum(c["valor2"] for c in st.session_state.costos_fijos if c["relevante"])  
        
        # Crear tabla resumen  
        data = {  
            "Costo Fijo": [c["nombre"] for c in st.session_state.costos_fijos] + ["**TOTAL**"],  
            datos_basicos['nombre_alt1']: [int(c["valor1"]) for c in st.session_state.costos_fijos] + [int(total_costos_fijos1)],  
            datos_basicos['nombre_alt2']: [int(c["valor2"]) for c in st.session_state.costos_fijos] + [int(total_costos_fijos2)],  
            "Reducción %": [c["reduccion"] for c in st.session_state.costos_fijos] + [""],  
            "¿Es Relevante?": [c["relevante"] for c in st.session_state.costos_fijos] + [""]  
        }  
        
        # Mostrar resumen en tabla  
        df = pd.DataFrame(data)  
        st.dataframe(df, use_container_width=True)  
        
        col1, col2 = st.columns(2)  
        with col1:  
            st.write(f"**Total Costos Fijos ({datos_basicos['nombre_alt1']}):** ${total_costos_fijos1:,}")  
            st.write(f"**Total Costos Relevantes ({datos_basicos['nombre_alt1']}):** ${total_costos_relevantes1:,}")  
        
        with col2:  
            st.write(f"**Total Costos Fijos ({datos_basicos['nombre_alt2']}):** ${total_costos_fijos2:,}")  
            st.write(f"**Total Costos Relevantes ({datos_basicos['nombre_alt2']}):** ${total_costos_relevantes2:,}")  
        
        if st.button("Borrar todos los costos fijos"):  
            st.session_state.costos_fijos = []  
            st.success("Todos los costos fijos han sido eliminados")  
            st.experimental_rerun()  
        
        return {  
            "costos_fijos": st.session_state.costos_fijos,  
            "total_costos_fijos1": total_costos_fijos1,  
            "total_costos_fijos2": total_costos_fijos2,  
            "total_costos_relevantes1": total_costos_relevantes1,  
            "total_costos_relevantes2": total_costos_relevantes2  
        }  
    
    else:  
        st.warning("No hay costos fijos ingresados")  
        return None  

# Función para calcular modelo de costo total  
def calcular_costo_total(datos_basicos, datos_costos):  
    # Cálculo de resultados  
    resultado1 = datos_basicos["margen1"] - datos_costos["total_costos_fijos1"]  
    resultado2 = datos_basicos["margen2"] - datos_costos["total_costos_fijos2"]  
    
    ventaja = resultado1 - resultado2  
    
    # Crear tabla para mostrar resultados  
    data = {  
        "Concepto": ["Ingreso", "Costo Variable", "Margen de Contribución"],  
        datos_basicos["nombre_alt1"]: [  
            int(datos_basicos["ingreso1"]),   
            int(datos_basicos["costo_variable1"]),   
            int(datos_basicos["margen1"])  
        ],  
        datos_basicos["nombre_alt2"]: [  
            int(datos_basicos["ingreso2"]),   
            int(datos_basicos["costo_variable2"]),   
            int(datos_basicos["margen2"])  
        ]  
    }  
    
    # Agregar cada costo fijo a la tabla  
    for costo in datos_costos["costos_fijos"]:  
        data["Concepto"].append(f"Costo Fijo: {costo['nombre']}")  
        data[datos_basicos["nombre_alt1"]].append(int(costo["valor1"]))  
        data[datos_basicos["nombre_alt2"]].append(int(costo["valor2"]))  
    
    # Agregar totales y resultado  
    data["Concepto"].extend(["Total Costos Fijos", "Resultado", f"Ventaja de {datos_basicos['nombre_alt1'] if ventaja > 0 else datos_basicos['nombre_alt2']}"])  
    
    data[datos_basicos["nombre_alt1"]].extend([  
        int(datos_costos["total_costos_fijos1"]),  
        int(resultado1),  
        int(abs(ventaja)) if ventaja > 0 else ""  
    ])  
    
    data[datos_basicos["nombre_alt2"]].extend([  
        int(datos_costos["total_costos_fijos2"]),  
        int(resultado2),  
        int(abs(ventaja)) if ventaja <= 0 else ""  
    ])  
    
    df = pd.DataFrame(data)  
    
    return df, resultado1, resultado2, ventaja  

# Función para calcular modelo de costos relevantes  
def calcular_costos_relevantes(datos_basicos, datos_costos):  
    # Resultado relevante  
    resultado_relevante1 = datos_basicos["margen1"] - datos_costos["total_costos_relevantes1"]  
    resultado_relevante2 = datos_basicos["margen2"] - datos_costos["total_costos_relevantes2"]  
    
    ventaja = resultado_relevante1 - resultado_relevante2  
    
    # Crear tabla para mostrar resultados  
    data = {  
        "Concepto": ["Ingreso", "Costo Variable", "Margen de Contribución"],  
        datos_basicos["nombre_alt1"]: [  
            int(datos_basicos["ingreso1"]),   
            int(datos_basicos["costo_variable1"]),   
            int(datos_basicos["margen1"])  
        ],  
        datos_basicos["nombre_alt2"]: [  
            int(datos_basicos["ingreso2"]),   
            int(datos_basicos["costo_variable2"]),   
            int(datos_basicos["margen2"])  
        ]  
    }  
    
    # Agregar solo costos fijos relevantes  
    costos_relevantes = [c for c in datos_costos["costos_fijos"] if c["relevante"]]  
    
    for costo in costos_relevantes:  
        data["Concepto"].append(f"Costo Relevante: {costo['nombre']}")  
        data[datos_basicos["nombre_alt1"]].append(int(costo["valor1"]))  
        data[datos_basicos["nombre_alt2"]].append(int(costo["valor2"]))  
    
    # Agregar totales y resultado  
    data["Concepto"].extend(["Total Costos Relevantes", "Resultado Relevante", f"Ventaja de {datos_basicos['nombre_alt1'] if ventaja > 0 else datos_basicos['nombre_alt2']}"])  
    
    data[datos_basicos["nombre_alt1"]].extend([  
        int(datos_costos["total_costos_relevantes1"]),  
        int(resultado_relevante1),  
        int(abs(ventaja)) if ventaja > 0 else ""  
    ])  
    
    data[datos_basicos["nombre_alt2"]].extend([  
        int(datos_costos["total_costos_relevantes2"]),  
        int(resultado_relevante2),  
        int(abs(ventaja)) if ventaja <= 0 else ""  
    ])  
    
    df = pd.DataFrame(data)  
    
    return df, resultado_relevante1, resultado_relevante2, ventaja  

# Función para calcular modelo de costo de oportunidad  
def calcular_costo_oportunidad(datos_basicos, resultado1, resultado2):  
    # El costo de oportunidad es el resultado de la alternativa no elegida  
    costo_oportunidad_alt1 = resultado2  # Si elijo alt1, pierdo resultado2  
    costo_oportunidad_alt2 = resultado1  # Si elijo alt2, pierdo resultado1  
    
    ventaja = resultado1 - resultado2  
    mejor_alternativa = datos_basicos["nombre_alt1"] if ventaja > 0 else datos_basicos["nombre_alt2"]  
    
    # Crear tabla para mostrar resultados  
    data = {  
        "Concepto": { 
            f"Resultado {datos_basicos['nombre_alt1']}",  
            f"Resultado {datos_basicos['nombre_alt2']}",  
            f"Costo de oportunidad si elijo {datos_basicos['nombre_alt1']}",  
            f"Costo de oportunidad si elijo {datos_basicos['nombre_alt2']}",  
            f"Ventaja de {mejor_alternativa}"}
    }
    # Inicializar estado de la aplicación
if "page" not in st.session_state:
    st.session_state.page = "caratula"

# Navegación principal
if st.session_state.page == "caratula":
    mostrar_caratula()
elif st.session_state.page == "costo_total":
    datos_basicos = ingresar_datos_basicos()
    datos_costos = ingresar_costos_fijos(datos_basicos)
    if datos_basicos and datos_costos:
        resultado_costo_total, resultado1, resultado2, ventaja = calcular_costo_total(datos_basicos, datos_costos)
        st.dataframe(resultado_costo_total)
    
    if st.button("Volver al Menú Principal"):
        st.session_state.page = "caratula"
        st.experimental_rerun()

elif st.session_state.page == "costos_relevantes":
    datos_basicos = ingresar_datos_basicos()
    datos_costos = ingresar_costos_fijos(datos_basicos)
    if datos_basicos and datos_costos:
        resultado_costos_relevantes, resultado1, resultado2, ventaja = calcular_costos_relevantes(datos_basicos, datos_costos)
        st.dataframe(resultado_costos_relevantes)
    
    if st.button("Volver al Menú Principal"):
        st.session_state.page = "caratula"
        st.experimental_rerun()

elif st.session_state.page == "costo_oportunidad":
    datos_basicos = ingresar_datos_basicos()
    datos_costos = ingresar_costos_fijos(datos_basicos)
    if datos_basicos and datos_costos:
        resultado_costo_total, resultado1, resultado2, _ = calcular_costo_total(datos_basicos, datos_costos)
        resultado_costo_oportunidad = calcular_costo_oportunidad(datos_basicos, resultado1, resultado2)
        st.write(resultado_costo_oportunidad)
    
    if st.button("Volver al Menú Principal"):
        st.session_state.page = "caratula"
        st.experimental_rerun()

elif st.session_state.page == "combinado":
    st.title("Modelo Combinado")
    datos_basicos = ingresar_datos_basicos()
    datos_costos = ingresar_costos_fijos(datos_basicos)
    
    if datos_basicos and datos_costos:
        # Costo Total
        resultado_costo_total, resultado1, resultado2, ventaja_total = calcular_costo_total(datos_basicos, datos_costos)
        st.subheader("Modelo de Costo Total")
        st.dataframe(resultado_costo_total)
        
        # Costos Relevantes
        resultado_costos_relevantes, resultado_relevante1, resultado_relevante2, ventaja_relevante = calcular_costos_relevantes(datos_basicos, datos_costos)
        st.subheader("Modelo de Costos Relevantes")
        st.dataframe(resultado_costos_relevantes)
        
        # Costo de Oportunidad
        resultado_costo_oportunidad = calcular_costo_oportunidad(datos_basicos, resultado1, resultado2)
        st.subheader("Modelo de Costo de Oportunidad")
        st.write(resultado_costo_oportunidad)
    
    if st.button("Volver al Menú Principal"):
        st.session_state.page = "caratula"
        st.experimental_rerun()
