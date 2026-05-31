import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import streamlit as st
import wbdata
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO

st.set_page_config(page_title="Ajira Data Analysis", layout="wide")
st.title("🇰🇪 Kenya Youth Employment Analysis (Real Data)")
st.markdown("This dashboard uses real data from the World Bank, aligned with the Ajira Digital Program.")

@st.cache_data
def get_data():
    indicator = "SL.UEM.1524.ZS"
    data = wbdata.get_dataframe({indicator: "Unemployment_Rate"}, country="KE", parse_dates=False)
    data = data.reset_index()
    data = data.dropna()
    data['date'] = data['date'].astype(int).astype(str)
    return data

try:
    df = get_data()

    # Generate charts
    def create_chart1():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='date', y='Unemployment_Rate', marker='o', linewidth=2, color='#2E86AB', ax=ax)
        ax.set_title("Kenya Youth Unemployment Rate (Ages 15-24)", fontsize=14)
        ax.set_xlabel("Year")
        ax.set_ylabel("Unemployment Rate (%)")
        ax.grid(True, linestyle='--', alpha=0.6)
        return fig

    def create_chart2():
        df_temp = df.copy()
        df_temp['Change'] = df_temp['Unemployment_Rate'].diff()
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['red' if x > 0 else 'green' if x < 0 else 'gray' for x in df_temp['Change'].dropna()]
        sns.barplot(data=df_temp.dropna(subset=['Change']), x='date', y='Change', palette=colors, ax=ax)
        ax.set_title("Annual Change in Unemployment Rate", fontsize=14)
        ax.set_ylabel("Change (%)")
        ax.axhline(0, color='black', linewidth=0.8)
        return fig

    # Save data and charts to Excel
    excel_filename = "kenya_youth_unemployment_ajira_with_charts.xlsx"
    
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Write data to Excel
        df.to_excel(writer, sheet_name='Data', index=False)
        
        # Get workbook
        workbook = writer.book
        worksheet = writer.sheets['Data']
        
        # Insert Chart 1
        fig1 = create_chart1()
        img_buffer = BytesIO()
        fig1.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)
        img1 = Image(img_buffer)
        worksheet.add_image(img1, 'B15')
        plt.close(fig1)
        
        # Insert Chart 2
        fig2 = create_chart2()
        img_buffer2 = BytesIO()
        fig2.savefig(img_buffer2, format='png', bbox_inches='tight')
        img_buffer2.seek(0)
        img2 = Image(img_buffer2)
        worksheet.add_image(img2, 'Z15')
        plt.close(fig2)

    # Save buffer to file and offer download
    with open(excel_filename, 'wb') as f:
        f.write(buffer.getvalue())
    
    st.success(f"✅ Data and charts saved to **{excel_filename}**")
    
    with open(excel_filename, "rb") as file:
        st.download_button(
            label="📥 Download Excel with Charts",
            data=file,
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Display charts in Streamlit
    st.pyplot(create_chart1())
    st.pyplot(create_chart2())

except Exception as e:
    st.error(f"Error: {e}")

st.sidebar.header("About This Data")
st.sidebar.write("""
- **Source**: World Bank Open Data
- **Indicator**: Youth Unemployment (% of labor force ages 15-24)
- **Country**: Kenya
- **Relevance**: Tracks the core challenge the Ajira Digital Program aims to solve.
""")   