import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="TABK-Irfan")

def olah_NPM(df, kode_kelas):
    df = df[df["Kelas"]==kode_kelas]
    df_temp = df[['Timestamp', 'NPM I', 'NPM II', 'Score']]
    df_temp['NPM I'] = df_temp['NPM I'].astype(str)
    df_temp['NPM II'] = df_temp['NPM II'].astype(str)
    df_temp['Score'] = df_temp['Score'].astype(str)
    df_temp["Score"] = df_temp["Score"].str.split('/').apply(lambda x: int(x[0]))
    df_temp = df_temp.sort_values("Timestamp", ascending=False)
    df_temp['time_score'] = range(len(df_temp))
    df_temp = pd.melt(df_temp, id_vars=["Score", "time_score"], value_vars=["NPM I", "NPM II"])
    df_temp = df_temp[["Score", "time_score", "value"]]
    df_temp.columns = ["Score", "time_score", "NPM"]
    df_temp = df_temp.dropna()
    df_temp['NPM'] = df_temp['NPM'].astype(str).str.split(".").apply(lambda x: x[0])
    min_value = 0
    max_value = 30
    df_temp['time_score'] = df_temp['time_score']**3
    df_temp['time_score'] = min_max_scaling(df_temp['time_score'], min_value, max_value).round(2)
    df_temp['final_score'] = df_temp['Score'] + df_temp['time_score']
    df_temp = df_temp.sort_values("final_score", ascending=False)
    return df_temp

def min_max_scaling(x, min_value, max_value):
    min_val = min(x)
    max_val = max(x)
    scaled_value = (x - min_val) * (max_value - min_value) / (max_val - min_val) + min_value
    return scaled_value

def recap(kelas, nilai, kode_kelas):
    kelas['NPM'] = kelas['NPM'].astype(str)
    nilai['NPM'] = nilai['NPM'].astype(str)
    df = kelas.merge(nilai, left_on="NPM", right_on="NPM")
    df = df.sort_values("final_score", ascending=False)
    df = df.reset_index()
    df = df[df["Kelas"] == kode_kelas]
    df = df[['Nama', 'final_score']]
    return df

def next_team(df):
    NPM1 = []
    NPM2 = []
    for i in range(int(len(df)/2)):
        o = (i+1)*(-1)
        NPM1.append((df["Nama"].values)[i])
        NPM2.append((df["Nama"].values)[o])
    if len(df)%2 != 0:
        NPM2.append(" ")
        NPM2.append(df['Nama'][int(len(df)/2)+1])
    df_next = pd.DataFrame({"I":NPM1, "II":NPM2})
    return df_next

def show(source_1, source_2, source_3, source_kelas, kode_kelas):
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.subheader("Babak I")
            if len(source_1) > 1:
                df1 = olah_NPM(source_1, kode_kelas)
                nilai1 = recap(source_kelas, df1, kode_kelas)
                st.table(nilai1.style.format({"final_score": "{:.2f}"}))
                next1 = next_team(nilai1)
                with st.expander("Next Team"):
                    st.dataframe(next1)
            else:   
                st.empty()
    with col2:
        with st.container(border=True):
            st.subheader("Babak II")
            if len(source_2) > 1:
                df2 = olah_NPM(source_2, kode_kelas)
                nilai2 = recap(source_kelas, df2, kode_kelas)
                st.table(nilai2.style.format({"final_score": "{:.2f}"}))
                next2 = next_team(nilai2)
                with st.expander("Next Team"):
                    st.dataframe(next2)
            else:
                st.empty()
    with col3:
        with st.container(border=True):
            st.subheader("Babak III")
            if len(source_3) > 1:
                df3 = olah_NPM(source_3, kode_kelas)
                nilai3 = recap(source_kelas, df3, kode_kelas)
                st.table(nilai3.style.format({"final_score": "{:.2f}"}))
            else:
                st.empty()
    with st.expander("Final Score"):
        df_merge = nilai1.merge(nilai2, left_on="Nama", right_on="Nama", suffixes=('satu', 'dua'))
        df_merge = df_merge.merge(nilai3, left_on="Nama", right_on="Nama")
        df_merge["FINAL_SCORE"] = df_merge['final_scoresatu'] + df_merge['final_scoredua'] + df_merge['final_score'] 
        df_merge = df_merge.sort_values("FINAL_SCORE", ascending=False)
        df_merge.index = range(1, len(df_merge)+1)
        st.dataframe(df_merge[['Nama', 'FINAL_SCORE']])


def refresh_data():
    st.session_state.turney1_1 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=1819435083")
    st.session_state.turney1_2 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=903057001")
    st.session_state.turney1_3 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=857540612")
    st.session_state.data_kelas = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=191090434")

def page_turney1():
    st.subheader("Kompetisi Pengolahan Data")
    st.write("Minggu ke-2")
    if "turney1_1" not in st.session_state:
        st.session_state.turney1_1 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=1819435083")
    if "turney1_2" not in st.session_state:
        st.session_state.turney1_2 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=903057001")
    if "turney1_3" not in st.session_state:
        st.session_state.turney1_3 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=857540612")
    tab_62, tab_63 = st.tabs(["6-02", "6-03"])
    with tab_63:
        show(st.session_state.turney1_1, st.session_state.turney1_2, st.session_state.turney1_3, st.session_state.data_kelas, "6-3")
    with tab_62:
        show(st.session_state.turney1_1, st.session_state.turney1_2, st.session_state.turney1_3, st.session_state.data_kelas, "6-2")

