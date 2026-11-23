# 21. Strategy

[Mục lục](../README.md) · [English](../original/21-strategy.md)

## Bài toán

Một nhóm lưu trữ cần ước tính thời gian nhập tài liệu. Lượt nhập tương tác dùng số tệp và thời gian xử lý trung bình. Lượt nhập theo lịch còn tính thêm thời gian chờ đến khung chạy theo lô. Cả hai dùng chung màn hình trạng thái. Nếu cần thêm cách tính cho lượt chạy lại dữ liệu cũ, màn hình sẽ phải nhận thêm một nhánh xử lý.

Xác định hợp đồng trước khi tách logic. Ở đây, mỗi quy tắc nhận cùng dữ liệu đầu vào và trả về thời gian ước tính theo giây. Bên gọi xử lý kết quả theo cùng một cách.

## Mẫu thiết kế và ranh giới

Strategy cho phép đối tượng sử dụng, ở đây là hàm định dạng trạng thái, nhận thuật toán thay thế được qua một hợp đồng chung. Bên gọi biết chế độ nhập nên chọn quy tắc ngay tại đó rồi truyền vào. Trong TypeScript, một kiểu hàm đủ để diễn tả hợp đồng. Có thể kiểm thử từng quy tắc riêng và gắn quy tắc mới mà không sửa hàm định dạng.

Cả hai quy tắc phải thống nhất đơn vị và ý nghĩa đầu vào, đầu ra. Nếu một thuật toán còn tự lên lịch nhập, tác dụng phụ đó vượt ra ngoài hợp đồng này.

## Ví dụ TypeScript

```typescript
type ImportBatch = Readonly<{ fileCount: number; secondsPerFile: number }>;
type EstimateSeconds = (batch: ImportBatch) => number;

const interactiveEstimate: EstimateSeconds = ({ fileCount, secondsPerFile }) =>
  fileCount * secondsPerFile;

const scheduledEstimate: EstimateSeconds = (batch) =>
  60 + interactiveEstimate(batch);

function statusLine(batch: ImportBatch, estimate: EstimateSeconds): string {
  return `Estimated time: ${estimate(batch)} seconds`;
}

const batch = { fileCount: 3, secondsPerFile: 5 };

if (statusLine(batch, interactiveEstimate) !== "Estimated time: 15 seconds") {
  throw new Error("Interactive estimate should use the processing time");
}
if (statusLine(batch, scheduledEstimate) !== "Estimated time: 75 seconds") {
  throw new Error("Scheduled estimate should include the batch delay");
}
```

## Khi nên dùng

Dùng Strategy khi các cách tính thay đổi độc lập nhưng vẫn dùng chung đầu vào và đầu ra. Mẫu này cũng phù hợp khi hai bên gọi cần cùng một luồng xử lý với hai quy tắc riêng.

### Bài toán thường gặp

- **Tính phí vận chuyển.** Giao tiêu chuẩn có thể tính theo trọng lượng, còn giao nhanh tính thêm phụ phí. Bên gọi chọn cách tính theo dịch vụ đã mua. Các cách tính nên trả kết quả cùng đơn vị và áp dụng cùng quy tắc làm tròn để bên gọi xử lý nhất quán.
- **Chọn cách tính khuyến mãi.** Một chương trình giảm theo phần trăm, chương trình khác giảm một số tiền cố định. Luồng thanh toán chọn đúng một quy tắc rồi truyền vào bước tính giá. Nếu chỉ khác một giá trị phần trăm, truyền tham số. Nếu nhiều khuyến mãi được phép cộng dồn, cần quy tắc riêng cho thứ tự kết hợp.

## Khi cách đơn giản đã đủ

Giữ câu điều kiện nếu các quy tắc ngắn, ít thay đổi và chỉ dùng ở một chỗ. Nếu chỉ khác thời gian chờ, truyền tham số hoặc dùng bảng tra.

## Đánh đổi

Nơi chọn quy tắc và nơi thực hiện quy tắc tách nhau. Nên tập trung việc chọn vào một chỗ và đặt tên từng strategy theo chính sách mà nó thực hiện. Kiểu hàm kiểm tra được cấu trúc kết quả, còn đơn vị, ca thường và giá trị biên cần được kiểm thử.

## Bài tập

Thêm quy tắc chạy lại với thời gian xử lý mỗi tệp bằng một nửa số đã ghi và làm tròn tổng lên. Ba tệp, mỗi tệp năm giây, phải cho kết quả tám giây. Các chế độ cũ vẫn phải trả kết quả như trước.

## Tài liệu tham khảo

- [Strategy · Refactoring.Guru](https://refactoring.guru/design-patterns/strategy)

[← Chương trước · 20. State](20-state.md) · [Chương sau → · 22. Template Method](22-template-method.md)
