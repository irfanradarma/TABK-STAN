import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="Competition")

hide_github_icon = """

.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

def olah_NPM(df):
    df_temp = df[['Timestamp', 'NPM I', 'NPM II', 'NPM III', 'Score']]
    df_temp["Score"] = df_temp["Score"].str.split('/').apply(lambda x: int(x[0]))
    df_temp = pd.melt(df_temp, id_vars=["Score", "Timestamp"], value_vars=["NPM I", "NPM II", "NPM III"])
    df_temp = df_temp[["Score", "Timestamp", "value"]]
    df_temp.columns = ["Score", "Timestamp", "NPM"]
    df_temp = df_temp.dropna()
    df_temp['NPM'] = df_temp['NPM'].astype(str).str.split(".").apply(lambda x: x[0])
    min_value = 0
    max_value = 30
    df_temp = df_temp.sort_values("Timestamp", ascending=False)
    df_temp['time_score'] = range(len(df_temp))
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
                df1 = olah_NPM(source_1)
                nilai1 = recap(source_kelas, df1, kode_kelas)
                st.write("Skor")
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
                df2 = olah_NPM(source_2)
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
            if len(source_2) > 1:
                df3 = olah_NPM(source_3)
                nilai3 = recap(source_kelas, df3, kode_kelas)
                st.table(nilai3.style.format({"final_score": "{:.2f}"}))
            else:
                st.empty()

def refresh_data():
    st.session_state.source_1 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=1819435083")
    st.session_state.source_2 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=903057001")
    st.session_state.source_3 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=857540612")
    st.session_state.source_kelas = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=191090434")

def main():
    st.header("Leaderboard Pengolahan Data")
    if "source_1" not in st.session_state:
        # st.session_state.source_1 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=275808846") #dummy
        st.session_state.source_1 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=1819435083")
    if "source_2" not in st.session_state:
        st.session_state.source_2 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=903057001")
    if "source_3" not in st.session_state:
        st.session_state.source_3 = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=857540612")
    if "source_kelas" not in st.session_state:
        st.session_state.source_kelas = pd.read_csv("https://docs.google.com/spreadsheets/d/14Ouf1pPmmCoqYMxVhEleA93Tz7K2H3W2Q8_V8LpRDWk/export?format=csv&gid=191090434")

    main_col1, main_col2 = st.columns([0.8, 0.2])
    with main_col1:
        st.write("Minggu-2 TABK by Teuku Raja Irfan Radarma")
    with main_col2:
        if st.button("refresh"):
            refresh_data()
    
    tab_62, tab_63 = st.tabs(["6-02", "6-03"])
    with tab_62:
        show(st.session_state.source_1, st.session_state.source_2, st.session_state.source_3, st.session_state.source_kelas, "6-2")
    with tab_63:
        show(st.session_state.source_1, st.session_state.source_2, st.session_state.source_3, st.session_state.source_kelas, "6-3")
    

if __name__ == "__main__":
    main()