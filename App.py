import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Parquet to Excel Converter", page_icon="📊", layout="wide")

st.title("📊 Parquet to Excel Converter")
st.markdown("Upload your `.parquet` file and download it as an Excel file")

# File uploader
uploaded_file = st.file_uploader("Choose a Parquet file", type=['parquet'])

if uploaded_file is not None:
    try:
        # Read the parquet file
        df = pd.read_parquet(uploaded_file)
        
        # Display file info
        st.success(f"✅ File loaded successfully!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", f"{len(df):,}")
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Show preview
        st.subheader("Data Preview")
        st.dataframe(df.head(100), use_container_width=True)
        
        # Column information
        with st.expander("📋 Column Details"):
            # Calculate null counts properly
            null_counts = df.isnull().sum()
            non_null_counts = len(df) - null_counts
            
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str),
                'Non-Null': non_null_counts.values,
                'Null': null_counts.values
            })
            st.dataframe(col_info, use_container_width=True, hide_index=True)
        
        # Convert to Excel
        st.subheader("Download Excel File")
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        
        excel_data = output.getvalue()
        
        # Download button
        original_filename = uploaded_file.name.replace('.parquet', '')
        st.download_button(
            label="⬇️ Download Excel File",
            data=excel_data,
            file_name=f"{original_filename}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        st.info("Please make sure you've uploaded a valid Parquet file.")

else:
    st.info("👆 Upload a Parquet file to get started")
    
    # Instructions
    st.markdown("""
    ### How to use:
    1. Click the **Browse files** button above
    2. Select your `.parquet` file
    3. Preview the data
    4. Click **Download Excel File** to get your `.xlsx` file
    
    ### Features:
    - ✨ Preview first 100 rows
    - 📊 View column statistics
    - 💾 Download as Excel (.xlsx)
    - 🚀 Fast conversion
    """)
