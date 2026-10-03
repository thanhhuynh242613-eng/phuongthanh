import streamlit as st
import pandas as pd
st.image("logo.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 APP TÍNH LÃI GỬI TIẾT KIỆM_Huỳnh Thị Phương Thanh")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================

# Số tiền gửi
tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10000000.0,
    step=1000000.0,
    format="%.0f"
)

# Kỳ hạn
ky_han = st.selectbox(
    "📅 Kỳ hạn gửi",
    options=[1, 3, 6, 9, 12, 18, 24, 36],
    format_func=lambda x: f"{x} tháng"
)

# Lãi suất
lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

# Hình thức nhận lãi
hinh_thuc = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

st.divider()

# =========================
# NÚT TÍNH
# =========================

if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    
    elif lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
    
    else:
        # Lãi suất dạng thập phân
        lai_suat_nam = lai_suat / 100

        # =========================
        # TÍNH TỔNG TIỀN LÃI
        # =========================
        tong_tien_lai = tien_gui * lai_suat_nam * ky_han / 12

        # =========================
        # XÁC ĐỊNH SỐ KỲ NHẬN LÃI
        # =========================

        if hinh_thuc == "Cuối kỳ":
            so_ky = 1
            lai_dinh_ky = tong_tien_lai

        elif hinh_thuc == "Hàng tháng":
            so_ky = ky_han
            lai_dinh_ky = tong_tien_lai / so_ky

        else:  # Hàng quý
            so_ky = ky_han // 3

            # Nếu kỳ hạn không chia hết cho 3
            if so_ky == 0:
                so_ky = 1

            lai_dinh_ky = tong_tien_lai / so_ky

        # Tổng tiền cuối cùng
        tong_tien = tien_gui + tong_tien_lai

        # =========================
        # HIỂN THỊ KẾT QUẢ
        # =========================

        st.success("✅ TÍNH TOÁN THÀNH CÔNG!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💰 Tiền lãi định kỳ",
                f"{lai_dinh_ky:,.0f} VNĐ"
            )

        with col2:
            st.metric(
                "📈 Tổng tiền lãi",
                f"{tong_tien_lai:,.0f} VNĐ"
            )

        st.metric(
            "💵 Tổng tiền gốc + lãi",
            f"{tong_tien:,.0f} VNĐ"
        )

        st.divider()

        # =========================
        # BẢNG CHI TIẾT
        # =========================

        st.subheader("📊 Chi tiết tiền lãi")

        du_lieu = []

        if hinh_thuc == "Cuối kỳ":

            du_lieu.append({
                "Kỳ nhận lãi": f"Sau {ky_han} tháng",
                "Tiền lãi": f"{tong_tien_lai:,.0f} VNĐ",
                "Tiền gốc": f"{tien_gui:,.0f} VNĐ",
                "Tổng nhận": f"{tong_tien:,.0f} VNĐ"
            })

        elif hinh_thuc == "Hàng tháng":

            for i in range(1, ky_han + 1):

                du_lieu.append({
                    "Kỳ nhận lãi": f"Tháng {i}",
                    "Tiền lãi": f"{lai_dinh_ky:,.0f} VNĐ",
                    "Tiền gốc": f"{tien_gui:,.0f} VNĐ",
                    "Tổng nhận": f"{lai_dinh_ky:,.0f} VNĐ"
                })

        else:  # Hàng quý

            for i in range(1, so_ky + 1):

                du_lieu.append({
                    "Kỳ nhận lãi": f"Quý {i}",
                    "Tiền lãi": f"{lai_dinh_ky:,.0f} VNĐ",
                    "Tiền gốc": f"{tien_gui:,.0f} VNĐ",
                    "Tổng nhận": f"{lai_dinh_ky:,.0f} VNĐ"
                })

        df = pd.DataFrame(du_lieu)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # =========================
        # THÔNG TIN KHOẢN GỬI
        # =========================

        st.divider()

        st.subheader("📋 Thông tin khoản gửi")

        st.write(f"**Số tiền gửi:** {tien_gui:,.0f} VNĐ")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")
