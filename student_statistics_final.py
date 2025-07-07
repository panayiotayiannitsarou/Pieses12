
import pandas as pd
import streamlit as st
from io import BytesIO

# ➤ Έλεγχος Ποιοτικών Χαρακτηριστικών (Προειδοποίηση για Απόκλιση >3)
def step7_8_quality_check(df, num_classes):
    st.subheader("🔍 Έλεγχος Ποιοτικών Χαρακτηριστικών")
    characteristics = ["ΦΥΛΟ", "ΚΑΛΗ ΓΝΩΣΗ ΕΛΛΗΝΙΚΩΝ", "ΙΚΑΝΟΠΟΙΗΤΙΚΗ ΜΑΘΗΣΙΑΚΗ ΙΚΑΝΟΤΗΤΑ"]
    for char in characteristics:
        value_counts = {}
        for i in range(num_classes):
            class_id = f'Τμήμα {i+1}'
            class_df = df[df['ΤΜΗΜΑ'] == class_id]
            count_N = (class_df[char] == 'Ν').sum()
            value_counts[class_id] = count_N

        max_diff = max(value_counts.values()) - min(value_counts.values())
        if max_diff > 3:
            st.warning(f"⚠️ Απόκλιση >3 στη στήλη '{char}': {value_counts}")

    return df

# ➤ Πίνακας Στατιστικών Ανά Τμήμα (με ονόματα στηλών όπως στο πρότυπο)
def show_statistics_table(df, num_classes):
    summary = []
    for i in range(num_classes):
        class_id = f'Τμήμα {i+1}'
        class_df = df[df['ΤΜΗΜΑ'] == class_id]
        total = class_df.shape[0]
        stats = {
            "ΤΜΗΜΑ": class_id,
            "ΑΓΟΡΙΑ": (class_df["ΦΥΛΟ"] == "Α").sum(),
            "ΚΟΡΙΤΣΙΑ": (class_df["ΦΥΛΟ"] == "Κ").sum(),
            "ΠΑΙΔΙΑ_ΕΚΠΑΙΔΕΥΤΙΚΩΝ": (class_df["ΠΑΙΔΙ ΕΚΠΑΙΔΕΥΤΙΚΟΥ"] == "Ν").sum(),
            "ΖΩΗΡΟΙ": (class_df["ΖΩΗΡΟΣ"] == "Ν").sum(),
            "ΙΔΙΑΙΤΕΡΟΤΗΤΕΣ": (class_df["ΙΔΙΑΙΤΕΡΟΤΗΤΑ"] == "Ν").sum(),
            "ΚΑΛΗ_ΓΝΩΣΗ_ΕΛΛΗΝΙΚΩΝ": (class_df["ΚΑΛΗ ΓΝΩΣΗ ΕΛΛΗΝΙΚΩΝ"] == "Ν").sum(),
            "ΙΚΑΝΟΠΟΙΗΤΙΚΗ_ΜΑΘΗΣΙΑΚΗ_ΙΚΑΝΟΤΗΤΑ": (class_df["ΙΚΑΝΟΠΟΙΗΤΙΚΗ ΜΑΘΗΣΙΑΚΗ ΙΚΑΝΟΤΗΤΑ"] == "Ν").sum(),
            "ΣΥΝΟΛΟ": total
        }
        summary.append(stats)

    stats_df = pd.DataFrame(summary)
    st.subheader("📊 Πίνακας Στατιστικών Ανά Τμήμα")
    st.dataframe(stats_df)

    if st.button("📥 Λήψη Excel με Κατανομή και Στατιστικά"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Κατανομή', index=False)
            stats_df.to_excel(writer, sheet_name='Στατιστικά', index=False)
        st.download_button(
            label="⬇️ Κατεβάστε το Αρχείο Excel",
            data=output.getvalue(),
            file_name="katanomi_kai_statistika.xlsx"
        )
