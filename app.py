import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# CSS GIAO DIỆN
# ==============================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f4e79;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666666;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .result-box {
        background-color: #f5f9ff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #d9e8f5;
        margin-top: 20px;
    }

    .result-title {
        color: #1f4e79;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .result-item {
        font-size: 17px;
        margin: 10px 0;
    }

    .total {
        font-size: 20px;
        font-weight: bold;
        color: #0b6e4f;
    }
</style>
""", unsafe_allow_html=True)


# ==============================
# TIÊU ĐỀ
# ==============================
st.markdown(
    '<div class="main-title">💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Tính toán theo lãi đơn và lãi kép</div>',
    unsafe_allow_html=True
)


# ==============================
# NHẬP THÔNG TIN
# ==============================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=1200,
        value=12,
        step=1
    )

with col2:
    loai_lai = st.selectbox(
        "📈 Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    lai_suat = st.number_input(
        "📊 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )


# ==============================
# HÌNH THỨC NHẬN LÃI
# ==============================
hinh_thuc_nhan = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)


# ==============================
# NÚT TÍNH
# ==============================
st.write("")

if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif lai_suat < 0:
        st.error("⚠️ Lãi suất không được nhỏ hơn 0.")

    else:
        # ------------------------------
        # CHUYỂN ĐỔI
        # ------------------------------
        P = tien_gui
        r = lai_suat / 100
        months = ky_han
        years = months / 12

        # ------------------------------
        # LÃI ĐƠN
        # ------------------------------
        if loai_lai == "Lãi đơn":

            tong_lai = P * r * years
            tong_tien = P + tong_lai

            # Lãi mỗi tháng
            lai_thang = P * r / 12

            # Lãi mỗi quý
            lai_quy = P * r / 4

            if hinh_thuc_nhan == "Lãnh lãi hàng tháng":
                tien_lai_dinh_ky = lai_thang
                so_ky = months

            elif hinh_thuc_nhan == "Lãnh lãi hàng quý":
                tien_lai_dinh_ky = lai_quy
                so_ky = months / 3

            else:
                tien_lai_dinh_ky = tong_lai
                so_ky = 1

        # ------------------------------
        # LÃI KÉP
        # ------------------------------
        else:

            if hinh_thuc_nhan == "Lãnh lãi hàng tháng":

                lai_suat_thang = r / 12
                so_ky = months

                tong_tien = P * (1 + lai_suat_thang) ** so_ky
                tong_lai = tong_tien - P

                # Tiền lãi của kỳ đầu tiên
                tien_lai_dinh_ky = P * lai_suat_thang

            elif hinh_thuc_nhan == "Lãnh lãi hàng quý":

                lai_suat_quy = r / 4
                so_ky = months / 3

                # Nếu kỳ hạn không chia hết cho 3
                if months % 3 != 0:
                    st.warning(
                        "⚠️ Kỳ hạn không chia hết cho 3 tháng. "
                        "Phần tháng lẻ được tính theo số tháng thực tế."
                    )

                    # Tính theo tháng để chính xác hơn
                    lai_suat_thang = r / 12
                    tong_tien = P * (1 + lai_suat_thang) ** months
                    tong_lai = tong_tien - P

                    tien_lai_dinh_ky = (
                        P * ((1 + lai_suat_thang) ** 3 - 1)
                        if months >= 3
                        else P * lai_suat_thang * months
                    )

                else:
                    tong_tien = P * (1 + lai_suat_quy) ** so_ky
                    tong_lai = tong_tien - P

                    tien_lai_dinh_ky = (
                        P * ((1 + lai_suat_quy) ** 1 - 1)
                    )

                    # Lãi của quý đầu tiên
                    tien_lai_dinh_ky = P * lai_suat_quy

            else:
                # Lãi kép cuối kỳ:
                # Ghép lãi theo tháng
                lai_suat_thang = r / 12
                so_ky = months

                tong_tien = P * (1 + lai_suat_thang) ** so_ky
                tong_lai = tong_tien - P

                tien_lai_dinh_ky = tong_lai

        # ==============================
        # HIỂN THỊ KẾT QUẢ
        # ==============================
        st.markdown(
            '<div class="result-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="result-title">📊 KẾT QUẢ TÍNH TOÁN</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="result-item">
                <b>Hình thức tính:</b> {loai_lai}
            </div>

            <div class="result-item">
                <b>Số tiền gửi:</b> {P:,.0f} VNĐ
            </div>

            <div class="result-item">
                <b>Kỳ hạn:</b> {months} tháng
            </div>

            <div class="result-item">
                <b>Lãi suất:</b> {lai_suat:.2f}%/năm
            </div>

            <div class="result-item">
                <b>Nhận lãi:</b> {hinh_thuc_nhan}
            </div>

            <hr>

            <div class="result-item">
                <b>💵 Tiền lãi định kỳ:</b>
                {tien_lai_dinh_ky:,.0f} VNĐ
            </div>

            <div class="result-item">
                <b>💰 Tổng tiền lãi:</b>
                {tong_lai:,.0f} VNĐ
            </div>

            <div class="result-item total">
                🏦 Tổng tiền gốc + lãi:
                {tong_tien:,.0f} VNĐ
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ==============================
# GIẢI THÍCH CÔNG THỨC
# ==============================
with st.expander("📚 Xem công thức tính"):

    st.markdown("### 1. Lãi đơn")

    st.latex(r"I = P \times r \times t")

    st.write("""
    Trong đó:

    - **P**: Số tiền gốc
    - **r**: Lãi suất năm
    - **t**: Thời gian gửi tính theo năm
    - **I**: Tổng tiền lãi
    """)

    st.markdown("### 2. Lãi kép")

    st.latex(r"A = P(1 + r)^n")

    st.write("""
    Trong đó:

    - **P**: Số tiền gốc
    - **r**: Lãi suất của mỗi kỳ
    - **n**: Số kỳ tính lãi
    - **A**: Tổng số tiền nhận được cả gốc và lãi
    """)

    st.info(
        "💡 Với lãi kép, tiền lãi của mỗi kỳ được cộng vào tiền gốc "
        "để tiếp tục sinh lãi ở kỳ tiếp theo."
    )


# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("💰 Ứng dụng tính lãi tiền gửi tiết kiệm | Streamlit")