def page_tugas1():
    st.subheader("Tugas I")
    st.write("Membuat Pertanyaan berkaitan dengan materi minggu ke-1 dan minggu ke-2")
    tugas1 = pd.read_csv("https://docs.google.com/spreadsheets/d/1RleFeOXO9Z5M8g1wdyyB19J0MdQQKKMgV6s7s6uJteg/export?format=csv&gid=595386302")
    data_kelas = st.session_state.data_kelas
    tugas1['NPM'] = tugas1['NPM'].astype(str)
    data_kelas['NPM'] = data_kelas['NPM'].astype(str)
    df_tugas1 = pd.merge(data_kelas, tugas1, how="left", on=["NPM", "NPM"])
    df_tugas1 = df_tugas1[['NPM', 'Nama', 'Timestamp', 'Kelas']]
    df_tugas1 = df_tugas1.fillna('BELUM SUBMIT')
    df_tugas1.rename(columns={'Timestamp' : "Submission"}, inplace=True)
    df_tugas1_62 = df_tugas1[df_tugas1['Kelas'] == '6-2']
    df_tugas1_62.index = range(1, len(df_tugas1_62)+1)
    df_tugas1_63 = df_tugas1[df_tugas1['Kelas'] == '6-3']
    df_tugas1_63.index = range(1, len(df_tugas1_63)+1)
    col_tugas1_62, col_tugas1_63 = st.columns(2)
    with col_tugas1_62:
        belum = len(df_tugas1_62[df_tugas1_62['Submission']!='BELUM SUBMIT'])
        st.subheader("6-02")
        st.write(f"{belum}/{len(df_tugas1_62)}")
        st.dataframe(df_tugas1_62[['Nama', 'Submission']], use_container_width=True)
    with col_tugas1_63:
        belum = len(df_tugas1_63[df_tugas1_63['Submission']!='BELUM SUBMIT'])
        st.subheader("6-03")
        st.write(f"{belum}/{len(df_tugas1_63)}")
        st.dataframe(df_tugas1_63[['Nama', 'Submission']], use_container_width=True)

def aktivitas2():
    tab_akt2_62, tab_akt2_63 = st.tabs(["6-02", "6-03"])
    df_akt2_sub = pd.read_csv("https://docs.google.com/spreadsheets/d/1jGcZapP0WmIcvIuIJBMDF0DzWAjy8eCIO8vKwPhflqE/export?format=csv&gid=1292952548")
    data_kelas = st.session_state.data_kelas
    df_akt2_sub["NPM"] = df_akt2_sub["NPM"].astype(str)
    data_kelas["NPM"] = data_kelas["NPM"].astype(str)
    df_akt2 = pd.merge(df_akt2_sub, data_kelas, how="right", on=["NPM", "NPM"])
    df_akt2 = df_akt2[['NPM', 'Nama', 'Unggah file Excel', 'Kelas']]
    df_akt2.columns = ['NPM', 'Nama', 'File Excel', 'Kelas']
    with tab_akt2_62:
        df_akt2_62 = df_akt2[df_akt2['Kelas'] == '6-2'][['NPM', 'Nama', 'File Excel',]]
        df_akt2_62.index = range(1, len(df_akt2_62)+1)
        st.data_editor(df_akt2_62, use_container_width=True,
                       column_config={"File Excel" : st.column_config.LinkColumn("File Excel", display_text="Unduh")})
    with tab_akt2_63:
        df_akt2_63 = df_akt2[df_akt2['Kelas'] == '6-3'][['NPM', 'Nama', 'File Excel',]]
        df_akt2_63.index = range(1, len(df_akt2_63)+1)
        st.data_editor(df_akt2_63, use_container_width=True,
                       column_config={"File Excel" : st.column_config.LinkColumn("File Excel", display_text="Unduh")})


def main():
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 100px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
    if "data_kelas" not in st.session_state:
        st.session_state.data_kelas = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=191090434")
    st.header("Teknik Audit Berbantuan Komputer")
    main_col1, main_col2 = st.columns([0.8, 0.2])
    with main_col1:
        st.write("by Teuku Raja Irfan Radarma")
    with main_col2:
        if st.button("refresh"):
            refresh_data()

    st.sidebar.subheader("Navigasi")
    if st.sidebar.button("Aktivitas Kelas"):
        st.session_state.active_page = "Kompetisi"
    if st.sidebar.button("Tugas"):
        st.session_state.active_page = "Tugas"

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Tugas"
    if st.session_state.active_page == "Tugas":
        page_tugas1()
    elif st.session_state.active_page == "Kompetisi":
        tab_akt1, tab_akt2 = st.tabs(["Pengolahan Data", "Pengendalian Aplikasi"])
        with tab_akt1:
            page_turney1()
        with tab_akt2:
            aktivitas2()

if __name__ == "__main__":
    main()