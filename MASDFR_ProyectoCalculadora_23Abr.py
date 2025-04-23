import streamlit as st

# === CONFIGURACIONES ===

def obtener_recargos_deducibles():
    return {
        "DM": {
            8: -0.10,
            6: -0.05,
            5:  0.00,
            4:  0.05,
            2:  0.10
        },
        "RT": {
            14: -0.10,
            12: -0.05,
            10:  0.00,
            8:   0.05,
            6:   0.10
        }
    }

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

def calcular_prima_total(config, recargos, ded_dm, ded_rt, sa_rc, sa_gm):
    prima_dm = config["prima_basica_dm"] * (1 + recargos["DM"][ded_dm])
    prima_rt = config["prima_basica_rt"] * (1 + recargos["RT"][ded_rt])

    prima_rc = config["prima_basica_rc"]
    prima_gm = config["prima_basica_gm"]

    exceso_rc = max(0, sa_rc - config["sa_basica_rc"])
    exceso_gm = max(0, sa_gm - config["sa_basica_gm"])

    prima_exceso_rc = (exceso_rc // 50000) * config["recargo_rc"]
    prima_exceso_gm = (exceso_gm // 10000) * config["recargo_gm"]

    prima_sin_iva = (
        prima_dm +
        prima_rt +
        prima_rc +
        prima_exceso_rc +
        prima_gm +
        prima_exceso_gm
    )

    iva = prima_sin_iva * 0.16
    prima_total_con_iva = prima_sin_iva + iva

    return {
        "prima_sin_iva": prima_sin_iva,
        "iva": iva,
        "prima_total_con_iva": prima_total_con_iva,
        "prima_dm": prima_dm,
        "prima_rt": prima_rt,
        "prima_rc": prima_rc,
        "prima_exceso_rc": prima_exceso_rc,
        "prima_gm": prima_gm,
        "prima_exceso_gm": prima_exceso_gm
    }

# === INTERFAZ STREAMLIT ===

def main():
    st.set_page_config(page_title="Cálculo de Prima de Seguro", page_icon="🧾", layout="centered")
    st.markdown("# 🧾 Cálculo de Prima de un Seguro de Automóvil")
    st.markdown("""
    Esta calculadora te permite conocer el monto total de tu prima de seguro para automóvil, basado en las coberturas seleccionadas y las sumas aseguradas elegidas. 
    Incluye los cálculos de los recargos por deducibles y las coberturas adicionales, como Daños Materiales, Robo Total, Responsabilidad Civil y Gastos Médicos.
    """)

    recargos = obtener_recargos_deducibles()
    config = obtener_configuracion_producto()

    with st.expander("🛠️ Configura tu seguro"):
        col1, col2 = st.columns(2)

        with col1:
            ded_dm = st.selectbox("📉 Deducible Daños Materiales (%)", options=sorted(recargos["DM"].keys()))
            sa_rc = st.number_input("🚗 Suma Asegurada RC ($)", min_value=config["sa_basica_rc"], step=50000)

        with col2:
            ded_rt = st.selectbox("🔐 Deducible Robo Total (%)", options=sorted(recargos["RT"].keys()))
            sa_gm = st.number_input("💊 Suma Asegurada GM ($)", min_value=config["sa_basica_gm"], step=10000)

    if st.button("💡 Calcular Prima"):
        resultado = calcular_prima_total(config, recargos, ded_dm, ded_rt, sa_rc, sa_gm)

        st.markdown("## 🧾 Desglose de Prima Total")
        st.markdown("""
        | Concepto | Monto ($) |
        |----------|-----------:|
        | ✅ Daños Materiales (ajustada) | ${:,.2f} |
        | ✅ Robo Total (ajustada) | ${:,.2f} |
        | ✅ Responsabilidad Civil - Básica | ${:,.2f} |
        | ➕ Responsabilidad Civil - Exceso | ${:,.2f} |
        | ✅ Gastos Médicos - Básica | ${:,.2f} |
        | ➕ Gastos Médicos - Exceso | ${:,.2f} |
        | 💸 Prima sin IVA | ${:,.2f} |
        | 🧾 IVA (16%) | ${:,.2f} |
        | 💰 Prima neta | **${:,.2f}** |
        """.format(
            resultado['prima_dm'],
            resultado['prima_rt'],
            resultado['prima_rc'],
            resultado['prima_exceso_rc'],
            resultado['prima_gm'],
            resultado['prima_exceso_gm'],
            resultado['prima_sin_iva'],
            resultado['iva'],
            resultado['prima_total_con_iva']
        ))

        st.success("✅ Cálculo completado correctamente.")
        st.balloons()

if __name__ == "__main__":
    main()
