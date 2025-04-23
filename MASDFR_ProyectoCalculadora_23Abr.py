import streamlit as st

# === CONFIGURACIONES ===

def obtener_recargos_deducibles():
    recargos_dm = {
        8: -0.10,
        6: -0.05,
        5:  0.00,
        4:  0.05,
        2:  0.10
    }

    recargos_rt = {
        14: -0.10,
        12: -0.05,
        10:  0.00,
        8:   0.05,
        6:   0.10
    }

    return recargos_dm, recargos_rt

def obtener_configuracion_producto():
    return {
        "prima_basica_dm": 4777.78,
        "prima_basica_rt": 2380.95,
        "prima_basica_rc": 1200.0,
        "prima_basica_gm": 400.0,
        "sa_basica_rc": 500000,
        "sa_basica_gm": 100000,
        "recargo_rc": 50,
        "recargo_gm": 20
    }

def calcular_prima_total(config, recargos_dm, recargos_rt, ded_dm, ded_rt, sa_rc, sa_gm):
    prima_dm = config["prima_basica_dm"] * (1 + recargos_dm[ded_dm])
    prima_rt = config["prima_basica_rt"] * (1 + recargos_rt[ded_rt])

    prima_rc = config["prima_basica_rc"]
    prima_gm = config["prima_basica_gm"]

    exceso_rc = max(0, sa_rc - config["sa_basica_rc"])
    exceso_gm = max(0, sa_gm - config["sa_basica_gm"])

    prima_exceso_rc = (exceso_rc // 50000) * config["recargo_rc"]
    prima_exceso_gm = (exceso_gm // 10000) * config["recargo_gm"]

    prima_total = (
        prima_dm +
        prima_rt +
        prima_rc +
        prima_exceso_rc +
        prima_gm +
        prima_exceso_gm
    )

    return {
        "prima_dm": prima_dm,
        "prima_rt": prima_rt,
        "prima_rc": prima_rc,
        "prima_exceso_rc": prima_exceso_rc,
        "prima_gm": prima_gm,
        "prima_exceso_gm": prima_exceso_gm,
        "prima_total": prima_total
    }

# === INTERFAZ STREAMLIT ===

def main():
    st.title("🧾 Cálculo de Prima de Seguro")

    recargos_dm, recargos_rt = obtener_recargos_deducibles()
    config = obtener_configuracion_producto()

    ded_dm = st.selectbox("Selecciona el deducible para Daños Materiales (%)", options=list(recargos_dm.keys()))
    ded_rt = st.selectbox("Selecciona el deducible para Robo Total (%)", options=list(recargos_rt.keys()))
    sa_rc = st.number_input("Suma Asegurada para Responsabilidad Civil ($)", min_value=config["sa_basica_rc"], step=50000)
    sa_gm = st.number_input("Suma Asegurada para Gastos Médicos ($)", min_value=config["sa_basica_gm"], step=10000)

    if st.button("Calcular Prima"):
        resultado = calcular_prima_total(config, recargos_dm, recargos_rt, ded_dm, ded_rt, sa_rc, sa_gm)
        
        st.subheader("📋 Desglose de la Prima")
        st.write(f"**Daños Materiales (ajustada):** ${resultado['prima_dm']:,.2f}")
        st.write(f"**Robo Total (ajustada):** ${resultado['prima_rt']:,.2f}")
        st.write(f"**Responsabilidad Civil - Básica:** ${resultado['prima_rc']:,.2f}")
        st.write(f"**Responsabilidad Civil - Exceso:** ${resultado['prima_exceso_rc']:,.2f}")
        st.write(f"**Gastos Médicos - Básica:** ${resultado['prima_gm']:,.2f}")
        st.write(f"**Gastos Médicos - Exceso:** ${resultado['prima_exceso_gm']:,.2f}")
        st.markdown("---")
        st.success(f"**TOTAL PRIMA EMITIDA:** ${resultado['prima_total']:,.2f}")

if __name__ == "__main__":
    main()
