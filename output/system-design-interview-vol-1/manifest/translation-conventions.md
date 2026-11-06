# Quy ước bản dịch

- Dịch đầy đủ nội dung từ PDF do người dùng cung cấp, giữ thứ tự các mục, lập luận, ví dụ, số liệu, công thức và tài liệu tham khảo; không thay bằng tóm tắt.
- Mỗi chương là một file `chuong-NN-ten-chuong-tieng-viet-khong-dau.md`, có một tiêu đề cấp 1 bằng tiếng Việt. Tên file giữ số chương hai chữ số, lấy từ tiêu đề trong manifest, chuyển về chữ thường không dấu và ngăn cách các từ bằng dấu gạch nối (ví dụ: `chuong-02-uoc-tinh-so-bo.md`). Dùng tiêu đề cấp 2, cấp 3 theo cấu trúc nguồn.
- Đầu file ghi tên chương tiếng Anh và khoảng trang PDF. Đánh dấu mỗi trang nguồn bằng comment `<!-- trang-pdf:NNN -->`, dùng ba chữ số. Đây là số trang của file PDF, không phải số trang in.
- Viết tiếng Việt tự nhiên, giữ tên sản phẩm, API, lệnh và mã nguồn. Theo [bảng thuật ngữ](../vi/thuat-ngu.md); ở lần xuất hiện đầu tiên, có thể kèm thuật ngữ tiếng Anh trong ngoặc.
- Giữ nguyên hình gốc và nhãn tiếng Anh bên trong hình; dẫn hình bằng đường dẫn tương đối `../assets/goc-NNN.jpg`. Lời dẫn, chú thích bên ngoài hình và đoạn giải thích được dịch sang tiếng Việt. Không tự vẽ lại hoặc đổi số liệu.
- Bảng, công thức hoặc mã nguồn nằm trong ảnh được giữ bằng ảnh gốc để tránh sai lệch khi trích xuất. Không bỏ qua ảnh vì phần trích xuất văn bản không đọc được nó.
- Giữ các URL và số dẫn chiếu tham khảo. Tên tác phẩm trong danh mục tham khảo có thể giữ nguyên để tra cứu.
- Ghi chú bổ sung phải mang nhãn **Ghi chú bản dịch**, không hòa vào lời tác giả. Các nhận định của sách phản ánh thời điểm xuất bản, không được âm thầm sửa thành kiến thức mới.
